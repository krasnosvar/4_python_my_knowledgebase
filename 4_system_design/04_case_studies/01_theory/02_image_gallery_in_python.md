# Кейс 2: Галерея изображений и медиа-пайплайн на Python

## О чём эта тема (краткий контекст)

Хранение и обработка пользовательских медиафайлов (фотографий, видео,
документов) характеризуются огромным объёмом бинарных данных (терабайты и
петабайты), тяжёлой процессорной нагрузкой при генерации превью (ресайз,
конвертация в WebP/AVIF) и экстремальным перекосом чтения к записи (1000:1).
Поэтому в архитектуре медиа-сервиса метаданные (PostgreSQL) с первого дня
отделяют от самих байтов (S3-совместимое объектное хранилище), загрузку уводят
мимо бэкенда через Presigned URLs, тяжёлую обработку выносят в асинхронную
очередь воркеров, а раздачу закрывают через CDN.

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Фреймворк System Design интервью и расчёты нагрузки](../../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/01_theory/01_interview_framework_and_estimations.md)
> - [Сквозные кейсы: денежные переводы, медиа-галерея, URL Shortener и лента](../../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/01_theory/02_case_studies_transfers_and_media.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки). Рабочую модель пайплайна с дедупликацией
> по SHA-256 на чистом Python можно запустить в [`main.py` (Image
> Pipeline)](../02_examples/02_image_pipeline_dedup/main.py).

---

## 1. Почему `await file.read()` убивает Python-воркеры по памяти (OOM)

Самая частая ошибка в FastAPI/Django при работе с файлами — вычитать весь
загруженный пользователем файл в оперативную память одной строкой:

```python
from fastapi import FastAPI, UploadFile

app = FastAPI()


# ❌ АНТИПАТТЕРН: 50 загрузок по 20 МБ = 1 ГБ в RAM воркера -> OOMKilled!
@app.post("/upload-bad")
async def upload_bad(file: UploadFile):
    content: bytes = await file.read()  # целиком аллоцирует буфер в куче Python
    ...
```

В Python крупный объект `bytes` сначала создаётся в памяти, затем копируется
при передаче в S3-клиент или при подсчёте хэша. При десятке одновременных
загрузок пиковое потребление RAM легко превышает лимит контейнера.

### Подход А (эталонный для высоких нагрузок): Presigned URL в S3 (`boto3`)

Бэкенд на Python вообще не пропускает через себя мегабайты пользовательских
файлов. Он лишь генерирует криптографически подписанный URL для прямой загрузки
в S3/MinIO (локальная операция с HMAC-SHA256, занимающая 0.1 мс и 0 сетевых
вызовов!):

```python
import uuid
import boto3
from botocore.config import Config

s3_client = boto3.client(
    "s3",
    endpoint_url="https://s3.example.com",
    config=Config(signature_version="s3v4"),
)


def create_upload_ticket(user_id: str, content_type: str) -> dict:
    object_key = f"raw/{user_id}/{uuid.uuid4()}"
    # Вычисляется локально на CPU без сетевого похода в S3!
    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": "media-uploads",
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=300,  # ссылка живёт 5 минут
    )
    return {"upload_url": upload_url, "object_key": object_key}
```

### Подход Б (если файл обязан пройти через Python): потоковое чтение чанками

Если по требованиям безопасности файл нужно пропустить через бэкенд и посчитать
его SHA-256 для дедупликации (Content-Addressed Storage, как в примере
[`main.py` (Image Pipeline)](../02_examples/02_image_pipeline_dedup/main.py)),
читайте поток фиксированными чанками по 64–256 КБ:

```python
import hashlib
from fastapi import HTTPException, UploadFile

CHUNK_SIZE = 64 * 1024          # 64 КБ в памяти независимо от размера файла
MAX_BYTES = 25 * 1024 * 1024    # жёсткий лимит 25 МБ


async def stream_and_hash(file: UploadFile) -> tuple[str, int]:
    hasher = hashlib.sha256()
    total_bytes = 0

    while chunk := await file.read(CHUNK_SIZE):
        total_bytes += len(chunk)
        if total_bytes > MAX_BYTES:
            raise HTTPException(status_code=413, detail="Файл превышает 25 МБ")
        hasher.update(chunk)

    return hasher.hexdigest(), total_bytes
```

---

## 2. Асинхронный пайплайн ресайза (`Pillow` / `pyvips` + Celery)

Декодирование JPEG/PNG и пересчёт пикселей в WebP/AVIF — тяжёлая CPU-bound и
RAM-bound операция. Выполнять её внутри `async def` обработчика FastAPI
нельзя: даже если C-код внутри `Pillow` частично отпускает GIL при сжатии, он
удерживает поток ОС на сотни миллисекунд и блокирует `asyncio` Event Loop.

### Архитектура обработки медиа в Python

1. После загрузки оригинала в S3 API сохраняет строку в PostgreSQL со статусом
   `status = "processing"` и ставит задачу
   `generate_image_variants.delay(image_id)` в очередь **Celery / Dramatiq /
   Taskiq**.
2. Воркеры обработки запускаются в отдельном пуле контейнеров с флагом
   `--concurrency` по числу ядер CPU и настройкой
   **`--max-tasks-per-child=500`** (перезапуск дочернего процесса каждые 500
   картинок гарантированно возвращает ОС фрагментированную C-кучу
   `libjpeg`/`libwebp`).

### Защита от Decompression Bomb («бомб декомпрессии») в `Pillow`

Злоумышленник может загрузить специально сформированный PNG-файл весом всего
400 КБ с разрешением $100\,000 \times 100\,000$ пикселей. При вызове
`Image.open().load()` распакованный буфер потребует **40 ГБ RAM** и мгновенно
убьёт воркер.

```python
from io import BytesIO
from PIL import Image, ImageOps

# Жёсткий порог: не более 25 мегапикселей (например, 5000x5000)
Image.MAX_IMAGE_PIXELS = 25_000_000

VARIANTS = {
    "thumbnail": (256, 256),
    "medium": (1080, 1080),
}


def build_webp_variants(raw_bytes: bytes) -> dict[str, bytes]:
    results: dict[str, bytes] = {}
    with Image.open(BytesIO(raw_bytes)) as img:
        # Поворачиваем по EXIF-ориентации и одновременно очищаем приватные
        # EXIF-метаданные (GPS-координаты пользователя, серийный номер камеры)
        clean_img = ImageOps.exif_transpose(img).convert("RGB")

        for name, max_size in VARIANTS.items():
            copy = clean_img.copy()
            copy.thumbnail(max_size, Image.Resampling.LANCZOS)
            buf = BytesIO()
            copy.save(buf, format="WEBP", quality=82, method=4)
            results[name] = buf.getvalue()

    return results
```

> **Альтернатива для сверхвысоких нагрузок (`pyvips`):** если сервис
> обрабатывает тысячи изображений в секунду, вместо `Pillow` используют
> **`pyvips`** (биндинг к потоковой C-библиотеке `libvips`). Она обрабатывает
> изображение полосами (streaming pipeline), потребляет в 5–10 раз меньше
> оперативной памяти и полностью освобождает GIL.

---

## 3. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** Почему при работе с объектом `UploadFile` в Starlette/FastAPI
> важно знать про параметр `SpooledTemporaryFile`?
>
> **Ответ:** Под капотом `UploadFile` оборачивает стандартный
> `tempfile.SpooledTemporaryFile(max_size=1024 * 1024)`. Пока размер файла не
> превышает 1 МБ, данные держатся в памяти (`BytesIO`), а при превышении 1 МБ
> автоматически сбрасываются во временный файл на диске (`/tmp`). Если в
> контейнере `/tmp` смонтирован как `tmpfs` в RAM или диск контейнера
> маленький, параллельная загрузка крупных файлов через приложение всё равно
> исчерпает память/диск пода — поэтому для файлов больше нескольких мегабайт
> нужно использовать прямую загрузку в S3 по Presigned URL.

> **Вопрос:** Зачем воркерам Celery, обрабатывающим изображения через `Pillow`,
> в продакшене обязательно задают `--max-tasks-per-child` (или
> `--max-memory-per-child`)?
>
> **Ответ:** При аллокации и освобождении больших буферов изображений в C-куче
> (`glibc malloc`) возникает фрагментация памяти: Python уже удалил объект
> `Image`, но страница памяти на верхушке кучи занята мелким объектом, поэтому
> `glibc` не возвращает освободившиеся сотни мегабайт обратно ядру ОС (метрика
> RSS процесса только растёт). Периодический плановый рестарт воркер-процесса
> через `--max-tasks-per-child=500` полностью очищает адресное пространство
> процесса без прерывания работы очереди.

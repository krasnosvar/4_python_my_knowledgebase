# Разбор кейсов на Python — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/) и каноническом разделе
[DevOps System Design](../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/).
⚠️ — типичная ошибка в Python-проектах, которая дорого обходится.

## Два эталонных кейса в Python-стеке

| Критерий | Денежные переводы | Галерея изображений |
| :--- | :--- | :--- |
| **Главное требование** | Строгая консистентность (ACID), идемпотентность, аудит | Read-heavy (1000:1), дешёвое хранение ТБ/ПБ, низкая latency |
| **Типы данных в Python** | `int` (минорные единицы: копейки/центы) или `Decimal` | Потоковые чанки `bytes` (64 КБ) + метаданные в Pydantic/ORM |
| **Защита от гонок / OOM** | `SELECT ... FOR UPDATE` с сортировкой ID (`sorted([a, b])`) | Прямая загрузка в S3 по Presigned URL (`boto3`) или чтение чанками |
| **Роль фоновых воркеров** | Outbox Relay — доставка события о свершившемся переводе | Вынос CPU-bound ресайза (`Pillow` / `pyvips`) в Celery |

## Денежные переводы на Python

Подробнее:
[01_money_transfers_in_python.md](./01_theory/01_money_transfers_in_python.md)

| Узел реализации | Как делать в Python (`SQLAlchemy` / `Django`) |
| :--- | :--- |
| Представление сумм | `amount_minor: int` (`BIGINT`) или `Decimal("10.50")`, **никогда не `float`** |
| Защита от Deadlock при блокировке пары счетов | `ordered = sorted([from_id, to_id])` → `.where(Account.id.in_(ordered)).order_by(Account.id).with_for_update()` |
| Проверка `Idempotency-Key` | Запись ключа + `payload_hash` с `with_for_update=True` или `ON CONFLICT` внутри той же транзакции |
| Внешние HTTP-вызовы (банки, антифрод) | **Строго вне транзакции БД!** Иначе `FOR UPDATE` держит локи и забивает пул `PgBouncer` |

Деньги в минорных единицах и инвариант двойной записи:

```python
print(0.1 + 0.2 == 0.3)   # False — float копит ошибки округления
print(10 + 20 == 30)      # True — копейки в int точны

entries = [("T1", "A", "DEBIT", 500), ("T1", "B", "CREDIT", 500)]
debits = sum(a for _, _, d, a in entries if d == "DEBIT")
credits = sum(a for _, _, d, a in entries if d == "CREDIT")
print(debits == credits)  # True
```

## Галерея изображений и медиа-пайплайн на Python

Подробнее:
[02_image_gallery_in_python.md](./01_theory/02_image_gallery_in_python.md)

| Узел реализации | Как делать в Python (`FastAPI` / `Celery` / `Pillow`) |
| :--- | :--- |
| Приём больших файлов | `s3_client.generate_presigned_url("put_object", ...)` — клиент грузит байты напрямую в S3 |
| Потоковое хэширование (SHA-256) | `while chunk := await file.read(65536): hasher.update(chunk)` (константные 64 КБ в RAM) |
| Защита от Decompression Bomb | `Image.MAX_IMAGE_PIXELS = 25_000_000` перед `Image.open()` |
| Очистка приватных EXIF (GPS) | `ImageOps.exif_transpose(img).convert("RGB")` перед сохранением в WebP |
| Защита от фрагментации C-кучи в Celery | Запускать воркеры с `--max-tasks-per-child=500` (или использовать `pyvips`) |

Оценка нагрузки (10 млн загрузок в сутки, 3.5 МБ на фото с вариантами):

```python
uploads_per_day = 10**7
seconds_per_day = 10**5  # ~86 400, округлено для оценки
read_write_ratio = 1000
print(uploads_per_day / seconds_per_day)                    # 100.0 write QPS
print(uploads_per_day * read_write_ratio / seconds_per_day) # 100000.0 read QPS
print(uploads_per_day * 3.5 / 10**6, "TB/сутки")            # 35.0 TB/сутки
```

## Типичные ошибки в Python

- ⚠️ Хранить деньги в `float` или делать `Decimal(0.1)` из `float` вместо
  строки `Decimal("0.1")`.
- ⚠️ Блокировать счёт отправителя и счёт получателя двумя отдельными `SELECT
  ... FOR UPDATE` в порядке `from_id → to_id` → гарантированный Deadlock при
  встречном переводе `B → A`.
- ⚠️ Делать `await httpx_client.post()` внутри блока `async with
  session.begin():` после взятия `FOR UPDATE` → паралич БД.
- ⚠️ Вызывать `await file.read()` без размера чанка на пользовательских файлах
  → `OOMKilled` воркера Uvicorn.
- ⚠️ Запускать ресайз `Pillow` прямо в `async def` хендлере FastAPI →
  блокировка Event Loop и деградация всех остальных запросов.

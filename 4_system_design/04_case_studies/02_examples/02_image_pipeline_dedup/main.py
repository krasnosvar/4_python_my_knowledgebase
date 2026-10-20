"""
Пример 02: пайплайн обработки изображения - метаданные, варианты, дедупликация.

Демонстрирует центральные решения из разбора "галерея изображений":
- разделение метаданных (маленькая структурированная запись) и байтов
  контента (условное "blob storage" - просто dict, эмулирующий его);
- асинхронный пайплайн генерации вариантов (thumbnail/medium) после
  завершения загрузки, вместо синхронной генерации в момент запроса;
- дедупликация по хэшу содержимого (content-addressed storage): повторная
  загрузка одинаковых байтов не создаёт вторую копию в blob storage.

Запуск: python3 ./02_examples/02_image_pipeline_dedup/main.py
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


class BlobStorage:
    """Эмуляция blob storage: адресация объектов по хэшу содержимого."""

    def __init__(self) -> None:
        self._objects: dict[str, bytes] = {}
        self.put_calls = 0  # сколько раз реально записывали новые байты

    @staticmethod
    def content_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()[:16]

    def put_if_absent(self, data: bytes) -> str:
        """Кладёт байты в хранилище, если объекта с таким хэшем ещё нет
        (дедупликация). Возвращает ключ объекта (хэш)."""
        key = self.content_hash(data)
        if key not in self._objects:
            self._objects[key] = data
            self.put_calls += 1
        return key

    def get(self, key: str) -> bytes:
        return self._objects[key]

    def object_count(self) -> int:
        return len(self._objects)


@dataclass
class ImageVariant:
    variant: str  # "thumbnail" | "medium" | "original"
    storage_key: str
    size_bytes: int


@dataclass
class ImageRecord:
    image_id: str
    owner_id: str
    status: str  # "processing" | "ready"
    variants: dict[str, ImageVariant] = field(default_factory=dict)


def fake_resize(data: bytes, variant: str) -> bytes:
    """Заглушка "обработки изображения": в реальном пайплайне здесь была бы
    настоящая генерация превью (например, через Pillow). Для примера просто
    берём префикс байтов, чтобы получить детерминированный "уменьшенный"
    результат разного размера на вариант."""
    sizes = {"thumbnail": 32, "medium": 128}
    n = sizes.get(variant, len(data))
    return data[:n] if n <= len(data) else data + b"\x00" * (n - len(data))


class ImagePipeline:
    """Координирует загрузку, дедупликацию и (эмулированно-асинхронную)
    генерацию вариантов изображения."""

    def __init__(self, storage: BlobStorage) -> None:
        self.storage = storage
        self.images: dict[str, ImageRecord] = {}
        self._next_id = 1

    def upload(self, owner_id: str, original_bytes: bytes) -> str:
        """Метаданные (ImageRecord) создаются сразу; тяжёлая генерация
        вариантов - отдельным шагом process(), эмулирующим асинхронного
        воркера, читающего событие "UploadCompleted" из брокера."""
        image_id = f"img-{self._next_id}"
        self._next_id += 1

        original_key = self.storage.put_if_absent(original_bytes)
        record = ImageRecord(
            image_id=image_id, owner_id=owner_id, status="processing"
        )
        record.variants["original"] = ImageVariant(
            "original", original_key, len(original_bytes)
        )
        self.images[image_id] = record
        return image_id

    def process(self, image_id: str) -> None:
        """Эмулирует асинхронного воркера: генерирует производные варианты
        и переводит статус в 'ready'. В реальной системе вызывается
        отдельным процессом-потребителем события из брокера, а не синхронно
        из upload()."""
        record = self.images[image_id]
        orig_key = record.variants["original"].storage_key
        original_bytes = self.storage.get(orig_key)

        for variant in ("thumbnail", "medium"):
            resized = fake_resize(original_bytes, variant)
            key = self.storage.put_if_absent(resized)
            record.variants[variant] = ImageVariant(variant, key, len(resized))

        record.status = "ready"


def main() -> None:
    print("--- Пример: пайплайн изображения с дедупликацией ---")

    storage = BlobStorage()
    pipeline = ImagePipeline(storage)

    original = b"fake-jpeg-bytes-" * 100  # эмуляция "тяжёлого" оригинала

    # Пользователь A загружает фото.
    image_a = pipeline.upload("user-A", original)
    status_a = pipeline.images[image_a].status
    print(f"Загружено (user-A): {image_a}, статус={status_a}")
    assert pipeline.images[image_a].status == "processing"

    # Асинхронный воркер обрабатывает изображение (генерирует варианты).
    pipeline.process(image_a)
    print(
        f"После обработки: статус={pipeline.images[image_a].status}, "
        f"варианты={list(pipeline.images[image_a].variants.keys())}"
    )
    assert pipeline.images[image_a].status == "ready"
    assert set(pipeline.images[image_a].variants) == {
        "original",
        "thumbnail",
        "medium",
    }

    objects_after_first_upload = storage.object_count()
    print(
        f"\nОбъектов в blob storage после первой загрузки: "
        f"{objects_after_first_upload}"
    )

    # Пользователь B загружает БАЙТ-В-БАЙТ такой же файл (например, пересланный
    # скриншот) - дедупликация должна распознать совпадение по хэшу и не
    # создать вторую копию оригинала в blob storage.
    image_b = pipeline.upload("user-B", original)
    pipeline.process(image_b)

    objects_after_second_upload = storage.object_count()
    print(
        f"Объектов в blob storage после повторной загрузки того же файла: "
        f"{objects_after_second_upload}"
    )

    assert objects_after_second_upload == objects_after_first_upload, (
        "дедупликация должна была предотвратить создание новых объектов "
        "для байт-в-байт идентичного контента"
    )

    # Но метаданные - отдельная запись на каждого владельца, это ожидаемо:
    # два разных image_id могут ссылаться на один и тот же объект в storage.
    assert image_a != image_b
    assert (
        pipeline.images[image_a].variants["original"].storage_key
        == pipeline.images[image_b].variants["original"].storage_key
    )

    print(
        "\nВывод: несмотря на то что user-A и user-B загрузили идентичные "
        "байты, blob storage хранит их физически один раз (адресация по "
        "хэшу содержимого), а метаданные (owner_id, image_id) остаются "
        "раздельными для каждого пользователя - разделение метаданных и "
        "байтов позволяет дедуплицировать контент, не теряя владение."
    )


if __name__ == "__main__":
    main()

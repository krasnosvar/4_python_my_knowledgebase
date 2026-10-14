"""Упражнение 1 (Kafka): партиционирование по ключу и порядок сообщений.

См. постановку задачи в ../README.md, раздел "Упражнение 1".

Нужно:
  1. Создать topic "events" с 3 партициями (если его ещё нет).
  2. Отправить не менее 9 событий для 3 разных user_id, используя user_id
     как ключ сообщения - так, чтобы порядок событий одного пользователя
     сохранялся при чтении.

Запуск: python producer.py  (стенд из 02_examples должен быть поднят)
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex1-producer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "events"
NUM_PARTITIONS = 3


async def ensure_topic_exists() -> None:
    """
    # TODO: используя AIOKafkaAdminClient, создай topic TOPIC с NUM_PARTITIONS
    # партициями и replication_factor=1, если он ещё не существует.
    # Подсказка: AIOKafkaAdminClient.create_topics([NewTopic(...)]) бросает
    # исключение, если topic уже есть - его нужно поймать и проигнорировать.
    """
    raise NotImplementedError("создай topic 'events' с 3 партициями")


async def send_events() -> None:
    await ensure_topic_exists()

    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k is not None else None,
    )
    await producer.start()
    try:
        # TODO: сформируй и отправь не менее 9 событий для 3 разных user_id
        # (например "user-1", "user-4", "user-8" - при 3 партициях и стандартном
        # партиционере эти три ключа детерминированно попадают в разные
        # партиции, что нагляднее для проверки "разные пользователи - разные
        # партиции"; впрочем, для самого упражнения подойдут любые ключи),
        # по 3+ события на каждого, с полем seq (0, 1, 2, ...) внутри каждого
        # user_id по возрастанию. Ключом сообщения (key=) должен быть user_id.
        #
        # Пример одного события:
        #   {"user_id": "user-1", "seq": 0, "action": "login"}
        #
        # После отправки залогируй, в какую партицию попало каждое сообщение
        # (producer.send_and_wait возвращает RecordMetadata с полем .partition).
        raise NotImplementedError("отправь события с ключом user_id")
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_events())

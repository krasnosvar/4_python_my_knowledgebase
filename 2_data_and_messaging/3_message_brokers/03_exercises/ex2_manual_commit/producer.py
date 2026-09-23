"""Упражнение 2 (Kafka): producer для проверки manual commit.

См. постановку задачи в ../README.md, раздел "Упражнение 2".

Отправляет 10 последовательных сообщений (номера 0..9) в topic
"manual-commit-demo". Партиционирование здесь не важно - для наглядности
эксперимента с commit'ом лучше, чтобы все сообщения были в одной партиции,
поэтому используем один и тот же ключ для всех.

Запуск: python producer.py  (стенд из 02_examples должен быть поднят)
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex2-producer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "manual-commit-demo"


async def send_sequence() -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
    )
    await producer.start()
    try:
        # TODO: отправь 10 сообщений {"number": i} для i от 0 до 9,
        # все с одним и тем же ключом (например "sequence"), чтобы все они
        # гарантированно попали в одну партицию и сохранили порядок отправки.
        raise NotImplementedError("отправь 10 последовательных сообщений")
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_sequence())

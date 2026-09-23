"""Упражнение 2 (Kafka) - решение: producer с последовательными сообщениями."""
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
        # Один и тот же ключ для всех 10 сообщений -> все они гарантированно
        # в одной партиции, порядок 0..9 сохраняется при чтении.
        for number in range(10):
            metadata = await producer.send_and_wait(
                TOPIC, value={"number": number}, key="sequence"
            )
            logger.info(
                "отправлено number=%d -> partition=%d offset=%d",
                number,
                metadata.partition,
                metadata.offset,
            )
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_sequence())

"""Упражнение 1 (Kafka) - решение: проверка порядка сообщений внутри партиции.

Проверяем два свойства, оба вытекающих из модели партиционирования Kafka
(01_theory/02_kafka_partitions.md):
  1. все сообщения одного user_id лежат в ОДНОЙ партиции (следствие того, что
     partition = hash(key) % num_partitions - детерминированная функция ключа);
  2. seq внутри партиции идёт строго по возрастанию (следствие того, что Kafka
     гарантирует порядок записи и чтения СТРОГО в пределах одной партиции).
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex1-consumer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "events"
GROUP_ID = "ex1-ordering-check"


async def consume_and_verify() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k is not None else None,
    )
    await consumer.start()

    seen: dict[str, list[tuple[int, int]]] = {}

    try:
        # Это разовый скрипт-проверка, а не долгоживущий сервис, поэтому нужно
        # уметь остановиться, когда сообщения закончились. У aiokafka НЕТ
        # "consumer_timeout_ms" в духе kafka-python (в aiokafka этот параметр
        # означает совсем другое - таймаут внутреннего фонового опроса, а не
        # сигнал "больше сообщений нет"). Поэтому используем getone() с явным
        # asyncio.wait_for: если 5 секунд не пришло ни одного нового
        # сообщения - считаем, что все данные вычитаны, и останавливаемся.
        while True:
            try:
                message = await asyncio.wait_for(consumer.getone(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.info("новых сообщений нет 5 секунд - останавливаемся")
                break

            user_id = message.value["user_id"]
            seq = message.value["seq"]
            seen.setdefault(user_id, []).append((message.partition, seq))
            logger.info(
                "получено: partition=%d key=%s seq=%d",
                message.partition,
                message.key,
                seq,
            )
    finally:
        await consumer.stop()

    for user_id, entries in seen.items():
        partitions = {p for p, _ in entries}
        seqs_in_order = [seq for _, seq in entries]

        same_partition = len(partitions) == 1
        strictly_increasing = seqs_in_order == sorted(seqs_in_order)

        status = "OK" if (same_partition and strictly_increasing) else "FAIL"
        logger.info(
            "%s: user_id=%s partitions=%s seqs=%s -> %s",
            status,
            user_id,
            partitions,
            seqs_in_order,
            "все события в одной партиции, порядок сохранён"
            if status == "OK"
            else "нарушение партиционирования или порядка",
        )


if __name__ == "__main__":
    asyncio.run(consume_and_verify())

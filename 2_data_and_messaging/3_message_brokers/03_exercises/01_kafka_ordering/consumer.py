"""Упражнение 1 (Kafka): чтение topic "events" и проверка порядка сообщений.

См. постановку задачи в ../README.md, раздел "Упражнение 1".

Нужно прочитать все сообщения topic'а "events" и убедиться, что для каждого
user_id значения seq идут строго по возрастанию в пределах партиции, а также
вывести, какая партиция досталась какому user_id.

Запуск: python consumer.py  (после producer.py)
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

    # TODO: заведи структуру данных вида {user_id: [(partition, seq), ...]}
    # и заполняй её по мере чтения сообщений.
    seen: dict[str, list[tuple[int, int]]] = {}

    try:
        # Это разовый скрипт-проверка, а не долгоживущий сервис - нужно уметь
        # остановиться, когда сообщения закончились. ВАЖНО: у aiokafka НЕТ
        # параметра, который останавливал бы `async for` по простою (в отличие
        # от kafka-python, где consumer_timeout_ms делает именно это - в
        # aiokafka одноимённый параметр означает другое, внутренний таймаут
        # фонового опроса, и `async for` с ним не завершится сам).
        #
        # TODO: вместо `async for message in consumer:` организуй цикл
        # `while True:`, внутри которого получай следующее сообщение через
        # `await asyncio.wait_for(consumer.getone(), timeout=5.0)`, и если
        # вылетит asyncio.TimeoutError - значит, новых сообщений 5 секунд не
        # было, и пора остановиться (break).
        #
        # TODO: для каждого полученного сообщения достань user_id, seq и
        # partition и добавь в seen. Залогируй partition/key/seq.
        raise NotImplementedError("реализуй цикл чтения с остановкой по таймауту")
    finally:
        await consumer.stop()

    # TODO: для каждого user_id проверь:
    #   1. все его сообщения лежат в ОДНОЙ и той же партиции;
    #   2. значения seq идут строго по возрастанию в порядке чтения.
    # Выведи результат проверки (OK / FAIL) для каждого user_id.
    for user_id, entries in seen.items():
        raise NotImplementedError("проверь порядок и партицию для каждого user_id")


if __name__ == "__main__":
    asyncio.run(consume_and_verify())

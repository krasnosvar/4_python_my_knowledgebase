"""Упражнение 2 (Kafka): manual commit offset'а ТОЛЬКО после успешной обработки.

См. постановку задачи в ../README.md, раздел "Упражнение 2".

process_message() ниже уже реализована и намеренно бросает исключение для
сообщения с number == 5 - это имитация временного сбоя обработки (например,
недоступность внешнего сервиса), не имеющая отношения к самому сообщению.
Твоя задача - реализовать consumer так, чтобы:
  - offset коммитился вручную, ТОЛЬКО после успешного вызова process_message();
  - при ошибке offset НЕ коммитился, и сообщение было прочитано повторно
    при следующем запуске consumer'а.

Важно (см. также TODO про "главное в этом упражнении" ниже): committed offset
в Kafka - это курсор "всё до этой позиции обработано", а не отметка по каждому
сообщению отдельно. Значит, если после провала number=5 продолжить цикл и
закоммитить number=6 (успешно обработанный) - этот коммит сдвинет курсор
и МИМО number=5 тоже, и оно будет потеряно, несмотря на то что вы вроде бы
"не закоммитили его". Поэтому при ошибке нужно не просто "не коммитить",
а прекратить обработку (остановить consumer), не читая дальше в этом запуске.

Запуск: python consumer.py  (после producer.py; скрипт должен остановиться
на number=5 и завершиться - перезапусти его, чтобы убедиться, что offset
так и остался на number=4, а number=5 читается заново)
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex2-consumer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "manual-commit-demo"
GROUP_ID = "ex2-manual-commit-group"


def process_message(payload: dict) -> None:
    """Не менять: сообщение number == 5 имитирует временный сбой обработки."""
    if payload["number"] == 5:
        raise RuntimeError("временная ошибка обработки (например, БД недоступна)")
    logger.info("обработано сообщение number=%s", payload["number"])


async def consume_with_manual_commit() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        # TODO: отключи авто-коммит offset'а - в этом упражнении commit
        # должен вызываться из кода вручную, а не по таймеру.
    )
    await consumer.start()
    try:
        async for message in consumer:
            try:
                process_message(message.value)
            except Exception:
                # TODO: залогируй ошибку (logger.exception) и ОСТАНОВИ consumer
                # (return/break), НЕ коммитя offset этого сообщения - при
                # следующем запуске consumer'а оно должно быть прочитано
                # и обработано снова. Не просто "continue" на следующее
                # сообщение - см. предупреждение в docstring про курсор.
                #
                # TODO (главное в этом упражнении): опиши здесь комментарием,
                # что конкретно сломалось бы, если бы вместо manual commit
                # был включён enable_auto_commit=True - что случилось бы
                # с сообщением number=5 при auto-commit по таймеру, если бы
                # consumer упал сразу после авто-коммита, но до успешной
                # обработки этого сообщения.
                raise NotImplementedError("обработай ошибку и останови consumer")

            # TODO: закоммить offset ТОЛЬКО здесь - после успешной обработки.
            raise NotImplementedError("закоммить offset после успеха")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_with_manual_commit())

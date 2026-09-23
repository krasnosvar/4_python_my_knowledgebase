"""Kafka consumer group: чтение topic "orders" с ручным коммитом offset'а.

Демонстрирует:
  - consumer-группу: несколько запущенных копий этого скрипта с одним
    и тем же group_id разделят партиции topic'а между собой автоматически
    (см. 01_theory/README.md, раздел 2.2);
  - manual commit ПОСЛЕ успешной обработки, а не до и не по таймеру.

Почему именно так, а не auto-commit (enable_auto_commit=True):
  при auto-commit offset коммитится по таймеру независимо от того, успела
  ли обработка сообщения завершиться. Если процесс упадёт МЕЖДУ авто-коммитом
  и завершением обработки - при рестарте consumer продолжит со следующего
  offset'а и молча потеряет недообработанные сообщения.
  Здесь commit вызывается вручную и только после того, как process_order()
  гарантированно отработал без исключения - то есть если процесс упадёт
  до коммита, при рестарте сообщение будет прочитано и обработано ПОВТОРНО
  (at-least-once), но никогда не будет потеряно. Плата за это - process_order()
  обязан быть идемпотентным (повторная обработка одного и того же order_id
  не должна портить результат).

Важный нюанс про сам commit(): committed offset в Kafka - это ЕДИНОЕ число-курсор
на партицию ("всё до этой позиции обработано"), а не отметка "вот это конкретное
сообщение подтверждено" по каждому сообщению отдельно. Из этого следует, что
если сообщение провалило обработку, а следующее за ним - обработалось успешно
и было закоммичено, то этот коммит молча "переедет" и провалившееся сообщение
тоже (оно окажется как бы обработанным с точки зрения Kafka, хотя это не так).
Поэтому ниже при ошибке мы не идём дальше по партиции, а останавливаем
consumer - в проде вместо остановки сообщение отправляют в отдельный
retry/DLQ-топик (см. 01_theory/README.md, раздел 4) и продолжают читать дальше,
уже не рискуя случайно "закоммитить мимо" непрочитанное сообщение.

Запуск (можно в нескольких терминалах для демонстрации consumer-группы):
    python kafka/consumer.py
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("kafka-consumer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "orders"
GROUP_ID = "orders-processing-group"


def process_order(order: dict) -> None:
    """Имитация обработки события заказа (запись в БД, вызов другого сервиса и т.п.)."""
    logger.info(
        "обработано: order_id=%s event=%s amount=%s",
        order["order_id"],
        order["event"],
        order["amount"],
    )


async def consume_orders() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        # Отключаем авто-коммит - коммитить offset будем сами, вручную,
        # и только после успешной обработки. См. пояснение в docstring выше.
        enable_auto_commit=False,
        auto_offset_reset="earliest",  # для новой группы - читать с начала топика
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k is not None else None,
    )

    await consumer.start()
    try:
        async for message in consumer:
            logger.info(
                "получено: partition=%d offset=%d key=%s",
                message.partition,
                message.offset,
                message.key,
            )

            try:
                process_order(message.value)
            except Exception:
                # Не коммитим offset при ошибке - сообщение будет прочитано
                # снова после перезапуска. И НЕ идём дальше по циклу: если
                # продолжить и закоммитить следующее (успешное) сообщение,
                # committed offset сдвинется и мимо этого, провалившегося -
                # см. пояснение в docstring про то, что commit - это курсор,
                # а не отметка по каждому сообщению. Останавливаем consumer.
                logger.exception(
                    "ошибка обработки partition=%d offset=%d, offset НЕ закоммичен - "
                    "останавливаемся, чтобы не закоммитить мимо этого сообщения",
                    message.partition,
                    message.offset,
                )
                return

            # Коммитим ТОЛЬКО после успешной обработки текущего сообщения.
            # commit() без аргументов коммитит текущую позицию consumer'а
            # по всем партициям, назначенным этому consumer'у на данный момент -
            # это безопасно ровно потому, что мы никогда не доходим сюда,
            # пропустив необработанное сообщение (см. return в except выше).
            await consumer.commit()
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_orders())

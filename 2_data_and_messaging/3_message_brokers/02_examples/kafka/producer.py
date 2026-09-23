"""Kafka producer: отправка сообщений с ключом в topic "orders".

Демонстрирует:
  - партиционирование по ключу: все сообщения с одним order_id всегда
    попадают в одну и ту же партицию (см. 01_theory/README.md, раздел 2.1) -
    это даёт гарантию порядка событий одного заказа при их последующем чтении;
  - явный уровень acks - компромисс между надёжностью и скоростью
    (см. раздел 2.4 теории про гарантии доставки).

Запуск (стенд из docker-compose.yml должен быть поднят):
    python kafka/producer.py
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("kafka-producer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "orders"
NUM_PARTITIONS = 3


async def ensure_topic_exists() -> None:
    """Явно создаём topic с несколькими партициями - иначе auto-create
    (KAFKA_AUTO_CREATE_TOPICS_ENABLE=true в docker-compose.yml) создаст topic
    с 1 партицией по умолчанию, и партиционирование по ключу будет негде
    продемонстрировать: всё окажется в единственной партиции."""
    admin = AIOKafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    await admin.start()
    try:
        topic = NewTopic(name=TOPIC, num_partitions=NUM_PARTITIONS, replication_factor=1)
        try:
            await admin.create_topics([topic])
            logger.info("topic '%s' создан с %d партициями", TOPIC, NUM_PARTITIONS)
        except TopicAlreadyExistsError:
            pass
    finally:
        await admin.close()


async def send_orders() -> None:
    await ensure_topic_exists()

    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        # acks="all" - ждать подтверждения от всех in-sync реплик, а не только
        # от лидера партиции. Дороже по латентности, но сообщение не потеряется
        # при падении лидера сразу после записи (см. теорию, at-least-once).
        # Для учебного одноброкерного стенда разница с acks=1 не видна на глаз,
        # но именно так выставляют acks в проде для событий, которые нельзя терять.
        acks="all",
        enable_idempotence=True,  # защита от дублей при retry на стороне producer'а
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        # Ключ сериализуем отдельно - именно по нему выбирается партиция.
        key_serializer=lambda k: k.encode("utf-8") if k is not None else None,
    )

    await producer.start()
    try:
        orders = [
            {"order_id": "order-1", "event": "created", "amount": 100},
            {"order_id": "order-2", "event": "created", "amount": 250},
            {"order_id": "order-1", "event": "paid", "amount": 100},
            {"order_id": "order-3", "event": "created", "amount": 75},
            {"order_id": "order-1", "event": "shipped", "amount": 100},
            {"order_id": "order-2", "event": "cancelled", "amount": 250},
        ]

        for order in orders:
            # key = order_id: все события ОДНОГО заказа (created/paid/shipped)
            # попадут в одну партицию и будут читаться в порядке отправки.
            # События РАЗНЫХ заказов могут попасть в разные партиции и не имеют
            # гарантии взаимного порядка друг относительно друга - это осознанный
            # компромисс ради параллелизма (см. теорию, раздел 2.1).
            metadata = await producer.send_and_wait(
                TOPIC, value=order, key=order["order_id"]
            )
            logger.info(
                "отправлено: order_id=%s event=%s -> partition=%d offset=%d",
                order["order_id"],
                order["event"],
                metadata.partition,
                metadata.offset,
            )
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_orders())

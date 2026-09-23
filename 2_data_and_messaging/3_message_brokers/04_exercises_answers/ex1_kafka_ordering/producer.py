"""Упражнение 1 (Kafka) - решение: партиционирование по ключу и порядок сообщений.

Ключевая идея решения: используя user_id как ключ сообщения, мы отдаём
Kafka выбор партиции через hash(key) % num_partitions. Это гарантирует, что
все события ОДНОГО пользователя лягут в одну партицию и будут прочитаны
в порядке отправки (см. 01_theory/README.md, раздел 2.1). Если бы ключ не
задавался, сообщения размазались бы по партициям round-robin, и порядок
между событиями одного пользователя не сохранялся бы.
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex1-producer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "events"
NUM_PARTITIONS = 3


async def ensure_topic_exists() -> None:
    """Создаём topic с явным числом партиций - полагаться на auto-create
    нельзя, т.к. auto-create по умолчанию создаёт topic с 1 партицией,
    а для этого упражнения важно именно несколько партиций."""
    admin = AIOKafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    await admin.start()
    try:
        topic = NewTopic(name=TOPIC, num_partitions=NUM_PARTITIONS, replication_factor=1)
        try:
            await admin.create_topics([topic])
            logger.info("topic '%s' создан с %d партициями", TOPIC, NUM_PARTITIONS)
        except TopicAlreadyExistsError:
            logger.info("topic '%s' уже существует, пропускаем создание", TOPIC)
    finally:
        await admin.close()


async def send_events() -> None:
    await ensure_topic_exists()

    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k is not None else None,
    )
    await producer.start()
    try:
        # Эти три ключа подобраны так, чтобы при 3 партициях и стандартном
        # партиционере aiokafka они детерминированно попадали в разные
        # партиции - так нагляднее видно, что "разные пользователи - разные
        # партиции" (для самого упражнения подошли бы и любые другие ключи,
        # важна лишь детерминированность hash(key) для ОДНОГО и того же ключа).
        user_ids = ["user-1", "user-4", "user-8"]
        events_per_user = 3

        for seq in range(events_per_user):
            for user_id in user_ids:
                event = {"user_id": user_id, "seq": seq, "action": "click"}
                # key=user_id - именно это определяет партицию (см. docstring выше).
                metadata = await producer.send_and_wait(TOPIC, value=event, key=user_id)
                logger.info(
                    "отправлено: user_id=%s seq=%d -> partition=%d offset=%d",
                    user_id,
                    seq,
                    metadata.partition,
                    metadata.offset,
                )
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_events())

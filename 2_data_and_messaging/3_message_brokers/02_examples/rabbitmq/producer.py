"""RabbitMQ producer: публикация в topic exchange с разными routing key.

Демонстрирует маршрутизацию по паттерну (см. 01_theory/06_rabbitmq.md):
  - exchange "orders_topic" типа topic;
  - routing key вида "orders.<страна>.<событие>";
  - разные сообщения уйдут в разные очереди в зависимости от того, как
    consumer.py забиндил свою очередь (см. соответствующий скрипт).

Запуск (стенд из docker-compose.yml должен быть поднят):
    python rabbitmq/producer.py
"""
from __future__ import annotations

import json
import logging

import pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("rabbitmq-producer")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE_NAME = "orders_topic"


def publish_orders() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    # durable=True - exchange переживёт перезапуск брокера (для учебного стенда
    # не критично, но так делают в проде, чтобы не терять топологию на рестарте).
    channel.exchange_declare(
        exchange=EXCHANGE_NAME, exchange_type="topic", durable=True
    )

    messages = [
        ("orders.eu.created", {"order_id": "order-1", "country": "eu", "event": "created", "amount": 100}),
        ("orders.us.created", {"order_id": "order-2", "country": "us", "event": "created", "amount": 250}),
        ("orders.eu.shipped", {"order_id": "order-1", "country": "eu", "event": "shipped", "amount": 100}),
        ("orders.us.cancelled", {"order_id": "order-2", "country": "us", "event": "cancelled", "amount": 250}),
        # Специально "плохое" сообщение без обязательного поля amount - на нём
        # consumer.py продемонстрирует retry с backoff и последующий уход в DLQ.
        # Это единственное eu-сообщение, которое должно провалиться -
        # остальные eu-сообщения корректны и обязаны быть обработаны успешно.
        ("orders.eu.created", {"order_id": "order-BAD", "country": "eu", "event": "created"}),
    ]

    for routing_key, payload in messages:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(payload).encode("utf-8"),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # persistent - сообщение переживёт рестарт брокера
            ),
        )
        logger.info("опубликовано: routing_key=%s payload=%s", routing_key, payload)

    connection.close()


if __name__ == "__main__":
    publish_orders()

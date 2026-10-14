"""Упражнение 4 (RabbitMQ) - решение: обычные и одно "ядовитое" сообщение."""
from __future__ import annotations

import json
import logging

import pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex4-producer")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE_NAME = "payments_topic"
ROUTING_KEY = "payments.charge"


def publish_payments() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct", durable=True)

    payments = [
        {"payment_id": "pay-1", "amount": 100},
        {"payment_id": "pay-2", "amount": 250},
        # Отрицательная сумма невалидна при любой попытке - систематическая
        # ошибка, а не временный сбой. Именно на ней сработает dead-lettering.
        {"payment_id": "pay-POISON", "amount": -50},
        {"payment_id": "pay-3", "amount": 75},
    ]

    for payload in payments:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=json.dumps(payload).encode("utf-8"),
            properties=pika.BasicProperties(
                content_type="application/json", delivery_mode=2
            ),
        )
        logger.info("опубликовано: %s", payload)

    connection.close()


if __name__ == "__main__":
    publish_payments()

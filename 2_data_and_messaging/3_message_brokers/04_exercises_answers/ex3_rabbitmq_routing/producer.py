"""Упражнение 3 (RabbitMQ) - решение: publish логов с разными routing key.

Routing key "logs.<service>.<level>". Специально включено сообщение
"logs.auth.error", которое должно быть доставлено сразу в ОБЕ очереди
упражнения (errors_queue - по level, auth_service_queue - по service) -
это демонстрирует, что биндинги topic exchange независимы друг от друга,
а не взаимоисключающие фильтры (см. 01_theory/README.md, раздел 3.1/3.4).
"""
from __future__ import annotations

import json
import logging

import pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex3-producer")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE_NAME = "logs_topic"


def publish_logs() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

    messages = [
        ("logs.auth.error", {"service": "auth", "level": "error", "msg": "login failed"}),
        ("logs.auth.info", {"service": "auth", "level": "info", "msg": "user logged in"}),
        ("logs.auth.warning", {"service": "auth", "level": "warning", "msg": "slow query"}),
        ("logs.billing.error", {"service": "billing", "level": "error", "msg": "charge failed"}),
        ("logs.billing.info", {"service": "billing", "level": "info", "msg": "invoice sent"}),
        ("logs.shipping.warning", {"service": "shipping", "level": "warning", "msg": "delay"}),
    ]

    for routing_key, payload in messages:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(payload).encode("utf-8"),
            properties=pika.BasicProperties(
                content_type="application/json", delivery_mode=2
            ),
        )
        logger.info("опубликовано: routing_key=%s payload=%s", routing_key, payload)

    connection.close()


if __name__ == "__main__":
    publish_logs()

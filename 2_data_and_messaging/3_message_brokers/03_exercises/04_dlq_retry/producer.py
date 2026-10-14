"""Упражнение 4 (RabbitMQ): publish обычных и одного "ядовитого" сообщения.

См. постановку задачи в ../README.md, раздел "Упражнение 4".

Запуск: python producer.py
(consumer.py стоит запустить ДО producer.py, чтобы очередь payments_queue
и вся DLX/DLQ-топология уже существовали)
"""
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

    # TODO: объяви exchange EXCHANGE_NAME (любой подходящий тип, например
    # "direct" - в этом упражнении важна не маршрутизация, а DLQ).
    raise NotImplementedError("объяви exchange payments_topic")

    payments = [
        {"payment_id": "pay-1", "amount": 100},
        {"payment_id": "pay-2", "amount": 250},
        # "Ядовитое" сообщение: отрицательная сумма невалидна и не может
        # быть обработана НИ ПРИ КАКОЙ повторной попытке - это должно
        # в итоге привести к dead-lettering, а не к бесконечным retry.
        {"payment_id": "pay-POISON", "amount": -50},
        {"payment_id": "pay-3", "amount": 75},
    ]

    for payload in payments:
        # TODO: опубликуй сообщение с ROUTING_KEY в EXCHANGE_NAME,
        # delivery_mode=2 (persistent).
        pass

    connection.close()


if __name__ == "__main__":
    publish_payments()

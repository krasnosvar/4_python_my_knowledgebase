"""Упражнение 3 (RabbitMQ): publish логов с разными routing key.

См. постановку задачи в ../README.md, раздел "Упражнение 3".

Routing key имеет формат "logs.<service>.<level>", например:
  logs.auth.error, logs.billing.warning, logs.auth.info

Запуск: python producer.py
(consumer_a.py и consumer_b.py стоит запустить ДО producer.py, чтобы очереди
уже существовали к моменту публикации - иначе non-durable подписки, начатые
позже публикации, эти сообщения не увидят)
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

    # TODO: объяви exchange EXCHANGE_NAME типа "topic", durable=True.
    raise NotImplementedError("объяви exchange logs_topic")

    messages = [
        # TODO: сформируй не менее 6 сообщений с разными комбинациями
        # service/level, минимум 2 разных сервиса (например "auth", "billing")
        # и минимум 2 разных уровня (например "error", "warning", "info"),
        # обязательно включи хотя бы одно сообщение "logs.auth.error"
        # (оно должно попасть сразу в обе очереди из этого упражнения).
    ]

    for routing_key, payload in messages:
        # TODO: опубликуй сообщение с этим routing_key в EXCHANGE_NAME.
        pass

    connection.close()


if __name__ == "__main__":
    publish_logs()

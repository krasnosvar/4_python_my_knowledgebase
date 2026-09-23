"""Упражнение 3 (RabbitMQ) - решение: очередь "все error-логи любого сервиса".

BINDING_KEY = "*.*.error": первые два "*" совпадают с ЛЮБЫМ одним словом
("logs" и <service>), последнее слово ДОЛЖНО быть "error" - это и даёт
"любой сервис, но только уровень error" (см. 01_theory/README.md, раздел 3.4:
"*" заменяет ровно одно слово в topic-паттерне).

Более явный (и чаще встречающийся на практике) вариант с фиксированным
первым словом - "logs.*.error" - тоже корректен, раз все наши routing key
всегда начинаются с "logs".
"""
from __future__ import annotations

import json
import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex3-consumer-a")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE_NAME = "logs_topic"
QUEUE_NAME = "errors_queue"
BINDING_KEY = "logs.*.error"


def on_message(
    channel: BlockingChannel,
    method: Basic.Deliver,
    _properties: BasicProperties,
    body: bytes,
) -> None:
    payload = json.loads(body.decode("utf-8"))
    logger.info("errors_queue получила: routing_key=%s payload=%s", method.routing_key, payload)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=BINDING_KEY)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    logger.info("ожидание сообщений в %s (Ctrl+C для выхода)", QUEUE_NAME)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()

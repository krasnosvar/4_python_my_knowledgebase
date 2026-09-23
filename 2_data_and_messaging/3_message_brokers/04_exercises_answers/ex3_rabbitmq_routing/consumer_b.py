"""Упражнение 3 (RabbitMQ) - решение: очередь "все логи одного сервиса".

BINDING_KEY = "logs.auth.#": первые два слова фиксированы ("logs" и "auth"),
"#" на месте level означает "ноль или более любых слов после этого" - то есть
подойдёт "logs.auth.error", "logs.auth.info", "logs.auth.warning" и даже
гипотетический "logs.auth.error.critical" (два слова после auth), но не
подойдёт "logs.billing.error" (см. 01_theory/README.md, раздел 3.4).
"""
from __future__ import annotations

import json
import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex3-consumer-b")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE_NAME = "logs_topic"
QUEUE_NAME = "auth_service_queue"
BINDING_KEY = "logs.auth.#"


def on_message(
    channel: BlockingChannel,
    method: Basic.Deliver,
    _properties: BasicProperties,
    body: bytes,
) -> None:
    payload = json.loads(body.decode("utf-8"))
    logger.info(
        "auth_service_queue получила: routing_key=%s payload=%s",
        method.routing_key,
        payload,
    )
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

"""Упражнение 3 (RabbitMQ): очередь, получающая ВСЕ логи одного сервиса.

См. постановку задачи в ../README.md, раздел "Упражнение 3".

Нужно забиндить очередь "auth_service_queue" к exchange "logs_topic" так,
чтобы она получала все сообщения от сервиса "auth", независимо от уровня
(error, warning, info - любой).

Запуск: python consumer_b.py
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

# TODO: подбери binding key так, чтобы очередь получала ВСЕ сообщения от
# service == "auth", независимо от level и от того, сколько слов идёт после
# service. Вспомни: "#" заменяет ноль или более слов.
BINDING_KEY = ""  # TODO


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
    # TODO: подтверди сообщение (manual ack).


def main() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    # TODO: объяви exchange (topic, durable) и очередь QUEUE_NAME (durable),
    # забинди очередь к exchange с BINDING_KEY.
    raise NotImplementedError("объяви exchange/очередь/биндинг для auth_service_queue")

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

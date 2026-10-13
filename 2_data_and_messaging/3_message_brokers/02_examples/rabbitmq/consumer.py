"""RabbitMQ consumer: wildcard-биндинг, manual ack и DLQ через нативный DLX.

Демонстрирует:
  - очередь "eu_orders_queue", привязанную к exchange "orders_topic"
    с binding key "orders.eu.*" (см. 01_theory/06_rabbitmq.md) -
    получит только события по EU-заказам, независимо от типа события;
  - manual ack: сообщение подтверждается только после успешной обработки;
  - retry с backoff (retry_with_backoff.py) перед тем, как сдаться;
  - dead-lettering: после исчерпания попыток сообщение nack'ается
    с requeue=False, и благодаря x-dead-letter-exchange, настроенному на
    очереди, RabbitMQ САМ пересылает его в DLQ - без единой строчки кода,
    отвечающей за "переложить сообщение в другую очередь".

Запуск (стенд из docker-compose.yml должен быть поднят; сначала запустить
rabbitmq/producer.py, чтобы в очереди появились сообщения):
    python rabbitmq/consumer.py
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

sys.path.append(str(Path(__file__).resolve().parent.parent))
from retry_with_backoff import RetryExhaustedError, retry_with_backoff  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("rabbitmq-consumer")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

MAIN_EXCHANGE = "orders_topic"
MAIN_QUEUE = "eu_orders_queue"
MAIN_BINDING_KEY = "orders.eu.*"  # * = ровно одно слово: eu.created, eu.shipped, ...

DLX_EXCHANGE = "orders_dlx"
DLQ_QUEUE = "eu_orders_dlq"


def declare_topology(channel: BlockingChannel) -> None:
    """Объявляет основную очередь + DLX/DLQ. Идемпотентно: можно вызывать сколько
    угодно раз, RabbitMQ не пересоздаёт уже существующие сущности с теми же
    параметрами."""

    # --- Dead-letter exchange и сама DLQ, куда будут падать "мёртвые" сообщения ---
    channel.exchange_declare(exchange=DLX_EXCHANGE, exchange_type="fanout", durable=True)
    channel.queue_declare(queue=DLQ_QUEUE, durable=True)
    channel.queue_bind(queue=DLQ_QUEUE, exchange=DLX_EXCHANGE)

    # --- Основной exchange для бизнес-событий заказов ---
    channel.exchange_declare(exchange=MAIN_EXCHANGE, exchange_type="topic", durable=True)

    # --- Основная очередь: подписана на срез "все EU-события" и настроена
    # так, что nack(requeue=False) уводит сообщение в DLX автоматически.
    channel.queue_declare(
        queue=MAIN_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DLX_EXCHANGE,
            # routing key в DLX не задаём - DLQ здесь одна и exchange fanout,
            # поэтому маршрутизация тривиальна.
        },
    )
    channel.queue_bind(queue=MAIN_QUEUE, exchange=MAIN_EXCHANGE, routing_key=MAIN_BINDING_KEY)


@retry_with_backoff(max_attempts=3, base_delay=1.0, max_delay=5.0)
def process_order(payload: dict) -> None:
    """Имитация обработки события заказа. "Плохое" сообщение (без поля amount)
    систематически падает - на нём и демонстрируется путь в DLQ."""
    if "amount" not in payload:
        raise ValueError(f"сообщение без обязательного поля 'amount': {payload}")

    logger.info(
        "обработано: order_id=%s country=%s event=%s amount=%s",
        payload["order_id"],
        payload["country"],
        payload["event"],
        payload["amount"],
    )


def on_message(
    channel: BlockingChannel,
    method: Basic.Deliver,
    _properties: BasicProperties,
    body: bytes,
) -> None:
    payload = json.loads(body.decode("utf-8"))
    logger.info("получено: routing_key=%s payload=%s", method.routing_key, payload)

    try:
        process_order(payload)
    except RetryExhaustedError as exc:
        # Все попытки провалились - подтверждать нельзя (сообщение не обработано),
        # но и возвращать в очередь на повторную попытку бессмысленно (ошибка
        # систематическая, не временная). requeue=False + настроенный на очереди
        # x-dead-letter-exchange -> RabbitMQ сам переложит сообщение в DLQ.
        logger.error(
            "сообщение уходит в DLQ после исчерпания попыток: %s", exc
        )
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    # Подтверждаем только после гарантированно успешной обработки.
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    declare_topology(channel)

    # prefetch_count=1: не забирать следующее сообщение, пока текущее не
    # подтверждено (ack/nack) - иначе один медленный consumer заберёт себе
    # весь бэклог, а остальные consumer'ы будут простаивать.
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MAIN_QUEUE, on_message_callback=on_message)

    logger.info("ожидание сообщений в очереди %s (Ctrl+C для выхода)", MAIN_QUEUE)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()

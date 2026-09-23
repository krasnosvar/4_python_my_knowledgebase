"""Упражнение 4 (RabbitMQ) - решение: полный цикл DLQ с retry-with-backoff.

Почему такая топология (см. 01_theory/README.md, раздел 4):
  - payments_queue настроена с x-dead-letter-exchange=payments_dlx - это
    единственное, что нужно RabbitMQ, чтобы САМОСТОЯТЕЛЬНО переложить
    сообщение в DLQ при nack(requeue=False). Никакого отдельного кода
    "скопировать сообщение в другую очередь" не требуется - в этом и разница
    с DLQ-паттерном в Kafka, где такое перекладывание пишется руками.
  - retry_with_backoff даёт обработчику несколько попыток с растущей паузой
    перед тем, как сдаться - это отличает "решил не обрабатывать после
    честной попытки разобраться" от "сдался при первой же ошибке", что было
    бы избыточно строго для потенциально временных сбоев (даже при том, что
    в данном конкретном упражнении сбой на payment_id=pay-POISON
    систематический и retry не помогает - в реальности отрицательный amount
    и временная недоступность внешнего сервиса неотличимы для decorator'а,
    поэтому обработчик всегда даёт несколько попыток на всякий случай).
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

sys.path.append(str(Path(__file__).resolve().parents[2] / "02_examples"))
from retry_with_backoff import RetryExhaustedError, retry_with_backoff  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex4-consumer")

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

MAIN_EXCHANGE = "payments_topic"
MAIN_QUEUE = "payments_queue"
ROUTING_KEY = "payments.charge"

DLX_EXCHANGE = "payments_dlx"
DLQ_QUEUE = "payments_dlq"


def declare_topology(channel: BlockingChannel) -> None:
    # DLX + DLQ: единственная очередь-приёмник "мёртвых" сообщений.
    channel.exchange_declare(exchange=DLX_EXCHANGE, exchange_type="fanout", durable=True)
    channel.queue_declare(queue=DLQ_QUEUE, durable=True)
    channel.queue_bind(queue=DLQ_QUEUE, exchange=DLX_EXCHANGE)

    # Основной exchange + очередь, с указанием, куда переслать мёртвые сообщения.
    channel.exchange_declare(exchange=MAIN_EXCHANGE, exchange_type="direct", durable=True)
    channel.queue_declare(
        queue=MAIN_QUEUE,
        durable=True,
        arguments={"x-dead-letter-exchange": DLX_EXCHANGE},
    )
    channel.queue_bind(queue=MAIN_QUEUE, exchange=MAIN_EXCHANGE, routing_key=ROUTING_KEY)


@retry_with_backoff(max_attempts=3, base_delay=1.0, max_delay=5.0)
def process_payment(payload: dict) -> None:
    if payload["amount"] < 0:
        raise ValueError(f"невалидная сумма платежа: {payload['amount']}")
    logger.info(
        "платёж обработан: payment_id=%s amount=%s",
        payload["payment_id"],
        payload["amount"],
    )


def on_message(
    channel: BlockingChannel,
    method: Basic.Deliver,
    _properties: BasicProperties,
    body: bytes,
) -> None:
    payload = json.loads(body.decode("utf-8"))
    logger.info("получено: %s", payload)

    try:
        process_payment(payload)
    except RetryExhaustedError as exc:
        logger.error(
            "payment_id=%s уходит в DLQ после исчерпания попыток: %s",
            payload.get("payment_id"),
            exc,
        )
        # requeue=False + x-dead-letter-exchange на очереди -> RabbitMQ сам
        # переложит сообщение в payments_dlq, без единой строчки кода
        # "переслать сообщение вручную".
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    declare_topology(channel)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MAIN_QUEUE, on_message_callback=on_message)

    logger.info("ожидание сообщений в %s (Ctrl+C для выхода)", MAIN_QUEUE)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()

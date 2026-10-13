# Брокеры сообщений: Kafka, RabbitMQ, DLQ и retry

Уроки читаются по порядку:

1. [01_why_message_brokers.md](./01_why_message_brokers.md) — зачем вообще
   нужен брокер вместо прямых вызовов между сервисами.
2. [02_kafka_partitions.md](./02_kafka_partitions.md) — Kafka как лог
   событий, что такое брокер в Kafka, партиции и порядок сообщений.
3. [03_kafka_consumer_groups.md](./03_kafka_consumer_groups.md) —
   consumer-группы и распределение партиций между consumer'ами.
4. [04_kafka_offsets.md](./04_kafka_offsets.md) — офсеты и коммит
   прогресса чтения.
5. [05_kafka_delivery_guarantees.md](./05_kafka_delivery_guarantees.md) —
   at-most-once, at-least-once, exactly-once.
6. [06_rabbitmq.md](./06_rabbitmq.md) — exchange и его типы, очереди и
   биндинги, ack/nack, routing key.
7. [07_dlq_and_retry.md](./07_dlq_and_retry.md) — Dead Letter Queue и retry
   с exponential backoff в Kafka и RabbitMQ.
8. [08_use_cases.md](./08_use_cases.md) — типовые сценарии применения.
9. [09_kafka_vs_rabbitmq.md](./09_kafka_vs_rabbitmq.md) — сравнение и выбор.

Как проходить всю тему (стенд, примеры, упражнения) — в
[README темы](../README.md).

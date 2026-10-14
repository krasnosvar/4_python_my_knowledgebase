# Тема 3. Брокеры сообщений: Kafka и RabbitMQ

## Зачем эта тема

Когда сервисов несколько, самый простой способ связать их — прямой
HTTP-вызов: сервис A вызывает сервис B и ждёт ответа. Это ломается, как
только B тормозит, падает или не успевает за всплеском нагрузки: A тоже
начинает тормозить и падать. Брокер сообщений ставится между ними: A
кладёт сообщение и идёт дальше, B забирает сообщения в своём темпе, а
бэклог переживает падения обеих сторон.

Взамен появляются новые вопросы: что будет, если consumer упал посреди
обработки, если сообщение обработалось дважды, если оно не обрабатывается
никогда. Тема разбирает, как на них отвечают Kafka и RabbitMQ. После неё ты
сможешь выбрать брокер под задачу, сохранить порядок сообщений, где он
нужен, правильно подтверждать обработку и построить retry с Dead Letter
Queue.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — Kafka и RabbitMQ, гарантии доставки, DLQ/retry и «что выбрать» в таблицах.

## Что нужно знать заранее

`asyncio` из
[1_python/6_concurrency](../../1_python/6_concurrency/) (Kafka-примеры
асинхронные), Docker на уровне
[0_tooling_and_workflow](../../0_tooling_and_workflow/) и виртуальное
окружение из
[other/01_environments_and_packaging](../../other/01_environments_and_packaging/).

## Структура темы

- **[01_theory/](./01_theory/README.md)** — 9 уроков по порядку:
  1. [Зачем вообще нужны брокеры сообщений](./01_theory/01_why_message_brokers.md)
  2. [Kafka: партиции](./01_theory/02_kafka_partitions.md)
  3. [Kafka: consumer-группы](./01_theory/03_kafka_consumer_groups.md)
  4. [Kafka: офсеты](./01_theory/04_kafka_offsets.md)
  5. [Kafka: гарантии доставки](./01_theory/05_kafka_delivery_guarantees.md)
  6. [RabbitMQ](./01_theory/06_rabbitmq.md)
  7. [Dead Letter Queue и retry с backoff](./01_theory/07_dlq_and_retry.md)
  8. [Сценарии применения](./01_theory/08_use_cases.md)
  9. [Kafka vs RabbitMQ](./01_theory/09_kafka_vs_rabbitmq.md)
- **[02_examples/](./02_examples/README.md)** — стенд Kafka (KRaft) + Kafka
  UI + RabbitMQ на Docker Compose, producer/consumer для Kafka (`aiokafka`)
  и RabbitMQ (`pika`), пример retry с backoff.
- **[03_exercises/](./03_exercises/README.md)** — 4 упражнения:
  партиционирование и порядок сообщений, ручной commit offset'а, topic
  exchange с двумя очередями, DLQ с retry-with-backoff.
- **[04_exercises_answers/](./04_exercises_answers/)** — готовые решения в
  тех же папках.

## Как проходить тему

1. Прочитайте уроки `01_theory/` по порядку от `01` до `09`.
2. Поднимите стенд (подробно — в
   [02_examples/README.md](./02_examples/README.md)):

   ```bash
   cd 02_examples
   docker compose up -d
   docker compose ps   # дождаться healthy у kafka и rabbitmq
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Запустите producer и consumer из примеров по инструкции в
   `02_examples/README.md`.
4. Выполните упражнения из `03_exercises/` и только потом сверьтесь с
   `04_exercises_answers/`.
5. Остановить стенд: `docker compose down`, с удалением топиков и очередей —
   `docker compose down -v`.

## Когда двигаться дальше

Когда ты можешь объяснить, как ключ сообщения связан с порядком в Kafka,
когда коммитить offset, чем topic exchange отличается от direct и как
устроен retry через DLQ — раздел пройден. Дальше —
[3_web_frameworks](../../3_web_frameworks/): там фоновые задачи (Celery)
используют брокер уже как часть веб-сервиса.

[К оглавлению раздела](../README.md).

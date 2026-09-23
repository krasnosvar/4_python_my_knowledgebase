# Данные и обмен сообщениями

Этот раздел — учебный набор по хранилищам данных и брокерам сообщений в контексте Python:
теория, учебные стенды на Docker Compose, практика на Python/SQL и упражнения с готовыми разборами.

## Структура

Каждый подраздел устроен одинаково:
- `01_theory/` — теория: как это устроено и почему, а не просто список команд
- `02_examples/` — рабочие примеры на Python (плюс `docker-compose.yml`, если нужен поднятый сервис)
- `03_exercises/` — практические задания (TODO), от простого к сложному
- `04_exercises_answers/` — полные рабочие решения к заданиям из `03_exercises/`

Подразделы:

- `1_sql_relational_databases/` — реляционная модель, транзакции и ACID, индексы и `EXPLAIN ANALYZE`,
  проблема N+1, блокировки, репликация, WAL; примеры на `psycopg` и SQLAlchemy поверх PostgreSQL
- `2_redis/` — Redis как кеш: структуры данных, TTL и вытеснение, паттерны кеширования, инвалидация,
  rate-limiting; примеры на `redis-py`
- `3_message_brokers/` — Kafka (партиции, consumer-группы, гарантии доставки) и RabbitMQ
  (exchange, ack/nack, routing key), Dead Letter Queue и retry с backoff; примеры на `aiokafka`/`kafka-python`
  и `pika`/`aio-pika`

## Как проходить

1) Открой `01_theory/` подраздела и прочитай теорию — там объясняется не только "что", но и "почему".
2) Подними стенд из `02_examples/` (`docker compose up -d`, затем `docker compose ps`) и прогони примеры.
3) Пройди задания из `03_exercises/` самостоятельно, помечая прогресс по TODO.
4) Сверься с `04_exercises_answers/` — но только после собственной попытки.

## Быстрые ссылки

- SQL / PostgreSQL: `1_sql_relational_databases/01_theory/README.md`
- Redis: `2_redis/01_theory/README.md`
- Брокеры сообщений (Kafka, RabbitMQ): `3_message_brokers/01_theory/README.md`

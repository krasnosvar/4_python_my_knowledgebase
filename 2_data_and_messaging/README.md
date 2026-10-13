# Данные и обмен сообщениями

Этот раздел — учебный набор по хранилищам данных и брокерам сообщений в
контексте Python: теория, учебные стенды на Docker Compose, практика на
Python/SQL и упражнения с готовыми разборами.

## Структура

Каждый подраздел устроен одинаково:

- `README.md` — зачем тема, что в ней и как её проходить;
- `01_theory/` — пронумерованные уроки: как это устроено и почему, а не
  просто список команд;
- `02_examples/` — рабочие примеры на Python (плюс `docker-compose.yml`, если
  нужен поднятый сервис);
- `03_exercises/` — практические задания (TODO), от простого к сложному;
- `04_exercises_answers/` — полные рабочие решения к заданиям из
  `03_exercises/`.

Подразделы:

- [1_sql_relational_databases](./1_sql_relational_databases/README.md) — SQL
  с нуля, реляционная модель, транзакции и ACID, индексы и
  `EXPLAIN ANALYZE`, ORM и проблема N+1, блокировки, репликация, CAP и
  eventual consistency, WAL; примеры на `psycopg` и SQLAlchemy поверх
  PostgreSQL.
- [2_redis](./2_redis/README.md) — Redis как кеш: структуры данных, TTL и
  вытеснение, паттерны кеширования, инвалидация, rate limiting; примеры на
  `redis-py`.
- [3_message_brokers](./3_message_brokers/README.md) — Kafka (партиции,
  consumer-группы, офсеты, гарантии доставки) и RabbitMQ (exchange,
  ack/nack, routing key), Dead Letter Queue и retry с backoff; примеры на
  `aiokafka` и `pika`.

## Как проходить

0) Подготовь окружение: примеры ставят зависимости через
   `pip install -r requirements.txt`, поэтому сначала нужно понимать, что
   такое виртуальное окружение (venv) и pip — это разобрано в
   [other/01_environments_and_packaging](../other/01_environments_and_packaging/).
   Стенды поднимаются через Docker Compose — основы в
   [0_tooling_and_workflow/02_docker_basics](../0_tooling_and_workflow/02_docker_basics/).
1) Проходи подразделы по порядку: SQL → Redis → брокеры. Начни с `README.md`
   подраздела, затем читай уроки `01_theory/` по порядку.
2) Подними стенд из `02_examples/` (`docker compose up -d`, затем
   `docker compose ps`) и прогони примеры.
3) Пройди задания из `03_exercises/` самостоятельно, помечая прогресс по TODO.
4) Сверься с `04_exercises_answers/` — но только после собственной попытки.

## Быстрые ссылки

- SQL / PostgreSQL:
  [1_sql_relational_databases/01_theory/](./1_sql_relational_databases/01_theory/README.md)
- Redis: [2_redis/01_theory/](./2_redis/01_theory/README.md)
- Брокеры сообщений (Kafka, RabbitMQ):
  [3_message_brokers/01_theory/](./3_message_brokers/01_theory/README.md)

# Тема 2. Redis как кеш

## Зачем эта тема

Реляционная база надёжна, но каждое обращение к ней стоит миллисекунды, а
на популярной странице таких обращений тысячи в секунду. Redis хранит данные
в оперативной памяти и отвечает в десятки раз быстрее, поэтому его ставят
перед базой как кеш: частые чтения обслуживает Redis, а база получает только
промахи.

Кеш сам по себе приносит новые проблемы: устаревшие данные, гонки между
обновлением базы и кеша, лавина запросов в базу, когда популярный ключ
истёк. Тема разбирает и сам Redis, и эти проблемы. После неё ты сможешь
выбрать структуру данных Redis под задачу, реализовать cache-aside с TTL,
продумать инвалидацию и сделать rate limiter.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — команды структур данных, eviction-политики, паттерны кеширования, rate limiting в таблицах.

## Что нужно знать заранее

Тема
[1_sql_relational_databases](../1_sql_relational_databases/README.md) (Redis
почти всегда стоит рядом с реляционной базой), Docker на уровне
[0_tooling_and_workflow](../../0_tooling_and_workflow/) и виртуальное
окружение из
[other/01_environments_and_packaging](../../other/01_environments_and_packaging/).

## Структура темы

- **[01_theory/](./01_theory/README.md)** — 8 уроков по порядку:
  1. [Что такое Redis и почему он быстрый](./01_theory/01_what_is_redis.md)
  2. [Основные структуры данных](./01_theory/02_data_structures.md)
  3. [TTL: expiration и eviction](./01_theory/03_ttl_expiration_eviction.md)
  4. [Паттерны кеширования](./01_theory/04_caching_patterns.md)
  5. [Инвалидация кеша](./01_theory/05_cache_invalidation.md)
  6. [Redis для rate limiting](./01_theory/06_rate_limiting.md)
  7. [Redis как простая очередь](./01_theory/07_redis_as_queue.md)
  8. [Pub/Sub — коротко](./01_theory/08_pubsub.md)
- **[02_examples/](./02_examples/README.md)** — стенд Redis на Docker
  Compose и 4 скрипта на `redis-py`: структуры данных, TTL и вытеснение,
  cache-aside, rate limiting.
- **[03_exercises/](./03_exercises/README.md)** — задания с `TODO`:
  cache-aside обёртка, TTL-инвалидация, sliding window rate limiter, выбор
  структуры данных для «последних поисков».
- **[04_exercises_answers/](./04_exercises_answers/)** — готовые решения под
  теми же именами файлов.

## Как проходить тему

1. Прочитайте уроки `01_theory/` по порядку от `01` до `08`.
2. Поднимите стенд (подробно — в
   [02_examples/README.md](./02_examples/README.md)):

   ```bash
   cd 02_examples
   docker compose up -d
   docker compose ps   # дождаться healthy у redis
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Запустите примеры, например `python 03_cache_aside_pattern.py`.
4. Выполните задания из `03_exercises/` и только потом сверьтесь с
   `04_exercises_answers/`.
5. Остановить стенд: `docker compose down`, с удалением данных —
   `docker compose down -v`.

## Когда двигаться дальше

Когда ты можешь реализовать cache-aside с осмысленным TTL, объяснить, как
кеш устаревает и как его инвалидировать, и сделать rate limiter на Redis —
переходи к [3_message_brokers](../3_message_brokers/README.md): там сервисы
начинают обмениваться событиями асинхронно.

[К оглавлению раздела](../README.md).

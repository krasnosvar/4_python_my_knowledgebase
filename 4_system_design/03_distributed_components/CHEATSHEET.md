# Компоненты распределённых систем в Python — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/) и каноническом разделе
[DevOps System Design](../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/).
⚠️ — типичная ошибка в Python-проектах, которая дорого обходится.

## Пулы соединений к БД и PgBouncer в Python

Подробнее: [Пулы БД и брокеры сообщений в
Python](./01_theory/01_db_pools_and_messaging_in_python.md)

| Параметр / Задача | Настройка в Python (`SQLAlchemy` / `Celery`) |
| :--- | :--- |
| Число коннектов от сервиса к БД | `PODS × WORKERS_PER_POD × (pool_size + max_overflow)` |
| Работа `asyncpg` через `PgBouncer` (`pool_mode = transaction`) | `connect_args={"statement_cache_size": 0}` в `create_async_engine` |
| Защита от мёртвых TCP-сокетов в пуле | `pool_pre_ping=True`, `pool_recycle=1800`, `pool_timeout=3.0` |
| Воркеры `Celery` с `prefork` | Использовать `NullPool` (перед PgBouncer) или создавать `Engine` в `worker_process_init` |

## Асинхронные сообщения: Outbox, Inbox и Backpressure

Подробнее: [Пулы БД и брокеры сообщений в
Python](./01_theory/01_db_pools_and_messaging_in_python.md)

| Паттерн | Реализация в Python |
| :--- | :--- |
| **Transactional Outbox** (запись) | `session.add(entity)` + `session.add(OutboxEvent(...))` в одном `await session.commit()` |
| **Outbox Relay** (отправка пачками) | `select(OutboxEvent).where(...).limit(100).with_for_update(skip_locked=True)` |
| **Idempotent Consumer** (Inbox) | `insert(ProcessedMessage).values(...).on_conflict_do_nothing()` в одной транзакции с бизнес-логикой |
| **Backpressure в `asyncio`** | Ограничение параллелизма через `asyncio.Semaphore(N)` или `asyncio.Queue(maxsize=N)` |

## Отказоустойчивость, Health Checks и Graceful Shutdown

Подробнее: [Отказоустойчивость и Graceful Shutdown в
Python](./01_theory/02_resilience_and_graceful_shutdown_in_python.md)

| Механизм защиты | Инструмент и синтаксис в Python |
| :--- | :--- |
| **Таймаут на запрос и блок** | `httpx.Timeout(connect=0.5, read=1.5, ...)` + `async with asyncio.timeout(2.0):` (3.11+) |
| **Retries с Full Jitter** | `@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=0.1, max=2.0))` (`tenacity`) |
| **Liveness Probe (`/healthz`)** | Быстрый ответ `{"status": "alive"}` **БЕЗ** походов в БД/Redis (иначе каскадный рестарт подов) |
| **Readiness Probe (`/readyz`)** | Проверка `SELECT 1` в БД с коротким таймаутом; при сбое — `503` (убирает под из балансировки) |
| **Graceful Shutdown (ASGI)** | `preStop: sleep 5` в K8s → `--timeout-graceful-shutdown 15` в Uvicorn → закрытие пулов после `yield` в `lifespan` |
| **Graceful Shutdown (Celery)** | `task_acks_late=True`, `task_reject_on_worker_lost=True`, `worker_prefetch_multiplier=1` |

## Типичные ошибки в Python

- ⚠️ Оставлять дефолтный `pool_size=5, max_overflow=10` при десятках подов и
  нескольких воркерах Gunicorn без `PgBouncer` → исчерпание `max_connections` в
  PostgreSQL.
- ⚠️ Делать `await kafka_producer.send()` сразу после `await session.commit()`
  без таблицы Outbox → потеря события при падении процесса между двумя строками.
- ⚠️ Вызывать `requests.get(url)` без `timeout=` → вечное зависание потока при
  потере пакетов.
- ⚠️ Проверять БД или внешний сервис внутри `/healthz` (`livenessProbe`) →
  одновременный рестарт всех подов при кратковременной просадке БД.
- ⚠️ Создавать задачи через `asyncio.create_task()` на каждое сообщение из
  очереди без семафора → `OOMKilled` при всплеске трафика.

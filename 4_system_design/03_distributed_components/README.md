# Тема 03. Компоненты распределённой системы в Python (Distributed Components)

## О чём эта тема (краткий контекст)

Когда система состоит из нескольких сервисов, баз данных и фоновых воркеров,
ключевой задачей становится надёжное соединение этих узлов между собой:
управление пулами соединений к БД, гарантированная асинхронная доставка событий
через брокеры сообщений (Transactional Outbox, идемпотентные консьюмеры,
backpressure), балансировка нагрузки, проверки здоровья (Liveness/Readiness),
защита сетевых вызовов (Timeouts, Retries с Jitter, Circuit Breaker) и
корректная остановка процессов при деплое (Graceful Shutdown).

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Репликация, шардирование, CAP/PACELC и распределённые данные](../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/01_data_replication_sharding_and_cap.md)
> - [Очереди, брокеры сообщений, Outbox, идемпотентность и Backpressure](../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/02_messaging_and_async_patterns.md)
> - [Балансировка нагрузки, Health Checks и паттерны отказоустойчивости](../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/03_load_balancing_and_resilience_patterns.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки).

## Зачем этот раздел

Здесь вы разберёте критические узлы распределённых систем в Python: почему
многопроцессная модель Gunicorn/Celery умножает пулы `SQLAlchemy` и кладёт
PostgreSQL без `PgBouncer` (и как подружить `asyncpg` с `transaction` pooling),
как написать `Transactional Outbox` на `FOR UPDATE SKIP LOCKED` и
идемпотентный консьюмер с `asyncio.Semaphore`, как настроить `asyncio.timeout`
+ `tenacity` с экспоненциальным Jitter, разделить `/healthz` и `/readyz` в
FastAPI и реализовать безупречный Graceful Shutdown при `SIGTERM`.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — формула пулов
соединений, `asyncpg` + `PgBouncer`, `Outbox`, `tenacity`, `/healthz` vs
`/readyz` и Graceful Shutdown в Uvicorn/Celery.

## Что нужно знать заранее

- Темы [01_architecture_styles](../01_architecture_styles/) и
  [02_performance_and_scaling](../02_performance_and_scaling/).
- Работа с транзакциями SQL и брокерами сообщений из
  [2_data_and_messaging](../../2_data_and_messaging/), основы FastAPI и Celery
  из [3_web_frameworks](../../3_web_frameworks/).

## Структура раздела

- **[01_theory/](./01_theory/)** — теория с фокусом на специфику Python:
  - [01_db_pools_and_messaging_in_python.md (урок
    01)](./01_theory/01_db_pools_and_messaging_in_python.md)
    — ловушка умножения пулов соединений (`QueuePool` × число воркеров),
    настройка `PgBouncer` (`statement_cache_size=0` в `asyncpg`), реализация
    `Transactional Outbox` (`FOR UPDATE SKIP LOCKED`), идемпотентных
    консьюмеров и Backpressure на `asyncio.Semaphore`.
  - [02_resilience_and_graceful_shutdown_in_python.md (урок
    02)](./01_theory/02_resilience_and_graceful_shutdown_in_python.md)
    — двухуровневые таймауты (`asyncio.timeout` + `httpx.Timeout`), ретраи с
    Full Jitter (`tenacity`), Circuit Breaker, реализация `/healthz` (Liveness)
    и `/readyz` (Readiness) в FastAPI и Graceful Shutdown в
    Uvicorn/Gunicorn/Celery по сигналу `SIGTERM`.
- **[02_examples/](./02_examples/)** — runnable-примеры на чистом Python:
  - [01_load_balancer_algorithms
    (пример)](./02_examples/01_load_balancer_algorithms/main.py)
    — сравнение Round Robin и Least Connections на неоднородной нагрузке.
  - [02_service_registry_health_checks
    (пример)](./02_examples/02_service_registry_health_checks/main.py)
    — реестр сервисов с heartbeat: исключение зависшего инстанса и возврат
    после восстановления.
  - [03_api_gateway_routing](./02_examples/03_api_gateway_routing/main.py) —
    минимальный API Gateway: маршрутизация, аутентификация и rate limiting на
    периметре.
- **[03_exercises/](./03_exercises/)** — сценарии системного дизайна для
  письменного разбора:
  - [01_design_the_gateway](./03_exercises/01_design_the_gateway.md) —
    определить границы ответственности API Gateway и BFF.
  - [02_pick_the_database](./03_exercises/02_pick_the_database.md) — подобрать
    хранилища под сервисы с разным профилем нагрузки (polyglot persistence).
  - [03_load_balancing_strategy](./03_exercises/03_load_balancing_strategy.md)
    — выбрать алгоритм балансировки и схему хранения сессий WebSocket.
  - [04_service_discovery_failure
    (задача)](./03_exercises/04_service_discovery_failure.md)
    — разобрать реальный продакшн-инцидент с Liveness/Readiness и таймаутами.
- **[04_exercises_answers/](./04_exercises_answers/)** — разобранные
  рассуждения по тем же сценариям.

## Как проходить

1. Изучите базовую теорию в каноническом разделе DevOps (по ссылкам в начале
   уроков) и прочитайте уроки в [01_theory/](./01_theory/).
2. Запустите и изучите примеры из `02_examples/`:
   ```bash
   python3 ./02_examples/01_load_balancer_algorithms/main.py
   python3 ./02_examples/02_service_registry_health_checks/main.py
   python3 ./02_examples/03_api_gateway_routing/main.py
   ```
3. Проработайте сценарии в [03_exercises/](./03_exercises/) письменно, прежде
   чем сверяться с [04_exercises_answers/](./04_exercises_answers/).

## Когда двигаться дальше

Когда вы умеете рассчитывать размер пулов соединений Python-воркеров, писать
Transactional Outbox и защищённые сетевые вызовы с `tenacity`, а также чётко
различаете Liveness, Readiness и этапы Graceful Shutdown — переходите к
[04_case_studies](../04_case_studies/).

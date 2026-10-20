# Раздел 4. Проектирование систем в Python (System Design in Python)

## О чём эта тема (краткий контекст)

System Design — дисциплина о проектировании масштабируемых, отказоустойчивых
и поддерживаемых систем. Базовые архитектурные компромиссы (монолит против
микросервисов, кэширование, шардирование, брокеры сообщений, API Gateway)
одинаковы в любом языке, но в Python они преломляются через специфику
CPython (GIL, стоимость памяти PyObject, pre-fork воркеры Gunicorn/Uvicorn,
кооперативная многозадачность `asyncio`). В этом разделе мы разбираем, как
проектировать реальные сервисы на Python-стеке с учётом этих ограничений.

> **Фундаментальная теория System Design:** Полный язык-агностичный курс по
> архитектуре, распределённым системам, консенсусу, репликации и разбору
> кейсов находится в
> [5_devops_sre_knowledgebase → 14_system_design](../../5_devops_sre_knowledgebase/14_system_design/).
> Здесь мы фокусируемся на специфике реализации и эксплуатации в Python.

## Зачем этот раздел

Этот раздел связывает знание синтаксиса, фреймворков и баз данных в умение
проектировать Python-бэкенд целиком: выбрать между модульным монолитом на
Django и микросервисами на FastAPI, рассчитать число воркеров Gunicorn/Uvicorn
под CPU-bound и I/O-bound нагрузку, настроить пулы соединений SQLAlchemy и
защиту от cache stampede в `asyncio`, спроектировать идемпотентный платёжный
сервис и конвейер обработки медиафайлов.

## Что нужно знать заранее

- Уверенный Python на уровне [1_python](../1_python/), особенно
  [5_concurrency](../1_python/5_concurrency/) (GIL, потоки, процессы,
  `asyncio`) — примеры написаны на чистом Python 3.12+ без внешних
  зависимостей.
- Желательно пройти [2_data_and_messaging](../2_data_and_messaging/) (SQL,
  Redis, брокеры) и [3_web_frameworks](../3_web_frameworks/) (FastAPI,
  Django, Celery): архитектурные решения опираются на эти инструменты.

## Эталон структуры

Каждая тема наполняется по единому стандарту базы:

- `01_theory/` — теория с кратким контекстом, ссылкой на фундаментальную
  базу и глубоким разбором специфики Python (CPython, ASGI/WSGI, ORM,
  `asyncio`);
- `02_examples/` — самодостаточные рабочие примеры на чистом Python;
- `03_exercises/` — архитектурные сценарии и задачи на расчёт/проектирование;
- `04_exercises_answers/` — эталонные инженерные разборы для самопроверки;
- `CHEATSHEET.md` — компактная шпаргалка с таблицами решений и кодом.

## Темы

1. [01_architecture_styles](01_architecture_styles/) — архитектурные стили в
   Python: модульный монолит (Django/FastAPI, `import-linter`) против
   микросервисов, Clean Architecture и DDD (`Protocol`, `dataclasses`,
   Unit of Work со SQLAlchemy), контракты API (REST/Pydantic v2, `grpc.aio`,
   GraphQL Strawberry и DataLoader).
2. [02_performance_and_scaling](02_performance_and_scaling/) —
   производительность и масштабирование в Python: GIL (PEP 703), блокировка
   event loop, расчёт воркеров Gunicorn/Uvicorn, профилирование (`py-spy`,
   `Memray`), in-memory и распределённое кэширование (`lru_cache`, утечки
   памяти, Singleflight на `asyncio.Lock`), шардирование и `RoutingSession`.
3. [03_distributed_components](03_distributed_components/) — компоненты
   распределённой системы в Python: пулы соединений SQLAlchemy + PgBouncer,
   Transactional Outbox, идемпотентные воркеры Celery/Kafka, каскадные
   таймауты в `httpx`, ретраи с джиттером, Circuit Breaker и Graceful
   Shutdown в Kubernetes (`SIGTERM`, `lifespan`).
4. [04_case_studies](04_case_studies/) — сквозные кейсы на Python: система
   денежных переводов (`Decimal`, `SELECT FOR UPDATE` в порядке ID, Double
   Entry Ledger, Outbox) и галерея изображений (Presigned S3 URL, проверка
   magic bytes, защита от Decompression Bomb в Pillow, фоновый ресайз в
   Celery, cursor pagination).

## Как проходить

- Идти последовательно от `01_architecture_styles` к `04_case_studies`:
  сначала границы модулей и сервисов → затем поведение Python-рантайма под
  нагрузкой, кэширование и шардирование → затем надёжная интеграция БД,
  очередей и внешних API → и наконец сборка всех паттернов в сквозных кейсах.
- В каждой теме сначала прочитайте `01_theory/`, запустите скрипты из
  `02_examples/`, письменно решите задачи из `03_exercises/` и сверьтесь с
  `04_exercises_answers/`.

## Когда двигаться дальше

Когда вы можете по требованиям к продукту и профилю нагрузки обосновать выбор
архитектуры и модели воркеров в Python, рассчитать пулы соединений к БД,
объяснить защиту от гонок и повторной доставки сообщений, а ваши решения
кейсов в `04_case_studies` учитывают все граничные случаи рантайма и БД —
раздел освоен.

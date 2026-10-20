# Тема 01. Архитектурные стили в Python (Architecture Styles)

## О чём эта тема (краткий контекст)

Архитектура приложения и системы отвечает на два главных вопроса: как провести
границы между процессами и базами данных (монолит, модульный монолит или
микросервисы) и как организовать слои кода внутри каждого отдельного сервиса
(Layered, Hexagonal, Clean Architecture, DDD), а также по каким сетевым
протоколам (REST, gRPC, GraphQL) сервисы общаются между собой. Правильный
выбор архитектурного стиля позволяет маленькой команде быстро запускать
продукт без лишней инфраструктурной цены, а большой организации — независимо
релизить, тестировать и масштабировать десятки сервисов, не скатываясь в
«распределённый монолит».

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Системная архитектура: монолит и микросервисы](../../../5_devops_sre_knowledgebase/14_system_design/01_architecture_and_api_styles/01_theory/01_system_architecture_monolith_microservices.md)
> - [Архитектура внутри сервиса: Layered, Clean, Hexagonal и DDD](../../../5_devops_sre_knowledgebase/14_system_design/01_architecture_and_api_styles/01_theory/02_service_architecture_clean_ddd.md)
> - [Стили API (REST, gRPC, GraphQL), API Gateway и Service Discovery](../../../5_devops_sre_knowledgebase/14_system_design/01_architecture_and_api_styles/01_theory/03_api_styles_gateway_and_discovery.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки).

## Зачем этот раздел

Здесь вы научитесь приземлять архитектурные паттерны на реальный Python-стек:
строить модульный монолит с контролем импортов (`tach`, `import-linter`),
понимать разницу между синхронным WSGI (Gunicorn) и асинхронным ASGI (Uvicorn
+ `httpx.AsyncClient`) при межсервисных вызовах, применять Чистую архитектуру
(`@dataclass`, `typing.Protocol`, `Unit of Work` поверх `SQLAlchemy`) там, где
Active Record Django перестаёт справляться, и выбирать между FastAPI +
`orjson`, `grpc.aio` и `Strawberry` GraphQL.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — таблицы выбора
архитектуры, WSGI vs ASGI, Clean Architecture / UoW и сравнение REST / gRPC /
GraphQL в Python.

## Что нужно знать заранее

- Python и ООП на уровне [1_python](../../1_python/) (особенно датаклассы,
  протоколы и [SOLID в
  Python](../../1_python/3_oop/01_theory/08_solid_in_python.md)).
- Базовое представление об HTTP-сервисах, ORM и фоновых задачах (см.
  [2_data_and_messaging](../../2_data_and_messaging/) и
  [3_web_frameworks](../../3_web_frameworks/)).

## Структура раздела

- **[01_theory/](./01_theory/)** — теория с фокусом на специфику Python:
  - [01_monolith_and_microservices_in_python.md (урок
    01)](./01_theory/01_monolith_and_microservices_in_python.md)
    — модульный монолит в пакетах Python (`import-linter`, `tach`), ловушки
    Django apps, переход через Strangler Fig, WSGI vs ASGI при межсервисных
    вызовах (`httpx.AsyncClient`), вынос фоновых задач в Celery/RQ/Dramatiq.
  - [02_clean_architecture_and_ddd_in_python.md (урок
    02)](./01_theory/02_clean_architecture_and_ddd_in_python.md)
    — Active Record в Django против Clean Architecture + DDD в Python:
    доменные сущности и неизменяемые `@dataclass(frozen=True)`, порты на
    `typing.Protocol`, `Unit of Work` поверх `AsyncSession` SQLAlchemy и DI в
    FastAPI.
  - [03_api_styles_and_contracts_in_python.md (урок
    03)](./01_theory/03_api_styles_and_contracts_in_python.md)
    — REST (FastAPI + Pydantic v2 + `orjson`), gRPC (`grpc.aio`, Protobuf,
    `mypy-protobuf`), GraphQL (`Strawberry` + `DataLoader` против проблемы
    N+1) и место BFF в Python.
- **[02_examples/](./02_examples/)** — runnable-примеры на чистом Python (без
  внешних зависимостей, детерминированные, завершаются сами):
  - [01_strangler_fig_router](./02_examples/01_strangler_fig_router/main.py) —
    маршрутизатор Strangler Fig: таблица префиксов путей и три этапа миграции
    трафика из монолита в новые сервисы без изменения клиента.
  - [02_distributed_monolith_chain
    (пример)](./02_examples/02_distributed_monolith_chain/main.py)
    — синхронная цепочка вызовов `A → B → C → D` без таймаутов: отказ нижнего
    звена рушит весь запрос.
- **[03_exercises/](./03_exercises/)** — сценарии системного дизайна для
  письменного разбора:
  - [01_startup_monolith_or_microservices
    (задача)](./03_exercises/01_startup_monolith_or_microservices.md)
    — стартап выбирает архитектуру для нового продукта на Python.
  - [02_spot_the_distributed_monolith
    (задача)](./03_exercises/02_spot_the_distributed_monolith.md)
    — распознать признаки распределённого монолита и исправить их.
  - [03_migration_plan](./03_exercises/03_migration_plan.md) — составить план
    инкрементальной миграции Django-монолита на сервисы.
  - [04_team_topology_fit](./03_exercises/04_team_topology_fit.md) — подобрать
    архитектуру под структуру команд (закон Конвея).
- **[04_exercises_answers/](./04_exercises_answers/)** — разобранные
  рассуждения по тем же сценариям для самопроверки.

## Как проходить

1. Ознакомьтесь с базовой теорией в каноническом разделе DevOps (по ссылкам в
   начале каждого урока) и прочитайте уроки в [01_theory/](./01_theory/).
2. Запустите и изучите примеры из `02_examples/`:
   ```bash
   python3 ./02_examples/01_strangler_fig_router/main.py
   python3 ./02_examples/02_distributed_monolith_chain/main.py
   ```
3. Проработайте сценарии в [03_exercises/](./03_exercises/) письменно, прежде
   чем открывать ответы.
4. Сверьте свой ход мыслей с [04_exercises_answers/](./04_exercises_answers/).

## Когда двигаться дальше

Когда вы можете обосновать выбор между модульным монолитом и микросервисами на
Python, спроектировать слои сервиса с помощью `Protocol` и `Unit of Work`, а
также выбрать между REST, gRPC и GraphQL под профиль нагрузки — переходите к
[02_performance_and_scaling](../02_performance_and_scaling/).

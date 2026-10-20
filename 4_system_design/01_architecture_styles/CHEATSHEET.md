# Архитектурные стили в Python — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/) и каноническом разделе
[DevOps System Design](../../../5_devops_sre_knowledgebase/14_system_design/01_architecture_and_api_styles/).
⚠️ — типичная ошибка в Python-проектах, которая дорого обходится.

## Модульный монолит vs Микросервисы в Python

Подробнее: [Монолит и микросервисы в
Python](./01_theory/01_monolith_and_microservices_in_python.md)

| Задача / Проблема | Решение в экосистеме Python |
| :--- | :--- |
| Запретить импорт чужих приватных модулей в монолите | `import-linter` (контракты в `pyproject.toml`) или `tach` (Rust AST-чекер) в CI |
| Изолировать Django-приложения (`apps`) | Не делать `ForeignKey` между доменами (хранить `UUID`), избегать междоменных сигналов `post_save` |
| Вынести тяжёлые/фоновые задачи без распила на микросервисы | Отдельные воркеры **Celery / Dramatiq / RQ / Taskiq** из того же Docker-образа |
| Сетевые межсервисные вызовы без блокировки потоков | Переход с WSGI (`gunicorn` sync) на ASGI (`uvicorn`) + единый пул `httpx.AsyncClient` в `lifespan` |
| Постепенный вынос сервиса из монолита | **Strangler Fig** (прокси перед монолитом) + миграция БД по схеме **Expand → Migrate → Contract** |

## Чистая архитектура и тактический DDD в Python

Подробнее: [Clean Architecture и DDD в
Python](./01_theory/02_clean_architecture_and_ddd_in_python.md)

| Строительный блок | Идиоматичная реализация в Python |
| :--- | :--- |
| **Value Object** (неизменяемый объект-значение) | `@dataclass(frozen=True, slots=True)` + валидация инвариантов в `__post_init__` |
| **Entity** (доменная сущность) | Обычный `@dataclass` с бизнес-методами, без импортов `sqlalchemy` или `pydantic` |
| **Port** (интерфейс репозитория / внешнего клиента) | `typing.Protocol` в слое Domain / Application (структурная типизация для `mypy`/`pyright`) |
| **Adapter** (реализация хранилища) | Класс `SqlAlchemyOrderRepository`, конвертирующий ORM-модели в доменные `@dataclass` |
| **Unit of Work (UoW)** | Асинхронный контекстный менеджер (`__aenter__` / `__aexit__`), оборачивающий `AsyncSession` |
| **Dependency Injection** | Явные конструкторы + сборка через `FastAPI Depends()` или DI-контейнер (`dishka`) |

| Профиль сервиса | Что выбрать |
| :--- | :--- |
| Простой CRUD, админка, прототип | Django Active Record («толстые модели») или FastAPI + прямой вызов SQLAlchemy в сервисе |
| Сложная бизнес-логика, биллинг, оркестрация заказов | Clean / Hexagonal Architecture: Domain (`@dataclass`) + `Protocol` + `UnitOfWork` |

## Стили API и контракты в Python

Подробнее: [Контракты API в
Python](./01_theory/03_api_styles_and_contracts_in_python.md)

| Протокол | Стек в Python | Когда применять и ключевые нюансы |
| :--- | :--- | :--- |
| **REST + JSON** | `FastAPI` + `Pydantic v2` + `ORJSONResponse` / `msgspec` | Публичные API, веб/мобайл. Использовать `model_validate_json()` (Rust-ядро) и `orjson` |
| **gRPC** | `grpcio` (`grpc.aio`) + `protobuf` + `mypy-protobuf` | Внутренние вызовы с высокой частотой, стриминг, строгие `.proto` контракты между языками |
| **GraphQL** | `Strawberry` + `DataLoader` (на каждый запрос!) | BFF для сложного фронтенда. Обязателен `DataLoader` против проблемы N+1 в `async def` резолверах |

## Типичные ошибки в Python

- ⚠️ Создавать `httpx.AsyncClient()` внутри каждого HTTP-хендлера вместо пула
  на уровне `lifespan` → исчерпание сокетов и лишние TLS-рукопожатия.
- ⚠️ Выносить ORM-модели SQLAlchemy/Django в общий пакет `common` для
  нескольких микросервисов → жёсткий распределённый монолит.
- ⚠️ Возвращать ленивые ORM-модели из `AsyncSession` напрямую в Pydantic-ответы
  → падение с `MissingGreenlet` и протечка схемы БД в API.
- ⚠️ Делать один глобальный `DataLoader` в GraphQL на весь процесс → утечка
  памяти и чужих данных между запросами разных пользователей.

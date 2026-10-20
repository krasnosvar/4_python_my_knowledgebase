# Чистая архитектура, Гексагональная архитектура и DDD в Python

## О чём эта тема (краткий контекст)

Даже если границы между сервисами проведены правильно, код внутри отдельного
сервиса может быстро деградировать, когда бизнес-правила перемешиваются с
SQL-запросами, HTTP-статусами и деталями внешних API. Слоистая (Layered),
Гексагональная (Ports & Adapters) и Чистая архитектура (Clean Architecture)
вместе с тактическими паттернами Domain-Driven Design (DDD) решают эту
проблему: они отделяют чистую доменную логику от фреймворков и баз данных,
направляя все зависимости внутрь — к ядру бизнеса. Это позволяет тестировать
сложные бизнес-сценарии за миллисекунды без поднятия БД и менять
инфраструктуру без переписывания правил предметной области.

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Архитектура внутри сервиса: Layered, Clean, Hexagonal и DDD](../../../../5_devops_sre_knowledgebase/14_system_design/01_architecture_and_api_styles/01_theory/02_service_architecture_clean_ddd.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки). Кодовый уровень принципов ООП (SOLID)
> разобран в уроке [SOLID в
> Python](../../../1_python/3_oop/01_theory/08_solid_in_python.md).

---

## 1. Active Record («толстые модели» Django) против Clean Architecture

В мире Python сосуществуют две противоположные архитектурные школы, связанные с
устройством двух главных фреймворков:

### Подход 1: Active Record и «Fat Models, Thin Views» (Django)

В Django ORM модель (`models.Model`) одновременно описывает таблицу БД,
валидацию и методы работы с данными, а сама умеет сохранять себя в базу
(`order.save()`). Это классический паттерн **Active Record**:

- **Когда отлично работает:** CRUD-сервисы, админки, контентные проекты и
  простые домены, где бизнес-логика сводится к проверке пары полей и записи в
  таблицу.
- **Где ломается в сложных системах:**
  1. Доменная сущность неотделима от БД — нельзя создать и протестировать
     сложный расчёт скидок и лимитов без обращения к PostgreSQL или хрупких
     моков ORM.
  2. По мере роста проекта модель `Order` разрастается до 3000 строк («God
     Object»), знающих одновременно про биллинг, доставку, промокоды и
     уведомления.
  3. Любой код, получивший экземпляр ORM-модели (даже шаблон или сериализатор),
     может неявно дёрнуть ленивый атрибут (`order.user.profile`) и породить
     скрытый синхронный SQL-запрос (проблема N+1, см. [ленивые
     выборки](../../../3_web_frameworks/2_django/01_theory/02_lazy_querysets.md)).

### Подход 2: Domain Model + Repository + Unit of Work (FastAPI + SQLAlchemy)

В Чистой и Гексагональной архитектуре доменные объекты — это обычные
Python-классы (`@dataclass`), которые вообще не знают про SQLAlchemy, Django
или FastAPI. Доступ к БД скрыт за абстрактным портом (**Repository**), а
управление транзакцией — за паттерном **Unit of Work (UoW)**.

```text
+-------------------------------------------------------------------+
| Presentation / Adapters (FastAPI routers, Celery tasks, CLI)      |
|   │ вызывает                                                      |
|   ▼                                                               |
| Application / Use Cases (Service Layer, UnitOfWork interface)     |
|   │ оркестрирует                         ▲ реализует порт         |
|   ▼                                      │                        |
| Domain (Entities, @dataclass(frozen=True) Value Objects, Ports)   |
+------------------------------------------│------------------------+
                                           │
+------------------------------------------┴------------------------+
| Infrastructure (SQLAlchemy AsyncSession, Redis, httpx clients)    |
+-------------------------------------------------------------------+
```

---

## 2. Тактический DDD и Порты/Адаптеры на идиоматичном Python

В отличие от Java или C#, в Python не нужны громоздкие иерархии интерфейсов и
DI-контейнеры на XML/рефлексии. Стандартная библиотека Python (`dataclasses`,
`typing.Protocol`, контекстные менеджеры `async with`) позволяет выразить все
паттерны Clean Architecture лаконично и строго типизированно.

### 1. Value Object и Entity на `@dataclass`

- **Value Object (Объект-значение)** определяется только своими атрибутами и
  обязан быть неизменяемым: в Python это `@dataclass(frozen=True, slots=True)`.
- **Entity (Сущность)** обладает уникальным идентификатором (`id`) и методами,
  защищающими бизнес-инварианты.

```python
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


class DomainError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise DomainError("Сумма не может быть отрицательной")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise DomainError("Нельзя складывать разные валюты")
        return Money(self.amount + other.amount, self.currency)


@dataclass
class Order:
    customer_id: UUID
    total: Money
    status: str = "NEW"
    id: UUID = field(default_factory=uuid4)

    def mark_paid(self) -> None:
        if self.status != "NEW":
            raise DomainError(f"Нельзя оплатить заказ в статусе {self.status}")
        self.status = "PAID"
```

### 2. Порт (Repository Interface) через `typing.Protocol`

Для инверсии зависимостей (DIP) доменный или сервисный слой объявляет
структурный интерфейс с помощью `typing.Protocol` (см. [утиная типизация и
протоколы](../../../1_python/3_oop/01_theory/07_duck_typing_and_protocols.md)).
Адаптеру не нужно даже наследоваться от протокола — `mypy` и `pyright`
проверят совместимость сигнатур статически:

```python
from typing import Protocol


class OrderRepositoryPort(Protocol):
    async def get_by_id(self, order_id: UUID) -> Order | None: ...
    async def save(self, order: Order) -> None: ...
```

### 3. Паттерн Unit of Work (UoW) через `async with`

Если бизнес-операция меняет две сущности (например, списывает средства и меняет
статус заказа плюс пишет событие в Outbox), нельзя вызывать
`await session.commit()` внутри каждого метода репозитория — иначе половина
операции закоммитится, а вторая упадёт.

В Python паттерн **Unit of Work** естественно ложится на асинхронный
контекстный менеджер (`__aenter__` / `__aexit__`), оборачивающий
`sqlalchemy.ext.asyncio.AsyncSession`:

```python
from typing import Protocol, Self


class UnitOfWorkPort(Protocol):
    orders: OrderRepositoryPort

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
```

Реализация адаптера инфраструктуры поверх SQLAlchemy:

```python
class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.orders = SqlAlchemyOrderRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
```

### 4. Сервисный слой (Use Case) и сборка через `FastAPI Depends()`

Слой сценария использования (Use Case) зависит только от `UnitOfWorkPort` и
доменных классов, а связывание (Dependency Injection) происходит на самом
верхнем уровне — в FastAPI роутере (или через контейнер вроде `dishka`):

```python
# Слой Application (Use Case) — ноль импортов из fastapi или sqlalchemy!
class PayOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort) -> None:
        self._uow = uow

    async def execute(self, order_id: UUID) -> None:
        async with self._uow as uow:
            order = await uow.orders.get_by_id(order_id)
            if order is None:
                raise DomainError("Заказ не найден")
            order.mark_paid()
            await uow.orders.save(order)
            await uow.commit()
```

Почему это радикально упрощает жизнь в больших Python-сервисах:
1. **Тестируемость:** для юнит-теста `PayOrderUseCase` достаточно написать
   `FakeUnitOfWork` на обычном `dict` в 15 строк кода — сотни бизнес-тестов
   проходят за 0.05 секунды без Docker и PostgreSQL.
2. **Безопасность в `asyncio`:** в `AsyncSession` SQLAlchemy запрещён неявный
   ленивый I/O (попытка обратиться к незагруженному `relationship` вне
   репозитория выбросит `MissingGreenlet`). Явный маппинг ORM-модели в чистый
   доменный `@dataclass` в репозитории полностью исключает `MissingGreenlet`
   в бизнес-логике и сериализаторах Pydantic.

---

## 3. Когда Clean Architecture в Python оправдана, а когда вредна

| Характеристика сервиса | Рекомендуемая архитектура в Python |
| :--- | :--- |
| Простой CRUD / админка / внутренний справочник, логика — «прочитать из БД и отдать JSON» | **Двухслойная (Роутер + ORM / Сервис):** FastAPI + SQLAlchemy напрямую в сервисе или Django Active Record. Полный DDD и UoW здесь — оверинжиниринг |
| Средний сервис с интеграциями (внешние API, брокер, кэш), умеренная бизнес-логика | **Слоистая + Сервисный слой (Service Layer):** роутеры принимают Pydantic-схемы, сервисы управляют транзакцией и вызывают внешние клиенты через интерфейсы |
| Ядро бизнеса (биллинг, расчёт тарифов, кредитный конвейер, оркестрация заказов), долгий срок жизни | **Гексагональная / Чистая архитектура + тактический DDD:** чистые `@dataclass`-сущности, `Protocol`-порты, `UnitOfWork`, строгая изоляция от ORM |
| Асимметрия чтения и записи (сложные инварианты при записи и тяжёлые плоские витрины при чтении) | **CQRS внутри сервиса:** команды идут через Domain + UoW, а запросы на чтение выполняют прямой `SELECT` через SQLAlchemy Core и сразу возвращают Pydantic DTO в обход доменных моделей |

---

## 4. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** Почему в асинхронном FastAPI-сервисе с SQLAlchemy 2.0 опасно
> возвращать ORM-модели из сервисного слоя напрямую в роутеры и полагаться на
> `from_attributes=True` в Pydantic?
>
> **Ответ:** Во-первых, это нарушает границу слоёв: структура таблицы БД
> протекает во внешний API-контракт. Во-вторых, когда Pydantic начинает читать
> поля ORM-модели во время сериализации ответа, обращение к любому
> незагруженному (`lazy="select"`) связанному полю попытается выполнить
> синхронный SQL-запрос вне зеленого потока SQLAlchemy и упадёт в рантайме с
> ошибкой `sqlalchemy.exc.MissingGreenlet` (или обратится к уже закрытой
> сессии). Преобразование в доменный `@dataclass` или явный DTO внутри
> репозитория/Use Case гарантирует, что все данные уже загружены в память.

> **Вопрос:** Зачем в Python нужен `Unit of Work`, если в SQLAlchemy уже есть
> `AsyncSession`, которая сама реализует паттерн Identity Map и Unit of Work?
>
> **Ответ:** `AsyncSession` действительно является реализацией Unit of Work на
> уровне ORM. Собственная обёртка `UnitOfWorkPort` нужна по двум причинам:
> 1) чтобы бизнес-логика (Use Case) не импортировала `AsyncSession` из
> `sqlalchemy` и могла тестироваться с in-memory фейком без базы данных;
> 2) чтобы сгруппировать в едином контексте `async with uow:` все репозитории,
> разделяющие одну и ту же транзакцию (`uow.orders`, `uow.payments`,
> `uow.outbox`), и гарантировать автоматический `rollback()` при любом
> необработанном исключении в блоке `async with`.

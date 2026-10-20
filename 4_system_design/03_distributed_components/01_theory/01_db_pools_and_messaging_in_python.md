# Пулы соединений к БД, PgBouncer и брокеры сообщений в Python

## О чём эта тема (краткий контекст)

В распределённой системе сервисы работают с разными типами хранилищ (реляционные
БД для транзакций, NoSQL для быстрых ключей и поиска) и связываются между собой
асинхронно через брокеры сообщений (Kafka, RabbitMQ). Брокер развязывает
сервисы во времени, сглаживает пики нагрузки и гарантирует доставку событий, а
паттерны Transactional Outbox и идемпотентный консьюмер защищают систему от
потери или задвоения сообщений при сетевых сбоях. На уровне рантайма каждый
инстанс сервиса удерживает пул сетевых соединений к БД и брокеру, которым
необходимо управлять, чтобы не исчерпать лимиты инфраструктуры.

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Репликация, шардирование, CAP/PACELC и распределённые данные](../../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/01_data_replication_sharding_and_cap.md)
> - [Очереди, брокеры сообщений, Outbox, идемпотентность и Backpressure](../../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/02_messaging_and_async_patterns.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки). Механика самих брокеров разобрана в
> разделе [3_message_brokers](../../../2_data_and_messaging/3_message_brokers/).

---

## 1. Главная ловушка БД в Python: умножение пулов соединений

В языках с многопоточным рантаймом (Go, Java) один процесс приложения
утилизирует все ядра контейнера и держит **один общий пул соединений** к
PostgreSQL. В Python из-за GIL приложение запускают в виде нескольких
процессов-воркеров (`gunicorn -w 4` или несколько контейнеров).

Поскольку процессы не разделяют память и сокеты, **каждый процесс-воркер
создаёт собственный `Engine` и собственный `QueuePool` в SQLAlchemy**:

```text
Максимальное число соединений к PostgreSQL от одного сервиса:
N_conns = PODS × GUNICORN_WORKERS × (pool_size + max_overflow)
```

Посчитаем дефолтные настройки SQLAlchemy (`pool_size=5, max_overflow=10`) для
обычного кластера из 10 подов по 4 воркера Gunicorn плюс 10 подов Celery:
- Веб-воркеры: $10 \times 4 \times (5 + 10) = 600$ соединений;
- Воркеры Celery: ещё $10 \times 8 = 80$ соединений.

При всплеске трафика один сервис мгновенно пытается открыть **680 физических
соединений** к PostgreSQL, пробивает `max_connections` (по умолчанию 100–200) и
роняет базу с ошибкой `FATAL: sorry, too many clients already`.

### Как правильно настраивать пул SQLAlchemy и PgBouncer в Python

1. **Всегда ставьте `PgBouncer` (или `Odyssey` / `pgcat`) в режиме
   `pool_mode = transaction`** между Python-воркерами и PostgreSQL. Тогда 600
   логических соединений от Python мультиплексируются в 30–50 реальных
   серверных процессов PostgreSQL только на время выполнения транзакции.
2. **Критичный нюанс `asyncpg` + `PgBouncer` (`transaction` mode):** драйвер
   `asyncpg` по умолчанию создаёт именованные `PREPARE` выражения, привязанные
   к конкретной серверной сессии PostgreSQL. В режиме `transaction` PgBouncer
   переключает серверные соединения между транзакциями, и `asyncpg` падает с
   ошибкой `PreparedStatementError: prepared statement "__asyncpg_stmt_1__"
   does not exist`.
   **Решение:** отключить кэш prepared statements в `create_async_engine` (или
   включить поддержку протокола prepared statements в PgBouncer 1.21+):

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://app:secret@pgbouncer:6432/prod_db",
    pool_size=5,
    max_overflow=5,
    pool_timeout=3.0,        # не ждать свободный коннект 30 секунд!
    pool_pre_ping=True,      # проверять живость коннекта перед выдачей
    pool_recycle=1800,       # переоткрывать коннект каждые 30 минут
    connect_args={
        "statement_cache_size": 0,  # обязательно для PgBouncer transaction mode
    },
)
```

3. **В процессах Celery с `prefork`** либо используйте `NullPool` (при наличии
   локального PgBouncer), либо инициализируйте `Engine` строго по сигналу
   `worker_process_init`, чтобы дочерние воркеры после `os.fork()` не пытались
   писать в один и тот же файловый дескриптор сокета родительского процесса.

---

## 2. Transactional Outbox на Python (`FOR UPDATE SKIP LOCKED`)

Нельзя делать `await session.commit()` и следующей строчкой
`await kafka_producer.send(...)`: если процесс упадёт между ними (или брокер
недоступен), запись в БД останется, а событие навсегда потеряется.

В Python паттерн **Transactional Outbox** реализуется в два шага:

### Шаг 1. Запись бизнес-сущности и события в одной транзакции SQLAlchemy

```python
from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    topic: Mapped[str] = mapped_column(String(128), nullable=False)
    key: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    processed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )
```

Внутри вашего `UnitOfWork` (см. тему 01) вместе с `session.add(order)` в ту же
сессию добавляется `session.add(OutboxEvent(...))`, после чего вызывается единый
`await session.commit()`.

### Шаг 2. Фоновый воркер-ретранслятор (Outbox Relay)

Чтобы несколько воркеров могли параллельно разгребать таблицу `outbox_events`,
не блокируя друг друга и не отправляя одно событие дважды, в PostgreSQL
используют конструкцию **`with_for_update(skip_locked=True)`**:

```python
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def relay_outbox_batch(session: AsyncSession, producer) -> int:
    async with session.begin():
        stmt = (
            select(OutboxEvent)
            .where(OutboxEvent.processed_at.is_(None))
            .order_by(OutboxEvent.id)
            .limit(100)
            # соседние воркеры возьмут другие строки
            .with_for_update(skip_locked=True)
        )
        events = list((await session.scalars(stmt)).all())
        if not events:
            return 0

        for ev in events:
            await producer.send_and_wait(
                ev.topic, key=ev.key.encode(), value=ev.payload
            )

        ids = [ev.id for ev in events]
        await session.execute(
            update(OutboxEvent)
            .where(OutboxEvent.id.in_(ids))
            .values(processed_at=func.now())
        )
        return len(events)
```

---

## 3. Идемпотентный консьюмер и Backpressure в `asyncio`

Поскольку брокеры и Outbox гарантируют доставку **at-least-once** (хотя бы один
раз), ваш Python-консьюмер (`aiokafka`, `aio-pika`, `FastStream` или задача
Celery) гарантированно получит дубликаты при ребалансировке партиций или
повторной отправке.

### Идемпотентная обработка через таблицу `processed_messages` (Inbox)

Самый надёжный способ в Python — вставлять `message_id` в таблицу
`processed_messages` (`PRIMARY KEY (message_id)`) через
`INSERT ... ON CONFLICT DO NOTHING` **внутри той же транзакции**, которая меняет
бизнес-данные:

```python
from sqlalchemy.dialects.postgresql import insert


async def handle_event_idempotently(
    session: AsyncSession, msg_id: str, data: dict
) -> bool:
    async with session.begin():
        stmt = (
            insert(ProcessedMessage)
            .values(message_id=msg_id)
            .on_conflict_do_nothing(index_elements=["message_id"])
        )
        res = await session.execute(stmt)
        if res.rowcount == 0:
            # Дубликат: сообщение уже было успешно обработано ранее!
            return False

        await apply_business_logic(session, data)
        return True
```

### Backpressure (обратное давление) в `asyncio`-консьюмерах

Опасный антипаттерн в Python — вычитывать сообщения из брокера в бесконечном
цикле и на каждое делать `asyncio.create_task(process(msg))` без ограничений.
При всплеске в очереди в памяти процесса мгновенно создадутся 100 000 корутин,
воркер упадёт по `OOMKilled` и не сможет отправить heartbeat брокеру.

**Правило:** ограничивайте параллелизм внутри воркера с помощью
`asyncio.Semaphore(max_concurrency)` или фиксированного пула корутин-воркеров,
читающих из `asyncio.Queue(maxsize=100)`. Пока очередь заполнена, `await
queue.put(msg)` приостанавливает вычитку из сокета брокера, создавая
естественный backpressure.

---

## 4. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** Команда увеличила число реплик FastAPI-сервиса в Kubernetes с 3
> до 25 в преддверии распродажи, и через минуту база PostgreSQL упала с ошибкой
> `too many clients already`. Почему это произошло и как починить?
>
> **Ответ:** Каждый под запускал несколько воркеров Uvicorn/Gunicorn, и каждый
> процесс-воркер инициализировал собственный пул `SQLAlchemy` (`pool_size +
> max_overflow`). При 25 подах по 4 воркера и пуле 15 соединений сервис открыл
> до 1500 соединений к PostgreSQL. Решение: 1) поставить перед БД пулер
> `PgBouncer` в режиме `transaction` (с `statement_cache_size=0` в `asyncpg`);
> 2) уменьшить число процессов на под до 1 воркера Uvicorn на 1 vCPU и снизить
> `pool_size` на стороне приложения.

> **Вопрос:** Почему конструкция `SELECT ... FOR UPDATE SKIP LOCKED` идеально
> подходит для воркеров Outbox на Python?
>
> **Ответ:** Обычный `FOR UPDATE` заблокировал бы второй воркер до тех пор,
> пока первый не закончит отправку батча в Kafka. Модификатор `SKIP LOCKED`
> приказывает PostgreSQL мгновенно пропустить уже заблокированные соседним
> воркером строки и выдать следующие 100 свободных записей. Это позволяет
> горизонтально масштабировать Python-воркеры ретранслятора Outbox без
> взаимных блокировок и без дублирования отправки.

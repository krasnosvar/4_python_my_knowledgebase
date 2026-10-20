# Кейс 1: Система денежных переводов на Python

## О чём эта тема (краткий контекст)

Система денежных переводов — классический кейс System Design, где главным
нефункциональным требованием выступает строгая согласованность (ACID) и
абсолютная финансовая корректность: деньги нельзя потерять, списать дважды при
сетевом ретрае или увести баланс в минус при параллельных запросах. Архитектура
такого сервиса строится вокруг ключей идемпотентности (`Idempotency-Key`),
пессимистичных блокировок строк счетов в упорядоченном порядке (защита от
deadlock), журнала двойной записи (Double-Entry Ledger) и паттерна
Transactional Outbox для надёжной отправки событий.

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Фреймворк System Design интервью и расчёты нагрузки](../../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/01_theory/01_interview_framework_and_estimations.md)
> - [Сквозные кейсы: денежные переводы, медиа-галерея, URL Shortener и лента](../../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/01_theory/02_case_studies_transfers_and_media.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки). Рабочую модель идемпотентного перевода с
> журналом двойной записи на чистом Python можно запустить в [`main.py`
> (Idempotent Transfer)](../02_examples/01_idempotent_transfer/main.py).

---

## 1. Представление денег в Python: почему `float` запрещён

В Python тип `float` реализован как двоичное число с плавающей точкой IEEE 754
(`double` в C). Десятичные дроби `0.1` и `0.2` не имеют точного двоичного
представления, поэтому базовый инвариант бухгалтерии ломается на первой же
операции:

```python
print(0.1 + 0.2 == 0.3)  # False (0.30000000000000004)
```

В Python-сервисах для денег используют один из двух строгих подходов:

1. **Целые минорные единицы (`int` — копейки, центы):** `amount_minor: int`. В
   Python тип `int` имеет произвольную точность (не переполняется, как `int64`)
   и идеально ложится на `BIGINT` в PostgreSQL.
2. **`decimal.Decimal` с фиксированным контекстом округления** (например,
   банковское округление `ROUND_HALF_EVEN`) и хранением в `NUMERIC(18, 4)` в
   PostgreSQL (важно передавать в конструктор `Decimal("10.50")` строку, а не
   `float`!).

В Pydantic v2 входной контракт фиксируется строго:

```python
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class TransferRequest(BaseModel):
    from_account_id: UUID
    to_account_id: UUID
    # Строго положительное целое число в минорных единицах (копейках/центах)
    amount_minor: int = Field(gt=0, le=100_000_000_00)
    currency: str = Field( min_length=3, max_length=3)
```

---

## 2. Защита от гонок и Deadlock: `with_for_update()` в SQLAlchemy и Django

Представим два параллельных запроса:
- Запрос 1 переводит 100 ₽ со счёта `A` на счёт `B`;
- Запрос 2 одновременно переводит 50 ₽ со счёта `B` на счёт `A`.

Если Запрос 1 сначала заблокирует строку `A`, а Запрос 2 в этот же момент
заблокирует строку `B`, оба воркера встанут в **взаимную блокировку
(Deadlock)**, ожидая друг друга, пока PostgreSQL не убьёт одну из транзакций по
`deadlock_timeout`.

### Правило детерминированной сортировки идентификаторов

Чтобы deadlock был математически невозможен, **всегда сортируйте ID счетов
перед взятием блокировки `SELECT ... FOR UPDATE`** и запрашивайте их одним
оператором `WHERE id IN (...) ORDER BY id`:

```python
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def lock_accounts_in_order(
    session: AsyncSession, acc_a: UUID, acc_b: UUID
) -> tuple[AccountModel, AccountModel]:
    if acc_a == acc_b:
        raise ValueError("Нельзя переводить средства самому себе")

    # Сортируем UUID: любой воркер блокирует счета в одном и том же порядке!
    ordered_ids = sorted([acc_a, acc_b])

    stmt = (
        select(AccountModel)
        .where(AccountModel.id.in_(ordered_ids))
        .order_by(AccountModel.id)
        .with_for_update()  # SELECT ... FOR UPDATE
    )
    rows = (await session.scalars(stmt)).all()
    if len(rows) != 2:
        raise AccountNotFoundError()

    by_id = {row.id: row for row in rows}
    return by_id[acc_a], by_id[acc_b]
```

В синхронном Django ORM эта же конструкция пишется внутри
`with transaction.atomic():` через
`Account.objects.select_for_update().filter(id__in=ordered_ids).order_by("id")`.

---

## 3. Атомарная реализация: Idempotency + Double-Entry + Outbox

Если клиент нажал кнопку «Перевести» дважды за 5 миллисекунд, две корутины в
разных воркерах Uvicorn одновременно пройдут простую проверку `SELECT` по
таблице `idempotency_keys` (обе увидят `None`) и спишут деньги дважды!

### Как защитить идемпотентность от параллельных дублей в Python

1. В начале транзакции вставляем запись в `idempotency_keys` со статусом
   `"STARTED"` и хэшем тела запроса (`payload_hash`).
2. Если второй запрос с тем же `Idempotency-Key` прилетел параллельно, его
   `INSERT` либо ждёт завершения первой транзакции на уникальном индексе в
   PostgreSQL, либо падает с `sqlalchemy.exc.IntegrityError` (в этот момент мы
   отдаём `409 Conflict: Request in progress` или возвращаем сохранённый ответ).
3. Если клиент прислал тот же `Idempotency-Key`, но подменил сумму или счёт
   получателя (`existing.payload_hash != current_hash`), немедленно возвращаем
   `422 Unprocessable Entity`.

```python
import hashlib
from uuid import UUID, uuid4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def execute_transfer(
    session: AsyncSession,
    idempotency_key: str,
    req: TransferRequest,
) -> dict:
    raw_payload = (
        f"{req.from_account_id}:{req.to_account_id}:"
        f"{req.amount_minor}:{req.currency}"
    )
    payload_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

    async with session.begin():
        existing = await session.get(
            IdempotencyRecord, idempotency_key, with_for_update=True
        )
        if existing is not None:
            if existing.payload_hash != payload_hash:
                raise IdempotencyKeyMismatchError("Параметры запроса изменены")
            return existing.response_body

        # 1. Блокируем оба счёта в детерминированном порядке
        sender, receiver = await lock_accounts_in_order(
            session, req.from_account_id, req.to_account_id
        )
        if sender.balance_minor < req.amount_minor:
            raise InsufficientFundsError("Недостаточно средств")

        # 2. Создаём перевод и пару проводок (Double-Entry Bookkeeping)
        transfer_id = uuid4()
        session.add_all(
            [
                LedgerEntry(
                    transfer_id=transfer_id,
                    account_id=sender.id,
                    direction="DEBIT",
                    amount_minor=req.amount_minor,
                ),
                LedgerEntry(
                    transfer_id=transfer_id,
                    account_id=receiver.id,
                    direction="CREDIT",
                    amount_minor=req.amount_minor,
                ),
            ]
        )

        # 3. Обновляем денормализованные балансы
        sender.balance_minor -= req.amount_minor
        receiver.balance_minor += req.amount_minor

        response = {"transfer_id": str(transfer_id), "status": "completed"}

        # 4. Сохраняем ключ идемпотентности и Outbox-событие в ТОЙ ЖЕ транзакции
        session.add(
            IdempotencyRecord(
                key=idempotency_key,
                payload_hash=payload_hash,
                response_body=response,
            )
        )
        session.add(
            OutboxEvent(
                topic="transfers.events",
                key=str(sender.id),
                payload=response,
            )
        )

    return response
```

---

## 4. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** Почему внутри транзакции `execute_transfer` нельзя делать
> HTTP-вызов к внешнему банку или антифроду (`await httpx_client.post(...)`)
> после того, как выполнен `SELECT ... FOR UPDATE` по счёту клиента?
>
> **Ответ:** Пока открыта транзакция с `FOR UPDATE`, PostgreSQL держит
> эксклюзивную строковую блокировку (`RowExclusiveLock`) на обоих счетах и
> занимает физическое соединение из пула `PgBouncer`. Если внешний HTTP-вызов
> зависнет на 2 секунды, все параллельные операции по этим счетам (особенно если
> один из счетов — горячий счёт мерчанта) встанут в очередь, а пул соединений к
> БД мгновенно исчерпается. Любые сетевые походы выполняются **строго вне БД
> транзакции** (через двухфазное резервирование средств: транзакция 1 — `HOLD`,
> сетевой вызов, транзакция 2 — `CAPTURE` или `RELEASE`).

> **Вопрос:** Что будет, если проверять идемпотентность простым
> `SELECT * FROM idempotency_keys WHERE key = :k` на уровне `READ COMMITTED`
> до изменения балансов без уникального ограничения и без блокировки?
>
> **Ответ:** Классическая гонка `Check-Then-Act` (TOCTOU). Два параллельных
> запроса от одного клиента одновременно выполнят `SELECT`, оба получат пустой
> результат, оба спишут деньги и лишь на этапе `COMMIT` второй упадёт по
> `UniqueViolation` (если есть уникальный индекс) либо создаст дубль (если
> индекса нет).

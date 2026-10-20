# Масштабирование данных в Python: Read/Write Splitting и роутинг по шардам

## О чём эта тема (краткий контекст)

Когда кэширование уже не спасает, а один узел базы данных упирается в потолок
по CPU, диску или соединениям, нагрузку на хранилище разделяют по двум осям:
отделяют чтение от записи с помощью реплик (Read/Write Splitting) и делят сами
данные на независимые части по ключу шардирования (Partitioning & Sharding).
Переход к репликам требует учитывать задержку репликации (replication lag),
чтобы пользователь видел собственные только что сохранённые изменения
(read-your-writes consistency), а шардирование на уровне приложения требует
детерминированной маршрутизации запросов к нужному узлу БД и минимизации
перемещения ключей при добавлении новых шардов (Consistent Hashing).

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Репликация, шардирование, CAP/PACELC и распределённые данные](../../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/01_data_replication_sharding_and_cap.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки). Базовая механика репликации PostgreSQL
> также рассмотрена в [репликации
> БД](../../../2_data_and_messaging/1_sql_relational_databases/01_theory/08_replication.md).

---

## 1. Read/Write Splitting (Лидер и Реплики) в SQLAlchemy и Django

Чтобы направлять пишущие транзакции (`INSERT/UPDATE/DELETE` и `SELECT ... FOR
UPDATE`) в `primary` (лидер), а обычные чтения (`SELECT`) — в пул
`read-replica`, в Python-приложениях используют маршрутизацию на уровне сессии
ORM.

### Реализация в SQLAlchemy 2.0 через `Session.get_bind()` и `contextvars`

В асинхронном FastAPI-приложении удобно управлять выбором БД через переменную
контекста `contextvars.ContextVar` (изолирована для каждой корутины/запроса):

```python
from contextvars import ContextVar
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

use_primary_ctx: ContextVar[bool] = ContextVar("use_primary", default=False)

primary_engine = create_engine("postgresql+psycopg://app@db-primary/prod")
replica_engine = create_engine("postgresql+psycopg://app@db-replica/prod")


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        # Всегда идём в лидер при записи, флаге или внутри транзакции записи
        if (
            self._flushing
            or use_primary_ctx.get()
            or self.in_nested_transaction()
        ):
            return primary_engine
        return replica_engine
```

### Гарантия Read-Your-Writes при асинхронной репликации

Если пользователь обновил профиль (`POST /profile` ушёл в `primary`) и через 20
мс браузер запросил `GET /profile`, чтение с реплики может вернуть старые
данные, так как WAL-запись ещё не доехала до реплики.

В Python-бэкенде это решается middleware-слоем:
1. При любой успешной мутации (`POST`, `PUT`, `PATCH`, `DELETE`) бэкенд
   выставляет в Redis ключ `recent_write:{user_id}` с TTL `3 секунды` (или
   ставит короткоживущую cookie `wrote_recently=1`).
2. При входящем `GET`-запросе middleware проверяет этот маркер: если он есть —
   вызывает `use_primary_ctx.set(True)`, принудительно направляя чтение этого
   пользователя в `primary` на ближайшие 3 секунды.

### Реализация в Django через `DatabaseRouter`

В Django маршрутизация чтения/записи и шардов встроена в ядро через класс
роутера в `settings.DATABASE_ROUTERS`:

```python
import random


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints) -> str:
        if use_primary_ctx.get():
            return "default"
        return random.choice(["replica_1", "replica_2"])

    def db_for_write(self, model, **hints) -> str:
        return "default"

    def allow_relation(self, obj1, obj2, **hints) -> bool:
        return True
```

---

## 2. Прикладной роутинг по шардам (Application-Level Sharding)

Когда один `primary`-узел PostgreSQL перестаёт справляться с потоком **записи**
или объёмом таблиц, данные делят между несколькими физическими БД по ключу
шардирования (`shard_key`, например `tenant_id`, `user_id` или `account_id`).

Разницу между наивным `hash(key) % N` (при котором добавление одного шарда
перемещает ~80% ключей) и кольцом **Consistent Hashing** (перемещается только
$1/N$ ключей) можно наглядно проверить, запустив пример
[`03_consistent_hashing/main.py`](../02_examples/03_consistent_hashing/main.py).

> **Важная деталь Python (`hash()` vs `hashlib`):** никогда не используйте
> встроенную функцию `hash(user_id)` для выбора шарда или ключа в Redis! В
> Python 3.3+ включена защита от Hash-DoS (`PYTHONHASHSEED`), из-за которой
> встроенный `hash("user_42")` возвращает **разные числа в разных процессах
> воркеров** и меняется после каждого перезапуска контейнера. Для шардирования
> используйте только детерминированные алгоритмы: `zlib.crc32`, `mmh3` или
> `hashlib.md5` / `sha256`.

```python
import zlib
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

SHARD_SESSIONS: dict[int, async_sessionmaker[AsyncSession]] = {
    0: shard_0_maker,
    1: shard_1_maker,
    2: shard_2_maker,
    3: shard_3_maker,
}


def get_shard_id(tenant_id: str, num_shards: int = 4) -> int:
    # Детерминированный CRC32 одинаков на всех воркерах и после рестарта
    checksum = zlib.crc32(tenant_id.encode("utf-8"))
    return checksum % num_shards


def get_session_for_tenant(tenant_id: str) -> AsyncSession:
    shard_id = get_shard_id(tenant_id, len(SHARD_SESSIONS))
    return SHARD_SESSIONS[shard_id]()
```

Также в пакете `sqlalchemy.ext.horizontal_shard` есть готовый класс
`ShardedSession`, который принимает колбэки `shard_chooser`, `identity_chooser`
и `execute_chooser` и прозрачно маршрутизирует ORM-запросы в нужный пул.

---

## 3. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** Почему при шардировании в Python нельзя написать
> `shard_id = hash(account_id) % NUM_SHARDS` для строковых или UUID ключей?
>
> **Ответ:** В CPython по умолчанию включена рандомизация хэш-функции для строк
> и байтов (`PYTHONHASHSEED=random`) для защиты словарей от коллизионных
> DoS-атак. Из-за этого два разных воркера Uvicorn (и один и тот же воркер
> после рестарта) вычислят разные значения `hash(account_id)` и отправят
> запросы одного клиента в разные шарды БД. Для роутинга по шардам нужен
> криптографический или стабильный некриптографический хэш (`zlib.crc32`,
> `hashlib.sha256`, `xxhash`, `mmh3`).

> **Вопрос:** В сервисе переводов или интернет-магазине добавили read-реплики
> через `DatabaseRouter` в Django, и теперь все `SELECT`-запросы автоматически
> уходят на реплики. Какая критическая уязвимость при этом появилась?
>
> **Ответ:** Любой `SELECT`, результат которого используется для принятия
> решения о записи внутри транзакции (например, проверка баланса перед
> списанием или остатка товара на складе, особенно с `select_for_update`),
> не имеет права идти в отстающую read-реплику! Во-первых, на реплике данные
> могут отставать на десятки миллисекунд (позволяя списать средства дважды).
> Во-вторых, `SELECT ... FOR UPDATE` на read-only реплике PostgreSQL вообще
> завершится ошибкой. Роутер обязан направлять в `primary` все чтения внутри
> открытой пишущей транзакции (`transaction.atomic()`).

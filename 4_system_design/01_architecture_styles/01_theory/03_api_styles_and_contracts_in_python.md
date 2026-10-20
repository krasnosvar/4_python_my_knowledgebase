# Стили API и контракты в Python: REST, gRPC, GraphQL

## О чём эта тема (краткий контекст)

Когда система разделена на сервисы или отдаёт данные внешним клиентам
(браузерам, мобильным приложениям, партнёрам), критическим узлом становятся
сетевые контракты: в каком формате передавать данные и как проверять их
корректность. REST поверх JSON универсален и понятен человеку, gRPC поверх
HTTP/2 и Protobuf минимизирует сетевые задержки и накладные расходы CPU между
внутренними микросервисами, а GraphQL позволяет фронтенду запрашивать сложные
графы данных одним запросом без лишних походов по сети. На периметре всей
системы эти взаимодействия координируются через API Gateway и паттерн Backend
for Frontend (BFF).

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Стили API (REST, gRPC, GraphQL), API Gateway и Service Discovery](../../../../5_devops_sre_knowledgebase/14_system_design/01_architecture_and_api_styles/01_theory/03_api_styles_gateway_and_discovery.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки).

---

## 1. REST и JSON в Python: стоимость сериализации и Pydantic v2

В компилируемых языках парсинг и сериализация JSON редко становятся главным
узким местом CPU. В Python создание тысяч словарей и объектов на каждый
HTTP-запрос нагружает интерпретатор CPython и удерживает GIL.

### Как сделать REST на FastAPI быстрым

1. **Ядро Pydantic v2 (`pydantic-core` на Rust).** Валидация входящего JSON в
   Pydantic v2 выполняется в скомпилированном Rust-коде без создания
   промежуточных Python-словарей, если использовать `model_validate_json()`
   вместо связки `json.loads()` + `model_validate()`.
2. **Быстрые JSON-библиотеки (`orjson`, `msgspec`).** Стандартный модуль `json`
   медленно сериализует `UUID`, `datetime` и `dataclass`. Замена стандартного
   ответа в FastAPI на `ORJSONResponse` (написан на Rust, сразу отдаёт `bytes`)
   снижает затраты CPU на сериализацию больших ответов в 3–8 раз.
3. **Не валидировать повторно собственные ответы.** Если вы сами сформировали
   корректный объект из БД, повторная прогонка списка из 10 000 элементов через
   `response_model` в FastAPI может занять больше времени, чем сам SQL-запрос.
   Для высоконагруженных эндпоинтов используют `msgspec.Struct` или
   возвращают `ORJSONResponse` напрямую.

```python
from datetime import datetime
from uuid import UUID
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, ConfigDict

# По умолчанию все роуты сериализуют ответ через Rust-библиотеку orjson
app = FastAPI(default_response_class=ORJSONResponse)


class OrderResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    order_id: UUID
    amount_minor: int
    created_at: datetime
```

---

## 2. gRPC в Python (`grpcio`, `grpc.aio` и Protobuf)

Для внутренней (east-west) связи между микросервисами в Python используют
официальный пакет **`grpcio`** (обёртка над C-ядром `gRPC Core`) или чисто
асинхронную библиотеку **`grpclib`**.

### Особенности эксплуатации gRPC в Python

- **Обязательное использование `grpc.aio` в асинхронных сервисах.** Классический
  синхронный `grpc.server(futures.ThreadPoolExecutor(...))` блокирует потоки.
  Если ваш сервис использует `asyncio` (например, ходит в БД через `asyncpg` и
  в кэш через `redis.asyncio`), поднимайте сервер и каналы через модуль
  `grpc.aio`:

```python
import grpc
from grpc import aio

# Повторно используйте один aio-канал (он мультиплексирует HTTP/2 стримы)!
channel = aio.insecure_channel(
    "pricing-service:50051",
    options=[
        ("grpc.keepalive_time_ms", 30_000),
        ("grpc.keepalive_timeout_ms", 5_000),
    ],
)
```

- **Кодогенерация с типами (`mypy-protobuf`).** Сам по себе компилятор
  `grpc_tools.protoc` генерирует динамический Python-код, в котором IDE и
  `mypy` не видят типов полей сообщений. В продакшн-пайплайне обязательно
  добавляйте плагин `--mypy_out=` и `--mypy_grpc_out=` (пакет `mypy-protobuf`),
  который создаёт `.pyi` стабы для строгой статической проверки контрактов.
- **Производительность:** поскольку парсинг бинарного Protobuf и работа с HTTP/2
  в `grpcio` вынесены в C/C++ расширение (C++ расширение `upb` в свежих версиях
  `protobuf`), Python тратит значительно меньше процессорного времени и памяти
  на мелких частых межсервисных вызовах, чем при JSON over HTTP/1.1.

---

## 3. GraphQL в Python (`Strawberry`) и проблема N+1 в резолверах

В современном Python стандартом де-факто для GraphQL стал фреймворк
**`Strawberry`** — он построен на стандартных аннотациях типов и синтаксисе
`@dataclass`, бесшовно встраиваясь в FastAPI/ASGI.

### Главная архитектурная ловушка: N+1 запросов в `async def` резолверах

Если клиент запрашивает список из 50 заказов и для каждого просит вложенное
поле `user { name }`, наивный резолвер выполнит 1 запрос за заказами и 50
отдельных запросов за пользователями:

```python
import strawberry
from strawberry.dataloader import DataLoader
from uuid import UUID


# Загрузчик пачками (batching): собирает все ID за один тик event loop
# и делает ОДИН SQL-запрос WHERE id IN (...) или один батч-запрос в сервис
async def load_users_batch(keys: list[UUID]) -> list["UserType"]:
    users_by_id = await fetch_users_by_ids(keys)  # 1 запрос вместо N
    return [users_by_id[k] for k in keys]


@strawberry.type
class UserType:
    id: strawberry.ID
    name: str


@strawberry.type
class OrderType:
    id: strawberry.ID
    user_id: strawberry.Private[UUID]

    @strawberry.field
    async def user(self, info: strawberry.Info) -> UserType:
        loader: DataLoader[UUID, UserType] = info.context["user_loader"]
        return await loader.load(self.user_id)
```

**Правило:** в Python GraphQL-сервисе объект `DataLoader` создаётся **на каждый
HTTP-запрос** (внутри `context_getter`), чтобы его in-memory кэш жил только в
рамках одного запроса и не протекал между разными пользователями.

---

## 4. API Gateway и BFF в архитектуре Python-приложений

Как показано в рабочем примере [маршрутизации API
Gateway](../../03_distributed_components/02_examples/03_api_gateway_routing/main.py),
периметр системы отделяет сквозные инфраструктурные задачи (аутентификацию,
лимиты, маршрутизацию) от бизнес-сервисов. В экосистеме Python действует чёткое
разделение ролей:

1. **Инфраструктурный API Gateway НЕ пишут на Python.** Терминацию TLS,
   проверку подписи JWT, глобальный Rate Limiting и L7-маршрутизацию выполняют
   высокопроизводительные прокси на C/Go/Rust (**Envoy, Kong, Nginx, Traefik**).
   Делать проксирование сырого трафика через Python-процесс бессмысленно из-за
   накладных расходов GIL и памяти на парсинг каждого HTTP-пакета.
2. **BFF (Backend for Frontend) отлично ложится на Python (FastAPI /
   Strawberry).** Задача BFF — параллельно опросить 3–4 внутренних сервиса по
   gRPC/HTTP (`asyncio.TaskGroup`), склеить и отфильтровать данные под
   конкретный экран мобильного или веб-приложения. Это чисто I/O-bound задача
   оркестрации, с которой асинхронный Python справляется идеально.

| Сценарий в Python-стеке | Выбор инструмента и протокола |
| :--- | :--- |
| Публичный API для браузеров, мобильных клиентов и внешних партнёров | **REST + JSON** на **FastAPI + Pydantic v2 + `orjson`** (автогенерация OpenAPI/Swagger из типов Python) |
| Склейка данных из нескольких микросервисов под сложный UI (BFF) | **FastAPI** (REST BFF) или **Strawberry GraphQL** + `DataLoader` + `httpx.AsyncClient` / `grpc.aio` |
| Внутренние синхронные вызовы с жёсткими требованиями к latency и типизации | **gRPC (`grpc.aio`) + Protobuf + `mypy-protobuf`** |
| Передача больших табличных/аналитических выборок между Python-сервисами | **Apache Arrow Flight** (zero-copy передача датафреймов `Polars`/`pandas` поверх gRPC без построчной сериализации) |

---

## 5. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** В каком случае переход с REST/JSON на gRPC между двумя
> Python-сервисами НЕ даст заметного ускорения?
>
> **Ответ:** Если время ответа сервиса определяется медленным SQL-запросом
> (например, 80 мс в БД) и небольшим JSON-ответом на 1 КБ (сериализация в
> `orjson` занимает микросекунды). В этом случае замена транспорта сэкономит
> менее 1 мс и не устранит реальное узкое место. Переход на gRPC в Python даёт
> кратный выигрыш тогда, когда вызовов между сервисами много (высокий RPS),
> пейлоады крупные и строго типизированные, требуется потоковая передача
> (`stream`) или мультиплексирование по одному HTTP/2 соединению, а также
> жёсткий контракт `.proto` между командами на разных языках (Python ↔ Go/Rust).

> **Вопрос:** Почему нельзя создать один глобальный экземпляр `DataLoader` при
> старте FastAPI/Strawberry приложения и переиспользовать его во всех запросах?
>
> **Ответ:** `DataLoader` не только группирует вызовы в батчи в рамках одного
> тика event loop, но и мемоизирует (кэширует в `dict`) загруженные объекты по
> ключу на всё время своей жизни. Глобальный `DataLoader` приведёт к двум
> критическим багам: 1) бесконечной утечке памяти в воркере Uvicorn;
> 2) подаче устаревших и чужих данных разным пользователям в последующих
> HTTP-запросах.

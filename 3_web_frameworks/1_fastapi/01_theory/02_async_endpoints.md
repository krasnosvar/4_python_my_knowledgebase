# Асинхронные эндпоинты: `async def` vs `def`

FastAPI позволяет объявлять роуты и как `async def`, и как обычный `def`. Разница
между ними — не синтаксическая, а про то, как именно код выполняется под капотом,
и цена ошибки здесь выше, чем кажется на первый взгляд.

## Как это устроено под капотом

FastAPI построен на Starlette и работает поверх одного event loop (asyncio, через
`anyio`). Когда приходит запрос:

- если роут объявлен как `async def`, обработчик выполняется прямо в event loop;
- если роут объявлен как обычный `def`, FastAPI сам оборачивает вызов и исполняет
  его в отдельном потоке из threadpool, не блокируя event loop.

Это ключевой момент: `def`-роуты не выполняются "синхронно и блокирующе" в смысле
всего приложения — FastAPI уводит их в поток специально, чтобы не мешать
остальным запросам.

## Когда `async def` действительно даёт выгоду

Async-код выгоден, когда внутри эндпоинта есть **I/O-bound ожидание**, и это
ожидание выполняется через `await` над действительно асинхронной библиотекой:

- запросы к другим сервисам через `httpx.AsyncClient`;
- запросы к БД через асинхронный драйвер (`asyncpg`, `asyncmy`, `motor` и т.п.);
- работа с очередями, кэшами, файлами через асинхронные клиенты.

Пока один запрос ждёт ответа от сети, event loop свободен и может обслуживать
другие запросы. Это даёт большую пропускную способность при большом количестве
одновременных I/O-bound запросов — без раздувания числа потоков.

```python
import httpx
from fastapi import APIRouter

router = APIRouter()


@router.get("/weather/{city}")
async def get_weather(city: str) -> dict:
    async with httpx.AsyncClient() as client:
        # await отдаёт управление event loop на время сетевого ожидания
        response = await client.get(f"https://example.com/weather/{city}")
        response.raise_for_status()
        return response.json()
```

## Когда `async def` не помогает и даже вредит

Если внутри `async def`-эндпоинта вызывается **блокирующий синхронный код**
(CPU-bound работа или синхронный I/O без `await`), происходит худшее из
возможного: этот вызов блокирует единственный event loop целиком. Пока он не
завершится, ни один другой запрос в приложении не обслуживается — не только
текущий, а вообще все.

```python
import time
from fastapi import APIRouter

router = APIRouter()


# НЕПРАВИЛЬНО: синхронный sleep внутри async def
@router.get("/bad")
async def bad_endpoint() -> dict:
    time.sleep(2)  # блокирует event loop на 2 секунды для ВСЕХ запросов
    return {"status": "done"}


# НЕПРАВИЛЬНО: синхронный клиент requests внутри async def
@router.get("/bad-http")
async def bad_http_call() -> dict:
    import requests

    response = requests.get("https://example.com")  # блокирующий вызов
    return {"data": response.text}
```

Частые источники такой блокировки:
- `requests` вместо `httpx.AsyncClient` внутри `async def`;
- синхронный драйвер БД (`psycopg2`, обычный `pymysql`) внутри `async def`;
- тяжёлые вычисления (парсинг больших файлов, шифрование, сериализация) без
  вынесения в отдельный процесс/поток.

## Правильные варианты

Есть два корректных способа обработать медленную или тяжёлую операцию:

**1. Объявить роут как обычный `def`** — тогда FastAPI сам уведёт вызов в
threadpool, и блокирующий код не остановит event loop:

```python
import time
from fastapi import APIRouter

router = APIRouter()


# ПРАВИЛЬНО: def-роут уходит в threadpool, event loop не блокируется
@router.get("/sync-ok")
def sync_ok_endpoint() -> dict:
    time.sleep(2)  # блокирует только один поток из threadpool, не весь сервис
    return {"status": "done"}
```

**2. Если роут должен быть `async def`, а внутри есть блокирующий вызов** —
явно вынести его в threadpool через `run_in_threadpool` (или
`asyncio.to_thread` в чистом asyncio):

```python
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

router = APIRouter()


def cpu_bound_report(data: list[int]) -> dict:
    # тяжёлые вычисления, синхронная библиотека и т.п.
    return {"sum": sum(data)}


@router.post("/report")
async def build_report(data: list[int]) -> dict:
    # снимаем блокирующую работу с event loop
    result = await run_in_threadpool(cpu_bound_report, data)
    return result
```

## Почему "плохой async def" опаснее, чем плохой def

Если в `def`-роуте написан медленный синхронный код — пострадает только
threadpool: он ограничен по размеру, но другие запросы либо встанут в очередь
на поток, либо (если это `async def`-запросы) продолжат обрабатываться в
event loop без изменений.

Если аналогичный медленный код попадает в `async def` — блокируется сам
event loop, а на нём завязаны вообще все `async def`-запросы во всём
приложении. Один неудачный `async def` с блокирующим вызовом внутри способен
уронить пропускную способность всего сервиса.

## Практическое правило

- Есть реальный `await` над асинхронной библиотекой (asyncpg, httpx.AsyncClient,
  асинхронный Redis-клиент и т.п.) — используй `async def`.
- Используешь синхронную библиотеку (requests, psycopg2, тяжёлые вычисления) —
  используй обычный `def` или явно оборачивай в `run_in_threadpool`.
- Сомневаешься — безопаснее выбрать `def`: FastAPI сам изолирует блокировку в
  threadpool, а не в event loop.

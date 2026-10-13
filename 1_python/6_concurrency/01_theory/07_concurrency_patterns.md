# Паттерны конкурентного ввода-вывода

## Rate limiting (ограничение скорости)

Два разных смысла «ограничить» — не путать:

- **Ограничение параллелизма** («не больше N одновременно») — `asyncio.Semaphore`.
- **Ограничение частоты во времени** («не больше N в секунду») — нужен
  собственный token bucket / интервал между вызовами.

```python
import asyncio, time

class RateLimiter:
    """Не больше `rate` вызовов в секунду (простой token bucket)."""
    def __init__(self, rate: float):
        self._interval = 1.0 / rate
        self._lock = asyncio.Lock()
        self._next_allowed = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            wait = self._next_allowed - now
            if wait > 0:
                await asyncio.sleep(wait)
            self._next_allowed = max(now, self._next_allowed) + self._interval
```

Ограничение параллелизма (семафор) и ограничение частоты (rate limiter)
часто нужны вместе: семафор бережёт локальные ресурсы (сокеты), rate
limiter — уважает лимиты внешнего API.

## Фоновые задачи (fire-and-forget)

Частая ошибка — потерять ссылку на задачу:

```python
asyncio.create_task(background_job())  # плохо: ссылка потеряна, GC может собрать задачу
```

Правильный паттерн — держать ссылки в множестве и убирать по завершении:

```python
background_tasks: set[asyncio.Task] = set()

def spawn(coro) -> asyncio.Task:
    task = asyncio.create_task(coro)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return task
```

Так задача не будет собрана сборщиком мусора преждевременно, а после
завершения не останется висеть в множестве. Важно также обрабатывать
исключения фоновой задачи — без `await`/проверки они молча теряются (кроме
предупреждения в логах о «Task exception was never retrieved»):

(`logging` — стандартный модуль для записи сообщений в лог вместо
`print`; подробно — в `7_standard_library/01_theory/07_logging_basics.md`.)

```python
def _log_exception(task: asyncio.Task) -> None:
    if not task.cancelled() and task.exception() is not None:
        logging.exception("background task failed", exc_info=task.exception())

task.add_done_callback(_log_exception)
```

## Graceful shutdown фоновых задач

```python
async def shutdown(tasks: set[asyncio.Task]) -> None:
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
```

`return_exceptions=True` здесь обязателен — иначе `CancelledError` от
отменённых задач всплывёт как исключение самого `gather`.

## Конкурентная работа с файлами

Стандартный `open()`/`read()`/`write()` — блокирующие системные вызовы.
Внутри asyncio их либо выносят в executor (`run_in_executor`), либо
используют сторонние библиотеки (`aiofiles`), которые под капотом делают
то же самое. Для скрипта, не встроенного в event loop, проще и быстрее
использовать `ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

async def read_many(paths: list[str]) -> list[str]:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=8) as pool:
        return await asyncio.gather(
            *(loop.run_in_executor(pool, read_file, p) for p in paths)
        )
```

## Конкурентная работа с сетью

Для сетевого I/O с нуля пишут на `asyncio.open_connection` /
`asyncio.start_server`, но в реальных проектах почти всегда используют
готовые async-библиотеки (`aiohttp`, `httpx` с `AsyncClient`, драйверы БД
`asyncpg`/`motor`), которые уже умеют кооперативно отдавать управление на
I/O. Общий шаблон конкурентных сетевых запросов с ограничением
параллелизма:

```python
async def fetch_all(urls: list[str], concurrency: int = 20) -> list[str]:
    sem = asyncio.Semaphore(concurrency)

    async def fetch_one(url: str) -> str:
        async with sem:
            async with session.get(url) as resp:
                return await resp.text()

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(fetch_one(u) for u in urls))
```

## Таймауты

`asyncio.wait_for` (до 3.11) и `asyncio.timeout` (3.11+, context manager)
— оборачивают корутину так, что при превышении времени она отменяется:

```python
async def with_timeout():
    async with asyncio.timeout(5):
        await slow_operation()
    # если slow_operation не уложилась в 5 секунд — TimeoutError
```

`asyncio.timeout` предпочтительнее `wait_for` в новом коде: работает и с
группами задач (`TaskGroup` внутри `timeout`), корректно отменяет всё
дерево вложенных awaitable, а не только верхний вызов.

## Общий чеклист паттернов

- Всегда ограничивайте параллелизм явно (`Semaphore`, `max_workers`) —
  «безлимитный» `gather` на 100 000 элементов может исчерпать файловые
  дескрипторы или упереться в лимиты внешнего сервиса.
- Всегда держите ссылки на фоновые задачи и логируйте их исключения.
- Всегда оборачивайте сетевые операции таймаутом — без него зависшее
  соединение блокирует ресурс навсегда.
- Не смешивайте блокирующий синхронный код с asyncio без `run_in_executor`.

# concurrent.futures: пулы потоков и процессов

`concurrent.futures` — единый высокоуровневый API поверх `threading` и
`multiprocessing`: одинаковый интерфейс `Executor.submit`/`map`, разная
реализация под капотом.

## ThreadPoolExecutor

Пул ОС-потоков, переиспользуемых между задачами (без накладных расходов на
создание потока на каждую задачу). Годится для I/O-bound работы, когда нет
async-варианта библиотеки (например, синхронный `requests`, драйвер БД без
async-поддержки):

```python
from concurrent.futures import ThreadPoolExecutor

def fetch(url: str) -> str:
    return requests.get(url).text  # синхронная блокирующая библиотека

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(fetch, url) for url in urls]
    results = [f.result() for f in futures]
```

- `max_workers` — верхняя граница одновременных потоков. Для I/O-bound
  можно ставить больше числа ядер CPU (потоки в основном ждут, а не считают).
- `pool.map(fetch, urls)` — короче, но результаты нельзя обработать по мере
  готовности (аналог `gather`, а не `as_completed`); для этого — `as_completed`
  из `concurrent.futures` (не путать с asyncio-версией — это разные функции
  с похожими именами).

## ProcessPoolExecutor

Пул процессов — то же API, но для CPU-bound работы, обходит GIL:

```python
from concurrent.futures import ProcessPoolExecutor

def is_prime(n: int) -> bool:
    if n < 2: return False
    return all(n % i for i in range(2, int(n ** 0.5) + 1))

with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(is_prime, big_list_of_numbers))
```

- `max_workers` по умолчанию = `os.cpu_count()` — больше обычно бессмысленно
  для чистого CPU-bound, если только задачи не имеют I/O-фазы.
- Аргументы и результат должны быть picklable (передаются между процессами
  через сериализацию) — нельзя передать, например, открытый сокет,
  генератор или локальную функцию с замыканием на неспециализируемые объекты.
- Издержки старта процесса и сериализации данных значимы: для мелких
  быстрых задач `ProcessPoolExecutor` может быть медленнее последовательного
  кода — имеет смысл при заметной вычислительной работе на задачу.

## run_in_executor — мост между asyncio и блокирующим кодом

Главная проблема: в event loop нельзя вызвать блокирующую функцию напрямую
— она остановит весь loop. `loop.run_in_executor` выполняет её в пуле
потоков/процессов и возвращает `awaitable`, не блокируя event loop:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def main():
    loop = asyncio.get_running_loop()

    # блокирующий синхронный вызов в отдельном потоке, не блокируя event loop
    text = await loop.run_in_executor(None, requests.get, url)  # None = default ThreadPoolExecutor

    # тяжёлые вычисления — в отдельном процессе
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_heavy_function, data)
```

- `None` в качестве executor — использует loop'овский дефолтный
  `ThreadPoolExecutor`.
- Для CPU-bound работы внутри async-приложения (например, обработка
  изображения в веб-хендлере) `run_in_executor` с `ProcessPoolExecutor` —
  стандартный способ не блокировать остальные запросы, пока считается один.
- `functools.partial` пригождается, чтобы передать функцию с
  keyword-аргументами (`run_in_executor` принимает только позиционные).
  `partial(f, a, x=1)` создаёт новую функцию, в которой часть аргументов
  `f` уже «подставлена заранее» (подробнее — в
  `7_standard_library/01_theory/02_functools_itertools_extra.md`):

```python
from functools import partial
await loop.run_in_executor(None, partial(fetch, url, timeout=5))
```

## Когда какой executor

| Ситуация | Executor |
|---|---|
| Синхронная I/O-библиотека без async-версии, много вызовов | `ThreadPoolExecutor` |
| Тяжёлые вычисления внутри синхронного скрипта | `ProcessPoolExecutor` |
| Тяжёлые вычисления внутри asyncio-приложения (не блокировать event loop) | `run_in_executor(ProcessPoolExecutor, ...)` |
| Блокирующий синхронный вызов внутри asyncio-приложения | `run_in_executor(None, ...)` (thread pool) |

## Отличие от «чистого» threading/multiprocessing

`concurrent.futures` не даёт ничего принципиально нового поверх
`threading`/`multiprocessing` — это удобный API с пулом и объектом
`Future` (аналог `asyncio.Future`, но синхронный: `.result()` блокирует
вызывающий поток до готовности). В большинстве кода стоит начинать именно
с `concurrent.futures`, а к «сырым» `threading.Thread`/`multiprocessing.Process`
обращаться только когда нужен нестандартный контроль жизненного цикла.

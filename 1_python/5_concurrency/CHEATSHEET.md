# Конкурентность — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.
Версии указаны там, где поведение зависит от них.

## Что выбрать

Подробно: [02_threading_vs_multiprocessing_vs_asyncio.md](./01_theory/02_threading_vs_multiprocessing_vs_asyncio.md).

| Нагрузка | Инструмент | Почему |
| :--- | :--- | :--- |
| Много сетевых/дисковых ожиданий, есть async-библиотеки | `asyncio` | один поток, тысячи задач, дешёвое переключение |
| I/O через синхронную библиотеку (`requests`, драйвер без async) | `ThreadPoolExecutor` / `threading` | GIL отпускается на время I/O |
| Тяжёлые вычисления на чистом Python | `ProcessPoolExecutor` / `multiprocessing` | свой GIL в каждом процессе, реальный параллелизм |
| Вычисления + общий state без дорогого IPC | numpy / C-расширение / другой алгоритм | потоки упрутся в GIL, процессы — в `pickle` |
| CPU-часть внутри asyncio-сервиса | `loop.run_in_executor(ProcessPoolExecutor(), f, x)` | не блокировать event loop |
| Блокирующий вызов внутри asyncio | `await asyncio.to_thread(f, x)` (3.9+) или `run_in_executor(None, f, x)` | то же, в пуле потоков |

| | `threading` | `multiprocessing` | `asyncio` |
| :--- | :--- | :--- | :--- |
| Единица | поток ОС | процесс ОС | задача (`Task`) в одном потоке |
| Параллелизм по CPU | нет (GIL) | да | нет |
| Переключение | вытесняющее (~5 мс, `sys.getswitchinterval()`) и на I/O | ОС | только в `await` |
| Память | общая → нужен `Lock` | раздельная → `pickle` аргументов | общая, гонки только через `await` |
| Масштаб | десятки–сотни | ≈ число ядер | тысячи–десятки тысяч |

## GIL и версии

Подробно: [01_gil_and_execution_model.md](./01_theory/01_gil_and_execution_model.md).

| Факт | Детали |
| :--- | :--- |
| GIL | Python-байткод выполняет один поток за раз |
| Атомарность | отдельная инструкция байткода — да; `counter += 1` — нет, нужен `Lock` |
| Кто отпускает GIL | блокирующие системные вызовы (`socket.recv`, `file.read`, `time.sleep`), C-расширения (numpy) |
| Per-interpreter GIL | 3.12 (PEP 684); в 3.14 — `concurrent.interpreters` и `InterpreterPoolExecutor` |
| Free-threaded сборка | 3.13 экспериментально, 3.14 официально поддерживается (`python3.14t`), но не по умолчанию |
| Start method на Linux | `fork` до 3.13, `forkserver` с 3.14; macOS/Windows — `spawn` (`mp.get_start_method()`) |

## asyncio API

Подробно: [03_asyncio_event_loop_coroutines.md](./01_theory/03_asyncio_event_loop_coroutines.md),
[05_running_many_coroutines.md](./01_theory/05_running_many_coroutines.md),
[07_concurrency_patterns.md](./01_theory/07_concurrency_patterns.md).

| Задача | Код |
| :--- | :--- |
| Точка входа | `asyncio.run(main())` (не из работающего loop — `RuntimeError`) |
| Вызвать корутину последовательно | `result = await coro()` |
| Запустить конкурентно | `task = asyncio.create_task(coro())` — держать ссылку! |
| Дождаться N штук, результаты по порядку | `await asyncio.gather(*coros)` |
| Ошибки как значения | `await asyncio.gather(*coros, return_exceptions=True)` |
| Результаты по мере готовности | `for c in asyncio.as_completed(coros): r = await c` |
| Группа с отменой при ошибке (3.11+) | `async with asyncio.TaskGroup() as tg: tg.create_task(...)` |
| Ловить ошибки группы | `except* ValueError as eg: eg.exceptions` |
| Таймаут (3.11+) | `async with asyncio.timeout(5): ...` → `TimeoutError` |
| Таймаут (любая версия) | `await asyncio.wait_for(coro(), 5)` |
| Отменить задачу | `task.cancel()` → `CancelledError` в точке `await` |
| Отдать управление | `await asyncio.sleep(0)` |
| Текущий loop | `asyncio.get_running_loop()` |
| Блокирующий вызов в потоке | `await asyncio.to_thread(f, *args)` (3.9+) |
| То же в своём пуле | `await loop.run_in_executor(pool, f, *args)`; kwargs — через `functools.partial` |

| Способ | Порядок результатов | При ошибке |
| :--- | :--- | :--- |
| `gather()` | как в аргументах | первая ошибка всплывает, остальные **не отменяются** |
| `gather(return_exceptions=True)` | как в аргументах | ошибки — элементы списка |
| `as_completed()` | по готовности | ошибка всплывает при `await` конкретного элемента |
| `TaskGroup` (3.11+) | собирать вручную (`task.result()`) | остальные задачи отменяются, ошибки — в `ExceptionGroup` |

```python
import asyncio

async def fetch(n: int, sem: asyncio.Semaphore) -> int:
    async with sem:                        # не больше 2 одновременно
        await asyncio.sleep(0.1)
        return n * 2

async def main() -> None:
    sem = asyncio.Semaphore(2)
    async with asyncio.timeout(5):         # 3.11+
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch(i, sem)) for i in range(4)]
    print([t.result() for t in tasks])     # [0, 2, 4, 6]

asyncio.run(main())
```

## Примитивы синхронизации

Подробно: [04_asyncio_sync_primitives.md](./01_theory/04_asyncio_sync_primitives.md).

| Нужно | asyncio (корутины одного loop) | Потоки |
| :--- | :--- | :--- |
| Взаимное исключение | `async with asyncio.Lock():` | `with threading.Lock():` |
| Не больше N одновременно | `asyncio.Semaphore(N)` | `threading.Semaphore(N)` |
| Разбудить всех ожидающих | `asyncio.Event()`: `await e.wait()` / `e.set()` | `threading.Event()` |
| Ждать условия с `notify()` | `asyncio.Condition()` | `threading.Condition()` |
| Producer/consumer | `asyncio.Queue(maxsize=N)`: `await q.put()`, `await q.get()`, `q.task_done()`, `await q.join()` | `queue.Queue` |

Между процессами — `multiprocessing.Queue`, а не `queue.Queue`.

## Executors

Подробно: [06_concurrent_futures_and_executors.md](./01_theory/06_concurrent_futures_and_executors.md).

| Задача | Код |
| :--- | :--- |
| Пул потоков | `with ThreadPoolExecutor(max_workers=10) as pool:` |
| Пул процессов | `with ProcessPoolExecutor() as pool:` (`max_workers` по умолчанию — число CPU) |
| Отправить задачу | `fut = pool.submit(f, x)`; `fut.result()` блокирует до готовности |
| Применить ко всем, результаты по порядку | `list(pool.map(f, items))` |
| Результаты по готовности | `concurrent.futures.as_completed(futures)` (не путать с asyncio-версией) |

```python
from concurrent.futures import ProcessPoolExecutor

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % i for i in range(2, int(n ** 0.5) + 1))

if __name__ == "__main__":                  # обязателен для spawn/forkserver
    with ProcessPoolExecutor() as pool:
        print(list(pool.map(is_prime, [2, 15, 17, 21])))   # [True, False, True, False]
```

## Фоновые задачи и shutdown

```python
import asyncio

background_tasks: set[asyncio.Task] = set()

def spawn(coro) -> asyncio.Task:
    task = asyncio.create_task(coro)
    background_tasks.add(task)                       # сильная ссылка, иначе GC
    task.add_done_callback(background_tasks.discard)
    return task

async def shutdown(tasks: set[asyncio.Task]) -> None:
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
```

| Ограничить | Чем |
| :--- | :--- |
| Число одновременных операций | `asyncio.Semaphore(N)` / `max_workers` |
| Частоту (N в секунду) | свой token bucket (`RateLimiter` в [07_concurrency_patterns.md](./01_theory/07_concurrency_patterns.md)) |
| Время операции | `asyncio.timeout(...)` / `wait_for(...)` |

## Ловушки

- ⚠️ `threading` для CPU-bound → не быстрее одного потока, иногда медленнее.
- ⚠️ `async def` с чистыми вычислениями не ускоряется: без `await` нет переключения.
- ⚠️ `time.sleep`, `requests.get`, `queue.Queue.get`, `threading.Lock` внутри корутины блокируют весь event loop.
- ⚠️ Корутину вызвали без `await` → тело не выполнилось, `RuntimeWarning: coroutine ... was never awaited`.
- ⚠️ `await a(); await b()` — последовательно; конкурентно — `create_task`/`gather`/`TaskGroup`.
- ⚠️ `create_task` без сохранённой ссылки → задачу может собрать GC.
- ⚠️ Check-then-act с `await` посередине → гонка даже в asyncio; нужен `asyncio.Lock`.
- ⚠️ `asyncio.Lock` и `threading.Lock` не реентерабельны: повторный захват в той же задаче/потоке → deadlock.
- ⚠️ Проглотили `CancelledError` → отмена не дошла до вызывающего; для очистки — `try/finally`.
- ⚠️ `gather` без `return_exceptions` после первой ошибки оставляет остальные задачи работать.
- ⚠️ Исключение фоновой задачи без `await`/callback → только «Task exception was never retrieved» в логе.
- ⚠️ Безлимитный `gather` на 100 000 запросов → кончатся дескрипторы или лимиты API.
- ⚠️ В `ProcessPoolExecutor` лямбды, генераторы, сокеты не передать — не сериализуются `pickle`.
- ⚠️ Мелкие задачи в `ProcessPoolExecutor` медленнее последовательного кода из-за старта процессов и `pickle`.

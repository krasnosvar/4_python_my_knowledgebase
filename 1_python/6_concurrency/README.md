# Тема 6. Конкурентность (Concurrency)

GIL, threading, multiprocessing, asyncio: когда что использовать, как
устроен event loop, синхронизация, конкурентный запуск задач, executors и
практические паттерны конкурентного I/O. Самый большой раздел базы —
конкурентность в Python имеет больше нюансов, чем в языках без GIL.

## Зачем этот раздел

Типичный бэкенд-сервис большую часть времени не считает, а **ждёт**:
ответа БД, другого API, диска. Если обрабатывать запросы строго по одному,
сервис простаивает во время каждого ожидания. Конкурентность позволяет в
это время обслуживать другие запросы — от этого зависит, выдержит ли
сервис сотни одновременных пользователей. После раздела вы сможете
осознанно выбрать между потоками, процессами и asyncio под конкретную
задачу, писать async-код (на нём построены FastAPI, aiokafka и др. из
следующих разделов) и не попадать в типичные ловушки: блокирующий вызов в
event loop, гонки данных, потерянные фоновые задачи.

Раздел начинается с объяснения простыми словами, что такое процесс, поток
и конкурентность, — заранее знать это не нужно.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — что выбрать (threading / multiprocessing / asyncio), API asyncio, примитивы, executors, ловушки.

## Что нужно знать заранее

- [3_functions_and_decorators](../3_functions_and_decorators/README.md) —
  функции как значения и контекст-менеджеры (`with lock:`, `async with`).
- [4_oop](../4_oop/README.md) — классы (примитивы синхронизации и
  executors — это объекты с методами).
- [5_iterators_generators](../5_iterators_generators/README.md) — корутины
  исторически выросли из генераторов, `send()` поможет понять `await`.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория (порядок важен):
  - [01_gil_and_execution_model.md](./01_theory/01_gil_and_execution_model.md)
    — процесс, поток, конкурентность vs параллелизм; что такое GIL и его
    следствия для CPU- и I/O-bound кода.
  - [02_threading_vs_multiprocessing_vs_asyncio.md](./01_theory/02_threading_vs_multiprocessing_vs_asyncio.md)
    — таблица решений «что выбрать», к которой удобно возвращаться.
  - [03_asyncio_event_loop_coroutines.md](./01_theory/03_asyncio_event_loop_coroutines.md)
    — `async def`/`await`, event loop и корутины изнутри, отмена задач.
  - [04_asyncio_sync_primitives.md](./01_theory/04_asyncio_sync_primitives.md)
    — `Lock`, `Semaphore`, `Event`, `Queue` (и их threading-аналоги).
  - [05_running_many_coroutines.md](./01_theory/05_running_many_coroutines.md)
    — `gather`/`as_completed`/`TaskGroup`.
  - [06_concurrent_futures_and_executors.md](./01_theory/06_concurrent_futures_and_executors.md)
    — `concurrent.futures` и `run_in_executor`.
  - [07_concurrency_patterns.md](./01_theory/07_concurrency_patterns.md) —
    rate limiting, фоновые задачи, конкурентный I/O с файлами и сетью.
- **[02_examples/](./02_examples/)** — 10 runnable-примеров, по одному на
  ключевую тему.
- **[03_exercises/](./03_exercises/)** — 8 упражнений с `TODO`, от
  threading/multiprocessing до `TaskGroup` и rate limiter'а.
- **[04_exercises_answers/](./04_exercises_answers/)** — готовые решения.

## Как проходить

1. Начать с `01_gil_and_execution_model.md` — без понимания GIL решения
   «threading или multiprocessing» выглядят как магия.
2. Прочитать `02_threading_vs_multiprocessing_vs_asyncio.md` — таблица
   решений, к которой удобно возвращаться.
3. Разобрать asyncio по порядку: event loop → примитивы синхронизации →
   способы конкурентного запуска → executors → паттерны.
4. Пройти упражнения по порядку — они калибруются по той же прогрессии.

## Запуск примеров и упражнений

```bash
python 02_examples/03_asyncio_basics/main.py
python 03_exercises/03_asyncio_fetch_many/main.py
```

Требуется Python 3.11+ (используется `asyncio.TaskGroup` и `except*`).

## Когда двигаться дальше

Когда можете для конкретной задачи обоснованно выбрать threading,
multiprocessing или asyncio, объяснить, почему блокирующий вызов внутри
`async def` останавливает весь сервис, и ограничить параллелизм через
`Semaphore`, — переходите к [7_standard_library](../7_standard_library/README.md).

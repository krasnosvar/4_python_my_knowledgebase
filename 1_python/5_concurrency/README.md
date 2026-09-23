# Concurrency в Python

GIL, threading, multiprocessing, asyncio: когда что использовать, как
устроен event loop, синхронизация, конкурентный запуск задач, executors и
практические паттерны конкурентного I/O. Самый большой раздел базы —
конкурентность в Python имеет больше нюансов, чем в языках без GIL.

## Структура

- `01_theory/` — GIL и его следствия; выбор между threading/multiprocessing/
  asyncio; event loop и корутины изнутри; примитивы синхронизации asyncio
  (и их threading-аналоги); способы конкурентного запуска корутин
  (`gather`/`as_completed`/`TaskGroup`); `concurrent.futures` и
  `run_in_executor`; паттерны (rate limiting, background tasks, конкурентный
  I/O с файлами и сетью).
- `02_examples/` — 10 runnable-примеров, по одному на ключевую тему.
- `03_exercises/` — 8 упражнений с `TODO`, от threading/multiprocessing до
  `TaskGroup` и rate limiter'а.
- `04_exercises_answers/` — готовые решения.

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

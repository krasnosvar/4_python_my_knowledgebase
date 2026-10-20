# Тема 02. Производительность и масштабирование (Performance and Scaling)

## О чём эта тема (краткий контекст)

Производительность и масштабируемость системы строятся на поиске самого узкого
звена на пути запроса (bottleneck), системном профилировании задержек (p95/p99)
и насыщения ресурсов, многоуровневом кэшировании (CDN, L1 в памяти процесса,
L2 Redis) и горизонтальном разделении нагрузки на вычислительные узлы и базы
данных (репликация и шардирование). Без измерения узких мест добавление новых
серверов лишь увеличивает счета за инфраструктуру и перегружает реальное
бутылочное горлышко (чаще всего базу данных).

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Узкие места и методология системного профилирования](../../../5_devops_sre_knowledgebase/14_system_design/02_performance_caching_and_scaling/01_theory/01_bottlenecks_and_profiling_methodology.md)
> - [Уровни и паттерны кэширования, вытеснение и аномалии кэша](../../../5_devops_sre_knowledgebase/14_system_design/02_performance_caching_and_scaling/01_theory/02_caching_levels_and_patterns.md)
> - [Вертикальное и горизонтальное масштабирование высоконагруженных систем](../../../5_devops_sre_knowledgebase/14_system_design/02_performance_caching_and_scaling/01_theory/03_scaling_high_load_systems.md)
> - [Репликация, шардирование, CAP/PACELC и распределённые данные](../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/01_data_replication_sharding_and_cap.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки).

## Зачем этот раздел

Здесь вы разберёте, как масштабировать и ускорять именно Python-бэкенд: как GIL
влияет на выбор числа воркеров Gunicorn/Uvicorn и почему один блокирующий вызов
роняет p99 всего `asyncio`-сервиса, как профилировать продакшн через `py-spy` и
`tracemalloc`, почему локальный кэш `lru_cache` умножает память между
pre-fork воркерами и как защитить Redis от Cache Stampede через `asyncio.Lock`,
а также как настроить Read/Write Splitting и роутинг по шардам в SQLAlchemy и
Django.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — формулы воркеров
WSGI/ASGI, диагностика блокировок Event Loop, ловушки L1-кэша в Gunicorn и
маршрутизация шардов в SQLAlchemy/Django.

## Что нужно знать заранее

- Тема [01_architecture_styles](../01_architecture_styles/).
- Устройство GIL, потоков, процессов и `asyncio` из
  [5_concurrency](../../1_python/5_concurrency/), а также основы SQL и Redis из
  [2_data_and_messaging](../../2_data_and_messaging/).

## Структура раздела

- **[01_theory/](./01_theory/)** — теория с фокусом на специфику Python:
  - [01_gil_bottlenecks_and_profiling.md (урок
    01)](./01_theory/01_gil_bottlenecks_and_profiling.md)
    — влияние GIL на CPU-bound и I/O-bound нагрузку, расчёт числа воркеров
    Gunicorn и Uvicorn, блокировка `asyncio` Event Loop (`to_thread` vs
    `ProcessPoolExecutor`) и профилирование в продакшене (`py-spy`,
    `tracemalloc`, `slow_callback_duration`).
  - [02_caching_in_python.md](./01_theory/02_caching_in_python.md) — локальный
    L1-кэш (`lru_cache`, `cachetools.TTLCache`), ловушка умножения памяти и
    рассинхрона между воркерами Gunicorn, двухуровневый кэш L1 + L2
    (`redis.asyncio`) и защита от Cache Stampede через `asyncio.Lock`.
  - [03_sharding_and_data_scaling_in_python.md (урок
    03)](./01_theory/03_sharding_and_data_scaling_in_python.md)
    — маршрутизация чтения и записи (Leader / Read Replica) с защитой
    Read-Your-Writes через `contextvars`, прикладной роутинг по шардам в
    SQLAlchemy (`Session.get_bind`) и Django (`DatabaseRouter`), ловушка
    рандомизации `hash()` в CPython.
- **[02_examples/](./02_examples/)** — runnable-примеры на чистом Python:
  - [01_bottleneck_pipeline](./02_examples/01_bottleneck_pipeline/main.py) —
    конвейер из трёх стадий: пропускная способность всей системы ограничена
    самой медленной стадией.
  - [02_scaling_tradeoffs](./02_examples/02_scaling_tradeoffs/main.py) — закон
    Амдала: как доля последовательной работы ограничивает ускорение при
    масштабировании.
  - [03_consistent_hashing](./02_examples/03_consistent_hashing/main.py) —
    сравнение наивного `hash(key) % N` и кольца Consistent Hashing при
    добавлении нового шарда.
- **[03_exercises/](./03_exercises/)** — сценарии системного дизайна для
  письменного разбора:
  - [01_find_the_bottleneck](./03_exercises/01_find_the_bottleneck.md) — найти
    реальное узкое место по метрикам пути запроса (Locust).
  - [02_scale_out_or_up](./03_exercises/02_scale_out_or_up.md) — выбрать схему
    масштабирования для stateless API на FastAPI и CPU-bound транскодера с
    учётом GIL.
  - [03_shard_the_dataset](./03_exercises/03_shard_the_dataset.md) — выбрать
    ключ шардирования и оценить влияние на типовые запросы и транзакции.
  - [04_cache_layers_design](./03_exercises/04_cache_layers_design.md) —
    спроектировать уровни кэширования (CDN / L1 / L2) под разную степень
    персонализации.
- **[04_exercises_answers/](./04_exercises_answers/)** — разобранные
  рассуждения по тем же сценариям.

## Как проходить

1. Изучите базовую теорию в каноническом разделе DevOps (по ссылкам в начале
   уроков) и прочитайте уроки в [01_theory/](./01_theory/).
2. Запустите примеры из `02_examples/`:
   ```bash
   python3 ./02_examples/01_bottleneck_pipeline/main.py
   python3 ./02_examples/02_scaling_tradeoffs/main.py
   python3 ./02_examples/03_consistent_hashing/main.py
   ```
3. Проработайте сценарии в [03_exercises/](./03_exercises/) письменно, прежде
   чем сверяться с [04_exercises_answers/](./04_exercises_answers/).

## Когда двигаться дальше

Когда вы понимаете, как GIL и модель воркеров влияют на масштабирование Python,
умеете находить блокировки Event Loop через `py-spy`, проектировать связку L1 +
L2 кэша и маршрутизировать запросы между репликами и шардами в ORM — переходите
к [03_distributed_components](../03_distributed_components/).

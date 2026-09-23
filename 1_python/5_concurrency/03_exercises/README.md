# Упражнения: concurrency

Запуск задания: `python 03_exercises/01_threading_word_count/main.py`

Ответы: `python 04_exercises_answers/01_threading_word_count_answers/main.py`

1. `01_threading_word_count` — I/O-bound задача на threading.
2. `02_multiprocessing_prime_check` — CPU-bound задача на multiprocessing.
3. `03_asyncio_fetch_many` — конкурентный запуск корутин через gather.
4. `04_semaphore_limited_downloads` — ограничение параллелизма через Semaphore.
5. `05_producer_consumer_queue` — producer/consumer на asyncio.Queue.
6. `06_taskgroup_error_handling` — TaskGroup и ExceptionGroup (3.11+).
7. `07_executor_bridge_cpu_task` — run_in_executor с ProcessPoolExecutor.
8. `08_rate_limited_api_client` — rate limiter поверх конкурентных вызовов.

# Производительность и масштабирование в Python — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/) и каноническом разделе
[DevOps System Design](../../../5_devops_sre_knowledgebase/14_system_design/02_performance_caching_and_scaling/).
⚠️ — типичная ошибка в Python-проектах, которая дорого обходится.

## Воркеры, GIL и профилирование в Python

Подробнее: [GIL, узкие места и
профилирование](./01_theory/01_gil_bottlenecks_and_profiling.md)

| Задача / Нагрузка | Рекомендация для Python |
| :--- | :--- |
| Число воркеров для синхронного WSGI (`gunicorn` sync/gthread) | `2 * CPU_CORES + 1` (перекрывает простой потоков на блокирующем I/O) |
| Число воркеров для асинхронного ASGI (`uvicorn`) | **`1 воркер на 1 vCPU`** (в K8s — 1 процесс на под и масштабирование через HPA) |
| Короткий блокирующий I/O или C-вызов, отпускающий GIL (`boto3`, `bcrypt`) в `async def` | `await asyncio.to_thread(func, *args)` |
| Тяжёлый расчёт на чистом Python (держит GIL) в `async def` | `await loop.run_in_executor(process_pool, func, *args)` или вынос в **Celery** |
| Найти, кто блокирует `asyncio` Event Loop | `loop.slow_callback_duration = 0.03` + `py-spy record --pid <PID> --gil` |
| Найти утечку памяти в объектах Python | Сравнение снимков кучи через `tracemalloc.take_snapshot().compare_to(...)` |

Закон Амдала — предел ускорения при последовательной доле `1 - p`:

```python
def speedup(p, n):
    return 1 / ((1 - p) + p / n)


print(
    round(speedup(0.9, 10), 2),
    round(speedup(0.9, 100), 2),
    round(speedup(0.9, 10**6), 2),
)
# 5.26 9.17 10.0  — при p = 0.9 больше 10x не получить
```

## Уровни кэша в Python (L1 + L2 Redis)

Подробнее: [02_caching_in_python.md](./01_theory/02_caching_in_python.md)

| Уровень в Python-стеке | Инструмент | Особенности и ограничения |
| :--- | :--- | :--- |
| **L1 (in-process)** | `cachetools.TTLCache`, `functools.lru_cache`, `async-lru` | ~0.5 мкс, но **размножается на каждый процесс Gunicorn** ($N \times \text{RAM}$) и не синхронизирован между воркерами |
| **L2 (distributed)** | `redis.asyncio` + сериализация в `orjson` / `msgpack` | ~0.5–1 мс, единый для всех воркеров и подов, переживает рестарт приложения |
| **Защита от Stampede** | `defaultdict(asyncio.Lock)` по ключу + Redis Lock | Гарантирует, что при промахе кэша только одна корутина пойдёт в PostgreSQL |

## Масштабирование БД: Реплики и Шарды в ORM

Подробнее: [Шардирование и масштабирование данных в
Python](./01_theory/03_sharding_and_data_scaling_in_python.md)

| Задача | Реализация в SQLAlchemy / Django |
| :--- | :--- |
| Read/Write Splitting (Leader / Replica) | Переопределение `Session.get_bind()` в SQLAlchemy или `DatabaseRouter` (`db_for_read` / `db_for_write`) в Django |
| Read-Your-Writes после мутации | Флаг `recent_write:{user_id}` в Redis на 3 сек + `contextvars.ContextVar`, направляющий чтение в `primary` |
| Вычисление номера шарда по ключу | Только детерминированный хэш: `zlib.crc32(key.encode()) % N` или Consistent Hashing (`hashlib.md5`/`sha256`) |

```python
# Наивный hash % N: доля ключей, сменивших шард при N=4 → N=5
moved = sum(1 for k in range(100_000) if k % 4 != k % 5)
print(moved / 100_000)  # 0.8
```

## Типичные ошибки в Python

- ⚠️ Вызывать `requests.get()`, `time.sleep()` или тяжёлый `json.loads()`
  внутри `async def` → замораживает весь Event Loop воркера и взвинчивает p99.
- ⚠️ Навешивать `@lru_cache` на методы экземпляра класса (утечка памяти через
  ссылку на `self`) или на `async def` (кэшируется одноразовый объект корутины).
- ⚠️ Держать большой L1-кэш при 8–16 воркерах Gunicorn → `OOMKilled` и разные
  ответы от разных воркеров.
- ⚠️ Использовать встроенный `hash(key) % N` для роутинга по шардам → из-за
  `PYTHONHASHSEED` разные воркеры отправят данные одного клиента в разные БД.
- ⚠️ Сериализовать объекты в Redis через `pickle` вместо `orjson`/`msgpack` →
  риск RCE и падение при переименовании классов в новом релизе.

# Celery — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая
ошибка, которая теряет задачи, дублирует эффект или блокирует запрос.
Проверено на Celery 5.6.

## Компоненты

Подробно: [01_architecture.md](./01_theory/01_architecture.md).

| Компонент | Роль | Обычно |
| :--- | :--- | :--- |
| Broker | очередь сообщений «имя задачи + аргументы» | Redis, RabbitMQ (сильнее гарантии доставки) |
| Worker | отдельный процесс: забирает и выполняет задачи | `celery -A app worker` |
| Result backend | статус (`PENDING`/`STARTED`/`SUCCESS`/`FAILURE`) и результат по `task_id` | Redis или БД |
| Beat | планировщик: только **кладёт** задачи по расписанию | `celery -A app beat` |

Поток: API кладёт задачу → сразу отвечает `202 Accepted` + `task_id` →
worker выполняет → пишет результат → клиент опрашивает по `task_id`.

## Команды

| Задача | Команда |
| :--- | :--- |
| Запустить worker | `celery -A app.celery_app worker --loglevel=info` |
| Worker только для своей очереди | `celery -A app.celery_app worker -Q fast --concurrency=8` |
| Отдельный пул для тяжёлых задач | `celery -A app.celery_app worker -Q heavy --concurrency=2` |
| Запустить планировщик | `celery -A app.celery_app beat --loglevel=info` |

## Задачи и вызов

Подробно: [02_tasks_queues_retry.md](./01_theory/02_tasks_queues_retry.md).

| Задача | Как |
| :--- | :--- |
| Объявить | `@app.task` над функцией |
| Поставить в очередь по умолчанию | `add.delay(2, 3)` |
| Отложить на N секунд | `add.apply_async(args=(2, 3), countdown=10)` |
| Не раньше времени | `apply_async(..., eta=datetime(...))` |
| В конкретную очередь | `apply_async(..., queue="fast")` |
| Маршрутизация по имени задачи | `app.conf.task_routes = {"app.tasks.add": {"queue": "fast"}}` |
| Статус / результат | `result.status` / `result.get(timeout=5)` |

- ⚠️ `result.get()` в HTTP-обработчике снова блокирует запрос — только в скриптах, тестах.
- ⚠️ Worker должен импортировать модуль с задачами: в сообщении лежит имя задачи, не функция.
- ⚠️ Быстрые и тяжёлые задачи в одной очереди — тяжёлая блокирует десятки лёгких.

## Retry и надёжность

| Параметр `@app.task(...)` | Что делает |
| :--- | :--- |
| `bind=True` | первым аргументом приходит `self` (нужен для `self.retry`, `self.request.retries`) |
| `autoretry_for=(ConnectionError,)` | автоматический повтор на этих исключениях |
| `retry_backoff=True` | экспоненциальная задержка 1, 2, 4, 8... с |
| `retry_backoff_max=60` | потолок задержки, с |
| `max_retries=5` | максимум повторов |
| `acks_late=True` | подтверждать сообщение после выполнения, а не при получении: упавший worker → задачу подхватит другой |

```python
from celery import Celery

app = Celery("demo")
app.conf.task_always_eager = True   # только для локальной проверки: без брокера

@app.task(bind=True, max_retries=3)
def fetch_data(self, url: str) -> dict:
    try:
        return http_get(url)
    except TimeoutError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

- ⚠️ Retry = тело может выполниться несколько раз → задача обязана быть идемпотентной (проверка состояния, idempotency key в той же транзакции, `UPSERT`, абсолютные значения вместо инкремента).
- ⚠️ `retry_backoff` не забывать: мгновенные повторы добивают и так лежащий внешний сервис.

## Расписание (beat)

Подробно: [03_periodic_tasks_beat.md](./01_theory/03_periodic_tasks_beat.md).

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    "cleanup-every-night": {
        "task": "app.tasks.cleanup_expired_sessions",
        "schedule": crontab(hour=3, minute=0),   # каждый день в 03:00
    },
    "heartbeat-every-30s": {
        "task": "app.tasks.heartbeat",
        "schedule": 30.0,                        # интервал в секундах
    },
}
```

- ⚠️ Beat не запущен → расписание молча не работает, даже если worker жив.
- ⚠️ Beat ставит задачу в очередь по времени, но не ждёт завершения предыдущей и не гарантирует время выполнения.

## Celery или хватит фоновой задачи в процессе

Подробно: [04_when_celery_vs_overkill.md](./01_theory/04_when_celery_vs_overkill.md).

| Критерий | `asyncio.create_task` / FastAPI `BackgroundTasks` | Celery |
| :--- | :--- | :--- |
| Длительность | доли секунды — единицы секунд | долго, CPU-bound, медленные внешние API |
| Потеря при рестарте/деплое | допустима | неприемлема (письмо о заказе, списание) |
| Retry, backoff | писать руками | из коробки |
| Масштабирование | вместе с веб-процессом | отдельные worker-пулы, другие машины |
| Расписание | нет | `celery beat` |
| Наблюдаемость (статус, результат) | писать руками | result backend, `task_id` |
| Инфраструктура | ничего | брокер + worker'ы (+ beat) |

Правило: «задача молча пропала при деплое — это страшно?» Нет →
`BackgroundTasks`/`asyncio`. Да → Celery (персистентная очередь).

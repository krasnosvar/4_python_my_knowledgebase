# Отказоустойчивость, Health Checks и Graceful Shutdown в Python

## О чём эта тема (краткий контекст)

В распределённой системе сеть ненадёжна, а соседние сервисы и базы данных
периодически замедляются, перезапускаются или падают. Чтобы частичный сбой
одного узла не вызывал каскадное падение всей платформы, сервисы защищают
четырьмя эшелонами обороны: алгоритмами балансировки нагрузки и проверками
здоровья (Liveness и Readiness probes), жёсткими таймаутами на каждый сетевой
вызов, умными повторными попытками (Retries с Exponential Backoff & Jitter),
предохранителями (Circuit Breaker, Rate Limiting, Bulkhead) и корректным
завершением процесса при деплое (Graceful Shutdown).

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Балансировка нагрузки, Health Checks и паттерны отказоустойчивости](../../../../5_devops_sre_knowledgebase/14_system_design/03_distributed_components_and_data/01_theory/03_load_balancing_and_resilience_patterns.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки). Рабочие симуляции алгоритмов
> балансировки, реестра с heartbeat и API Gateway на чистом Python доступны в
> [`02_examples/`](../02_examples/).

---

## 1. Таймауты в Python (`asyncio.timeout` и `httpx.Timeout`)

Первое правило надёжного Python-сервиса: **ни один сетевой вызов не имеет права
выполняться без таймаута.** В стандартной библиотеке `urllib` и популярном
пакете `requests` таймаут по умолчанию равен `None` (бесконечность) — один
зависший TCP-сокет навечно хоронит поток воркера.

### Двухуровневая защита в современном Python (3.11+)

1. **Транспортный таймаут в `httpx.Timeout`:** раздельно задаёт время на
   установку TCP-соединения (`connect`), чтение очередного чанка (`read`),
   отправку (`write`) и ожидание свободного коннекта в пуле (`pool`).
2. **Общий дедлайн на всю бизнес-операцию через `asyncio.timeout()` (Python
   3.11+):** ограничивает суммарное время выполнения блока (даже если сервер
   присылает по 1 байту раз в секунду и не триггерит `read` таймаут):

```python
import asyncio
import httpx

HTTP_TIMEOUT = httpx.Timeout(connect=0.5, read=1.5, write=1.0, pool=0.5)


async def fetch_Order_status(client: httpx.AsyncClient, order_id: str) -> dict:
    # Жёсткий дедлайн 2.0 секунды на весь блок, включая чтение тела и парсинг
    async with asyncio.timeout(2.0):
        resp = await client.get(
            f"http://billing-svc/v1/orders/{order_id}",
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
```

---

## 2. Retries с Exponential Backoff & Jitter (`tenacity`)

Повторять упавший запрос немедленно (`for _ in range(3): client.get(...)`) в
распределённой системе опасно: если соседний сервис перегружен, мгновенные
повторы от всех воркеров утроят нагрузку на него (Retry Storm) и не дадут ему
подняться.

В экосистеме Python стандартом для повторных попыток является библиотека
**`tenacity`**. Правильная конфигурация включает:
- **Экспоненциальную задержку со случайным разбросом**
  (`wait_random_exponential`) — размазывает повторы во времени (Jitter);
- **Строгий фильтр исключений** — ретраить можно только сетевые сбои и `502 /
  503 / 504`, но никогда не `400 / 401 / 404 / 422`;
- **Обязательную идемпотентность** (передачу `Idempotency-Key` для `POST`).

```python
import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    # Full Jitter: случайная пауза от 0 до min(2.0, 0.1 * 2^attempt) секунд
    wait=wait_random_exponential(multiplier=0.1, max=2.0),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
)
async def call_partner_api(
    client: httpx.AsyncClient, payload: dict, idempotency_key: str
) -> dict:
    resp = await client.post(
        "https://partner.example/charge",
        json=payload,
        headers={"Idempotency-Key": idempotency_key},
    )
    if resp.status_code in (502, 503, 504):
        resp.raise_for_status()
    return resp.json()
```

Для защиты от каскадных отказов поверх ретраев ставят **Circuit Breaker**
(библиотеки `pybreaker`, `aiobreaker` или на уровне Service Mesh / Envoy): при
достижении порога ошибок цепь размыкается (`OPEN`), и вызовы мгновенно падают
с локальным исключением без обращения к сети.

---

## 3. Liveness (`/healthz`) и Readiness (`/readyz`) в FastAPI и Django

Как показано в примере [`main.py` (Service
Registry)](../02_examples/02_service_registry_health_checks/main.py),
оркестратор (Kubernetes) и балансировщик задают сервису два принципиально
разных вопроса:

1. **Liveness (`/healthz`) — «Жив ли процесс Python и не застрял ли его Event
   Loop навечно?»**
   - Если `/healthz` не отвечает, Kubernetes **убивает и перезапускает под**.
   - **Критическое правило:** в `/healthz` **категорически запрещено** ходить в
     PostgreSQL, Redis или внешние сервисы! Если БД моргнула на 3 секунды, а
     ваш `/healthz` делает `SELECT 1`, Kubernetes одновременно убьёт все 20
     подов вашего сервиса.
2. **Readiness (`/readyz`) — «Готов ли этот конкретный инстанс прямо сейчас
   принимать пользовательский трафик?»**
   - Если `/readyz` вернул `503`, под **НЕ перезапускается**, а просто временно
     исключается из балансировки (`Endpoints`), пока БД или кэш не вернутся в
     строй.

```python
from fastapi import FastAPI, Response, status
from sqlalchemy import text

app = FastAPI()


@app.get("/healthz")
async def liveness_probe() -> dict:
    # Проверяет только то, что процесс жив и asyncio event loop не завис
    return {"status": "alive"}


@app.get("/readyz")
async def readiness_probe(response: Response) -> dict:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready"}
```

---

## 4. Корректный Graceful Shutdown в Uvicorn, Gunicorn и Celery

При каждом деплое новой версии или масштабировании Kubernetes посылает процессу
сигнал **`SIGTERM`**. Если процесс просто умрёт в ту же миллисекунду, все
выполняющиеся в этот момент запросы оборвутся с ошибкой `502 Bad Gateway`, а
транзакции оборвутся посередине.

### Порядок Graceful Shutdown для Python веб-сервиса (ASGI / FastAPI)

1. При получении `SIGTERM` под параллельно удаляется из списка активных
   эндпоинтов балансировщика Kubernetes, но из-за асинхронного распространения
   правил `iptables`/`IPVS` новые запросы могут прилетать ещё **2–5 секунд**.
   Поэтому в Kubernetes задают `preStop` хук (`sleep 5`) перед отправкой
   `SIGTERM` в Uvicorn.
2. Uvicorn перестаёт принимать новые соединения и ждёт завершения текущих
   корутин (лимит задаётся флагом **`--timeout-graceful-shutdown 15`** в
   Uvicorn и **`--graceful-timeout 20`** в Gunicorn).
3. Когда все активные HTTP-запросы завершились, выполняется код **после `yield`
   в контекстном менеджере `lifespan`**: закрываются `httpx.AsyncClient`,
   сбрасываются буферы кафка-продюсера и вызывается `await engine.dispose()`
   для закрытия соединений с PostgreSQL.

### Graceful Shutdown и защита от потери задач в Celery

По умолчанию воркер Celery подтверждает получение задачи из брокера **сразу в
момент вычитки** (`acks_late=False`). Если во время долгой задачи прилетит
`SIGTERM` и по истечении `terminationGracePeriodSeconds` под будет убит через
`SIGKILL`, задача исчезнет навсегда.

Для надёжных идемпотентных задач в Python включают три настройки:

```python
celery_app.conf.update(
    task_acks_late=True,             # ACK в брокер только ПОСЛЕ выполнения
    task_reject_on_worker_lost=True,  # вернуть в очередь при внезапной гибели
    worker_prefetch_multiplier=1,    # не набирать пачку задач в память впрок
)
```

---

## 5. Типовые вопросы на собеседовании (Python System Design)

> **Вопрос:** Разработчик написал единый эндпоинт `/health`, который проверяет
> соединение с PostgreSQL, Redis и внешним платёжным шлюзом, и прописал его и в
> `livenessProbe`, и в `readinessProbe` в Kubernetes. Что произойдёт, когда
> внешний платёжный шлюз начнёт отвечать с задержкой 5 секунд?
>
> **Ответ:** Каскадный самострел всей системы. Провал `livenessProbe` заставит
> kubelet убивать и перезапускать поды один за другим (CrashLoopBackOff). Даже
> те эндпоинты сервиса, которые вообще не связаны с платёжным шлюзом (просмотр
> каталога, профиль), станут полностью недоступны, а при старте новые поды
> создадут шторм подключений к PostgreSQL. В `livenessProbe` должен быть только
> мгновенный `/healthz` без внешних вызовов, а в `readinessProbe` — проверка
> только собственных критических инфраструктурных зависимостей (БД).

> **Вопрос:** Почему при обычном редеплое FastAPI в Kubernetes пользователи
> иногда видят единичные ошибки `502 Bad Gateway`, хотя в Uvicorn настроен
> `--timeout-graceful-shutdown`?
>
> **Ответ:** Когда Kubernetes удаляет под, он делает две вещи **одновременно и
> асинхронно**: 1) отправляет `SIGTERM` процессу внутри контейнера; 2) удаляет
> IP пода из объекта `Endpoints`, откуда его забирают `kube-proxy` и Ingress
> контроллер. Если Uvicorn получил `SIGTERM` на миллисекунду раньше и сразу
> закрыл слушающий сокет, а Ingress ещё 1–2 секунды продолжает слать новые
> запросы на этот IP, они получат `Connection refused` (`502`). Лечится
> добавлением `lifecycle.preStop.exec.command: ["sh", "-c", "sleep 5"]` или
> переводом `/readyz` в `503` на 5 секунд перед закрытием сокета.

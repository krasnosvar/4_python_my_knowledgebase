# Примитивы синхронизации: asyncio и threading

У `asyncio` есть свой набор примитивов синхронизации — они **не потокобезопасны**
и не взаимозаменяемы с `threading`-версиями: `asyncio.Lock` нельзя использовать
для защиты данных между потоками, а `threading.Lock` внутри корутины
заблокирует весь event loop (это блокирующий вызов).

## Почему в asyncio вообще нужны блокировки

Раз переключение возможно только в точках `await`, гонки по данным без
`await` внутри критической секции не бывает. Но она возможна, если между
проверкой состояния и его изменением есть `await`:

```python
balance = 100

async def withdraw(amount: int):
    global balance
    if balance >= amount:
        await asyncio.sleep(0)  # искусственная точка переключения (например, поход в БД)
        balance -= amount       # к этому моменту другая корутина могла уже списать
```

Если две корутины одновременно вызовут `withdraw(80)` при `balance == 100`,
обе пройдут проверку `if balance >= amount`, обе спишут — баланс уйдёт в минус.
Это классическая гонка «check-then-act», и `await asyncio.sleep(0)` между
проверкой и действием — ровно та точка, где event loop может передать
управление другой задаче.

## asyncio.Lock

```python
lock = asyncio.Lock()

async def withdraw(amount: int):
    async with lock:
        global balance
        if balance >= amount:
            await asyncio.sleep(0)
            balance -= amount
```

Не re-entrant (повторный `acquire` в той же задаче — deadlock, как и
`threading.Lock`).

## asyncio.Semaphore

Ограничивает число одновременных «держателей» (не 0/1, а N):

```python
sem = asyncio.Semaphore(5)  # не больше 5 одновременных операций

async def fetch(url: str):
    async with sem:
        return await http_get(url)
```

Классический пример — ограничение параллельных сетевых запросов, чтобы не
перегрузить сервер или локальный пул соединений (rate limiting «по числу
одновременных», не «по времени» — см. паттерны).

## asyncio.Event

Флаг «сигнал уже подан / ещё не подан» — способ разбудить множество
ожидающих задач одновременно:

```python
event = asyncio.Event()

async def waiter():
    await event.wait()   # спит, пока флаг не установлен
    print("proceed")

async def setter():
    await asyncio.sleep(1)
    event.set()          # будит всех, кто ждёт wait()
```

В отличие от `Lock`, `Event` не про взаимное исключение, а про
широковещательное уведомление («готовность наступила»).

## asyncio.Condition

`Lock` + возможность ждать произвольного условия и получать точечные
`notify()`/`notify_all()` — аналог `threading.Condition`. Нужен реже,
обычно `Queue` решает те же задачи проще.

## asyncio.Queue — конкурентный producer/consumer

```python
queue: asyncio.Queue[int] = asyncio.Queue(maxsize=10)

async def producer():
    for i in range(100):
        await queue.put(i)   # блокируется, если очередь полна (backpressure)
    await queue.put(None)     # sentinel — сигнал consumer'у остановиться

async def consumer():
    while (item := await queue.get()) is not None:
        process(item)
        queue.task_done()
```

`maxsize` — естественный backpressure: producer не убежит вперёд
consumer'а бесконтрольно. `task_done()` + `await queue.join()` в producer'е
— способ дождаться, пока все элементы обработаны, без sentinel-значений.

## Таблица: asyncio vs threading аналоги

| asyncio | threading | Отличие |
|---|---|---|
| `asyncio.Lock` | `threading.Lock` | asyncio-версия не блокирует поток ОС, только текущую корутину |
| `asyncio.Semaphore` | `threading.Semaphore` | тот же смысл, разный примитив ожидания |
| `asyncio.Event` | `threading.Event` | идентичная семантика set/wait |
| `asyncio.Condition` | `threading.Condition` | идентичная семантика, разный scheduler |
| `asyncio.Queue` | `queue.Queue` | `queue.Queue` — потокобезопасная блокирующая очередь для потоков/процессов; `asyncio.Queue` — кооперативная, для корутин одного event loop |

Важно не перепутать модули: `queue.Queue` из стандартной библиотеки — то,
что используется между `threading.Thread`, она **потокобезопасна** и
использует внутри `threading.Lock`/`Condition`. Использовать её в asyncio
корутине без обёртки нельзя — это блокирующий вызов, который остановит
event loop на время ожидания.

## Правило выбора

- Взаимное исключение над shared state внутри одного event loop → `asyncio.Lock`.
- Ограничение параллелизма (не более N одновременных операций) → `asyncio.Semaphore`.
- «Разбудить всех, когда что-то готово» → `asyncio.Event`.
- Producer/consumer с очередью работ → `asyncio.Queue`.
- То же самое, но между потоками ОС (не корутинами) → `threading.Lock` /
  `threading.Semaphore` / `threading.Event` / `queue.Queue`.

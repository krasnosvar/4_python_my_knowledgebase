# Брокеры сообщений (Kafka, RabbitMQ) — шпаргалка

Подробности — в [01_theory/](./01_theory/README.md). ⚠️ — частая ловушка.

## Зачем брокер

Подробнее: [01_why_message_brokers.md](./01_theory/01_why_message_brokers.md).

| Даёт | Цена |
| :--- | :--- |
| Decoupling: producer не знает consumer'ов | Ещё одна инфраструктура (кластер, мониторинг) |
| Буферизация пиков | Eventual consistency вместо мгновенной |
| Асинхронность: не ждать обработки | Думать о потерях и дублях |

## Kafka: партиции, группы, офсеты

Подробнее: [02_kafka_partitions.md](./01_theory/02_kafka_partitions.md),
[03_kafka_consumer_groups.md](./01_theory/03_kafka_consumer_groups.md),
[04_kafka_offsets.md](./01_theory/04_kafka_offsets.md).

| Понятие | Суть |
| :--- | :--- |
| Topic | Именованный поток событий, разбит на партиции |
| Партиция | Упорядоченный append-only лог; единица параллелизма |
| Брокер (в Kafka) | Один сервер кластера |
| Ключ сообщения | `hash(key) % num_partitions` → одна партиция для одного ключа |
| Без ключа | Round-robin / sticky — равномерно, без порядка |
| Consumer group (`group_id`) | Одну партицию в группе читает не более одного consumer'а |
| Разные группы | Читают тот же топик независимо |
| Offset | Номер сообщения внутри партиции (не глобальный) |
| Committed offset | Хранится в `__consumer_offsets`; с него стартует consumer после рестарта |
| Retention | Сообщения живут по сроку, а не до прочтения |

| Задача | Как |
| :--- | :--- |
| Порядок событий одного заказа | Ключ = `order_id` |
| Больше параллелизма чтения | Больше партиций (consumer'ов > партиций — лишние простаивают) |
| Перечитать историю (replay) | Сдвинуть committed offset назад / новая группа с `earliest` |
| Не терять при падении consumer'а | Manual commit **после** обработки |

- ⚠️ Порядок гарантирован только внутри партиции.
- ⚠️ Смена числа партиций меняет `hash(key) % N` — ключи переедут.
- ⚠️ Rebalance останавливает группу; обработка дольше `max.poll.interval.ms` выкидывает consumer'а.
- ⚠️ Auto-commit по таймеру может закоммитить необработанное → потеря.

## Гарантии доставки

Подробнее: [05_kafka_delivery_guarantees.md](./01_theory/05_kafka_delivery_guarantees.md).

| Семантика | Producer | Consumer | Когда |
| :--- | :--- | :--- | :--- |
| At-most-once | `acks=0` | Commit **до** обработки | Метрики, некритичные логи |
| At-least-once | `acks=all` + `retries > 0` | Commit **после** обработки + идемпотентный обработчик | Большинство бизнес-событий |
| Exactly-once | `enable.idempotence=true` + транзакции | `isolation.level=read_committed` | Только внутри Kafka (consume-transform-produce) |

- ⚠️ Exactly-once не распространяется на запись в БД/HTTP — там это снова at-least-once.
- Практичный рецепт: at-least-once + идемпотентность, например
  `INSERT ... ON CONFLICT (event_id) DO NOTHING`.

## RabbitMQ

Подробнее: [06_rabbitmq.md](./01_theory/06_rabbitmq.md).

| Exchange | Маршрутизация | Типичный случай |
| :--- | :--- | :--- |
| `direct` | `routing_key == binding_key` | Фиксированный набор каналов (`error`, `info`) |
| `topic` | Шаблон: `*` — ровно одно слово, `#` — ноль или больше | Подписка на срез: `orders.eu.*`, `orders.*.cancelled`, `orders.#` |
| `fanout` | Routing key игнорируется, во все очереди | Broadcast («конфиг обновился») |
| `headers` | Совпадение заголовков (`x-match: all` / `any`) | Многомерная маршрутизация, редко |

| Подтверждение | Результат |
| :--- | :--- |
| `ack` | Обработано, удалить из очереди |
| `nack`/`reject`, `requeue=True` | Вернуть в очередь ⚠️ при постоянной ошибке — busy loop |
| `nack`/`reject`, `requeue=False` | В DLX, если настроен; иначе сообщение потеряно |
| auto-ack | ⚠️ Упал посреди обработки — сообщение потеряно |

## DLQ и retry

Подробнее: [07_dlq_and_retry.md](./01_theory/07_dlq_and_retry.md).

| Задача | Kafka (код приложения) | RabbitMQ (конфигурация) |
| :--- | :--- | :--- |
| Отложенный повтор | Топики `orders-retry-1`, `orders-retry-2` с задержкой | Очередь `retry_queue_5s` с TTL, без consumer'ов, DLX → основной exchange |
| Финальная DLQ | Топик `orders-dlq` + причина ошибки | `x-dead-letter-exchange`, `x-dead-letter-routing-key` |
| Счётчик попыток | Заголовок в сообщении | Заголовок `x-death` или счётчик в сообщении |

Почему сообщение попадает в DLQ: исчерпан лимит попыток, истёк TTL,
переполнена очередь (`x-max-length`), явный reject.

```python
import random

def backoff(attempt: int, base: float = 1.0, cap: float = 60.0) -> float:
    """Пауза перед попыткой attempt (1, 2, ...): 1, 2, 4, 8 ... + jitter, не больше cap."""
    delay = base * 2 ** (attempt - 1)
    return min(cap, delay + random.uniform(0, delay * 0.1))

print([round(backoff(n)) for n in range(1, 6)])  # примерно [1, 2, 4, 8, 16]
```

- ⚠️ Retry «на месте» без паузы = head-of-line blocking: партиция/очередь встаёт.
- ⚠️ Не `time.sleep()` в цикле основной очереди — паузу делает retry-топик/очередь.

## Kafka vs RabbitMQ — что выбрать

Подробнее: [08_use_cases.md](./01_theory/08_use_cases.md),
[09_kafka_vs_rabbitmq.md](./01_theory/09_kafka_vs_rabbitmq.md).

| Критерий | Kafka | RabbitMQ |
| :--- | :--- | :--- |
| Модель | Лог, хранение по retention | Очередь, удаление после ack |
| Throughput | Очень высокий | Высокий, обычно ниже |
| Маршрутизация | Топик + партиция по ключу | direct / topic / fanout / headers |
| Replay | Да (сдвиг offset) | Нет |
| Порядок | Внутри партиции | Внутри очереди с одним consumer'ом |
| DLQ / retry | Паттерн в коде | Встроено (DLX + TTL) |
| Эксплуатация | Сложнее (KRaft/ZooKeeper, партиции) | Проще на малых масштабах |

| Нужно | Выбор |
| :--- | :--- |
| Перечитать историю за 30 дней новым сервисом | Kafka |
| Сотни тысяч сообщений/с, много независимых групп | Kafka |
| Агрегация логов, стриминговая аналитика | Kafka |
| Гибкая маршрутизация по многим критериям | RabbitMQ |
| Task queue: одна задача — один воркер, приоритет, TTL, DLQ | RabbitMQ |
| Маленькая команда без экспертизы по Kafka | RabbitMQ |
| Шина событий + task-queue в отдельных сервисах | Kafka + RabbitMQ вместе |

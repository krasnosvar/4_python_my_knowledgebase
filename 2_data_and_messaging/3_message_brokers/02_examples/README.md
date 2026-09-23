# Примеры: Kafka и RabbitMQ

Рабочие Python-примеры producer/consumer для обоих брокеров поверх локального
Docker Compose стенда. Перед запуском рекомендуется прочитать
`../01_theory/README.md` - примеры используют термины (партиция, consumer-группа,
exchange, routing key, DLX) без повторного объяснения.

## Структура

```
02_examples/
├── docker-compose.yml       # Kafka (KRaft) + Kafka UI + RabbitMQ (management)
├── requirements.txt         # aiokafka, pika
├── retry_with_backoff.py    # общий декоратор retry с экспоненциальным backoff
├── kafka/
│   ├── producer.py          # отправка сообщений с ключом в topic "orders"
│   └── consumer.py          # consumer-группа, manual commit offset'а
└── rabbitmq/
    ├── producer.py          # publish в topic exchange с разными routing key
    └── consumer.py          # wildcard-биндинг, manual ack, DLQ через DLX
```

## Запуск стенда

```bash
cd 02_examples
docker compose up -d
docker compose ps          # дождаться healthy у kafka и rabbitmq
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Проверить, что стенд поднялся:

- **Kafka UI** - http://localhost:8080 (список топиков, партиций, сообщений
  в реальном времени; topic `orders` появится сам после первого запуска
  producer'а, т.к. `KAFKA_AUTO_CREATE_TOPICS_ENABLE=true`);
- **RabbitMQ management UI** - http://localhost:15672 (логин/пароль:
  `guest`/`guest`); во вкладке Exchanges/Queues видно `orders_topic`,
  `eu_orders_queue`, `orders_dlx`, `eu_orders_dlq` после первого запуска
  `rabbitmq/consumer.py` (топология объявляется самим consumer'ом).

## Kafka: producer + consumer

```bash
# Терминал 1: consumer-группа (можно запустить несколько копий -
# партиции автоматически разделятся между ними, см. теорию 2.2)
python kafka/consumer.py

# Терминал 2: отправка сообщений
python kafka/producer.py
```

Что смотреть:

- в логе producer'а - `partition=N offset=M` для каждого сообщения. Сообщения
  с одинаковым `order_id` (ключ) всегда попадают в одну и ту же партицию -
  это видно, если сравнить partition у `order-1`/`created`, `order-1`/`paid`
  и `order-1`/`shipped`;
- в логе consumer'а - offset коммитится (в коде, не в консоли) только после
  строки "обработано" - т.е. после успешного завершения `process_order()`.
  Если остановить consumer через Ctrl+C сразу после "получено", но до
  "обработано", и запустить заново - это же сообщение будет прочитано повторно
  (at-least-once, см. теорию 2.3-2.4);
- в Kafka UI на вкладке Consumers видно committed offset группы
  `orders-processing-group` по каждой партиции.

## RabbitMQ: routing key + DLQ

```bash
# Терминал 1: consumer (объявляет топологию: exchange, очереди, DLX/DLQ)
python rabbitmq/consumer.py

# Терминал 2: отправка сообщений с разными routing key
python rabbitmq/producer.py
```

Что смотреть:

- consumer забиндил очередь `eu_orders_queue` с binding key `orders.eu.*` -
  в логе появятся только сообщения с routing key `orders.eu.created` и
  `orders.eu.shipped`, но НЕ `orders.us.created`/`orders.us.cancelled`
  (сравните с тем, что реально отправил producer - в его логе видны все 5
  сообщений, включая us-события, которые эта очередь не заберёт);
- последнее сообщение от producer'а (`order-BAD`, без поля `amount`)
  систематически проваливает обработку. В логе consumer'а видно 3 попытки
  с растущей паузой (retry-with-backoff), а затем - "уходит в DLQ";
- в RabbitMQ management UI на вкладке Queues у `eu_orders_dlq` появится
  1 сообщение - это и есть результат работы `x-dead-letter-exchange`,
  настроенного на основной очереди: RabbitMQ переложил сообщение сам,
  без отдельного кода "переслать в другую очередь".

## Остановка стенда

```bash
docker compose down          # остановить контейнеры, оставить volumes
docker compose down -v       # остановить и стереть данные (топики, очереди)
```

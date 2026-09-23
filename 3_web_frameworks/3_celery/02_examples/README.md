# Пример: минимальный Celery worker + Redis broker

Небольшое приложение из двух задач (`add`, `send_report`) и одной задачи с
retry (`flaky_external_call`), запускаемое через docker-compose: Redis как
broker и result backend, отдельный контейнер с worker-ом.

## Структура

```
app/
  celery_app.py   # инстанс Celery, конфигурация, маршрутизация задач по очередям
  tasks.py        # сами задачи
docker-compose.yml
Dockerfile
requirements.txt
demo_client.py    # скрипт для постановки задач в очередь и чтения результата
```

## Запуск

```bash
cd 02_examples
docker compose up -d --build
docker compose ps
```

Проверить, что worker поднялся и слушает очереди:

```bash
docker compose logs -f worker
```

В логе должна быть строка вида `celery@... ready.`

## Отправка задач

Redis проброшен на `localhost:6379`, поэтому `demo_client.py` можно запускать
прямо с хоста (нужны установленные `celery`/`redis`, например через
`pip install -r requirements.txt` в локальном venv):

```bash
python demo_client.py
```

Ожидаемый вывод:

```
add task id: <uuid>
add result: 5
send_report task id: <uuid>
статус сразу после отправки: PENDING
send_report result: report-for-user-42-sent
```

`send_report` искусственно "спит" 5 секунд — это видно и в выводе клиента
(результат приходит не мгновенно), и в логах worker-а:

```bash
docker compose logs -f worker
```

## Проверка retry

`flaky_external_call` настроена на автоматический retry при
`ConnectionError` (см. `app/tasks.py` и `01_theory/02_tasks_queues_retry.md`).
Чтобы увидеть retry в деле, обратитесь к `03_exercises/01_retry_task/` —
там задача, которая реально иногда бросает исключение, и полная демонстрация
retry-цикла в логах worker-а.

## Остановка

```bash
docker compose down
```

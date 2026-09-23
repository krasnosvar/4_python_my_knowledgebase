# Упражнения

Оба упражнения используют общий Celery-инстанс из `02_examples/app/celery_app.py`
(через Redis из `02_examples/docker-compose.yml`). Прежде чем начинать,
поднимите стенд:

```bash
cd ../02_examples
docker compose up -d --build
```

Затем возвращайтесь сюда и правьте код упражнений — worker в контейнере
монтирует только `02_examples/app`, поэтому для проверки задач из упражнений
проще всего скопировать/подключить файл задачи во временный worker или
запускать worker локально (`celery -A ... worker`) с адресом брокера
`redis://localhost:6379/0`, указывая на нужный модуль. Каждое упражнение
объясняет это отдельно в своём README.md.

- [`01_retry_task/`](./01_retry_task/) — задача с retry и экспоненциальным backoff.
- [`02_periodic_task/`](./02_periodic_task/) — периодическая задача через `celery beat`.

Решения — в `../04_exercises_answers/`.

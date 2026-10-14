# Тема 3. Celery

## Зачем эта тема

HTTP-запрос должен отвечать за доли секунды, а часть работы — отправка
писем, генерация отчётов, обработка файлов, вызовы медленных внешних API
— занимает секунды или минуты. Celery позволяет вынести такую работу из
запроса в отдельные процессы-воркеры через очередь сообщений. После темы
ты сможешь поставить задачу в очередь из веб-приложения, настроить
повторы при ошибках и периодические задачи — и, что не менее важно,
понять, когда Celery не нужен и хватит простого фонового `asyncio`.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — команды, `delay`/`apply_async`, retry, beat, Celery vs `BackgroundTasks`.

## Что нужно знать заранее

- Docker и Docker Compose из
  [0_tooling_and_workflow/02_docker_basics](../../0_tooling_and_workflow/02_docker_basics/).
- Представление о брокерах сообщений из
  [2_data_and_messaging/3_message_brokers](../../2_data_and_messaging/3_message_brokers/)
  и о Redis из [2_data_and_messaging/2_redis](../../2_data_and_messaging/2_redis/).

## Структура темы

- **[01_theory/](./01_theory/)** — теория, читать по порядку:
  1. [01_architecture.md](./01_theory/01_architecture.md) — зачем
     выносить работу из запроса; broker, worker, result backend.
  2. [02_tasks_queues_retry.md](./01_theory/02_tasks_queues_retry.md) —
     задачи, очереди, повторы при ошибках.
  3. [03_periodic_tasks_beat.md](./01_theory/03_periodic_tasks_beat.md)
     — задачи по расписанию через Celery Beat.
  4. [04_when_celery_vs_overkill.md](./01_theory/04_when_celery_vs_overkill.md)
     — когда Celery оправдан, а когда избыточен.
- **[02_examples/](./02_examples/)** — worker + Redis в docker-compose и
  клиент, ставящий задачи.
- **[03_exercises/](./03_exercises/)** — задача с retry и backoff,
  периодическая задача.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные
  решения.

## Как проходить тему

1. Прочитать теорию по порядку.
2. Поднять стенд по [02_examples/README.md](./02_examples/README.md) и
   запустить `demo_client.py`.
3. Выполнить упражнения из `03_exercises/` (условия — в их README),
   сверить с `04_exercises_answers/`.

## Когда двигаться дальше

Когда ты можешь поставить задачу в очередь, настроить для неё retry с
экспоненциальным backoff, запустить периодическую задачу через `celery beat`
и объяснить, когда хватит фонового `asyncio` — переходи к
[4_stack_comparison](../4_stack_comparison/).

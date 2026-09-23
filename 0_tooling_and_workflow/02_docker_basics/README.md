# Тема 02. Docker — базовые вещи о контейнеризации

Минимум, достаточный для локальной разработки: чем образ отличается от
контейнера, из чего состоит `Dockerfile`, как поднять приложение с базой
через `docker-compose`, и какие грабли встречаются чаще всего.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_images_and_containers.md](./01_theory/01_images_and_containers.md) —
    образы vs контейнеры, слои и кэш сборки, базовые команды
    (`run`/`exec`/`logs`/`ps`).
  - [02_dockerfile_basics.md](./01_theory/02_dockerfile_basics.md) —
    инструкции Dockerfile, `CMD` vs `ENTRYPOINT`, shell vs exec form,
    `.dockerignore`, multi-stage builds.
  - [03_compose_and_commands.md](./01_theory/03_compose_and_commands.md) —
    `docker-compose.yml`, сети между сервисами, volumes (named vs bind
    mount).
- **[02_examples/](./02_examples/)** — рабочий минимальный пример:
  FastAPI-приложение (`app/`), однослойный `Dockerfile`,
  `Dockerfile.multistage`, `.dockerignore` и `docker-compose.yml` с
  сервисом Postgres. Все файлы собраны и проверены — можно запускать как
  есть:
  ```bash
  cd 02_examples
  docker compose up -d --build
  curl http://localhost:8000/
  docker compose down -v
  ```
- **[03_exercises/](./03_exercises/)** — 3 практические задачи с
  автопроверкой `PASS`/`FAIL` через `check.sh` (реально собирает образы и
  поднимает контейнеры).
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения
  со скриптами `solve.sh`.

## Как проходить тему

1. Прочитать теорию по порядку — `01_theory/01` → `02` → `03`.
2. Собрать и запустить пример из `02_examples/` (см. команды выше), затем
   собрать `Dockerfile.multistage` и сравнить размер образов:
   ```bash
   docker build -t demo -f Dockerfile .
   docker build -t demo-multi -f Dockerfile.multistage .
   docker images | grep demo
   ```
3. Выполнить упражнения из `03_exercises/` — для каждого: прочитать
   `TASK.md`, внести изменения, довести `bash check.sh` до всех `PASS`.
4. Сверить решение с `04_exercises_answers/`.

Для всех упражнений и примеров нужен установленный и запущенный Docker
(Docker Desktop или Docker Engine + `docker compose` plugin).

# Тема 02. Docker — базовые вещи о контейнеризации

## Зачем этот раздел

Минимум, достаточный для локальной разработки: чем образ отличается от
контейнера, из чего состоит `Dockerfile`, как поднять приложение с базой
через `docker-compose`, и какие грабли встречаются чаще всего. После темы
вы сможете сами упаковать сервис в образ и поднять его вместе с базой или
кэшем одной командой — это нужно для
[2_data_and_messaging](../../2_data_and_messaging/) и
[3_web_frameworks](../../3_web_frameworks/).

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — команды docker/compose, инструкции Dockerfile, частые ошибки.

## Что нужно знать заранее

- Терминал и `cd` (урок
  [00_setup](../../1_python/1_python_fundamentals/00_setup/)), базовый Git
  ([01_git_essentials](../01_git_essentials/)).
- Желательно пройти [1_python](../../1_python/): приложения в примерах и
  упражнениях используют классы, `with`, `try`, модули `socket` и
  `http.server`, а также FastAPI/Flask. Разбираться в их коде не нужно —
  его можно считать «чёрным ящиком»: задача темы в том, чтобы упаковать
  и запустить приложение, а не написать его.
- Установленный и запущенный Docker (Docker Desktop или Docker Engine +
  плагин `docker compose`).

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

## Когда двигаться дальше

Когда можете объяснить разницу между образом и контейнером, написать
`Dockerfile` для небольшого приложения и поднять два связанных сервиса
через `docker compose up` (все `check.sh` дают `PASS`) — переходите к
[2_data_and_messaging](../../2_data_and_messaging/).

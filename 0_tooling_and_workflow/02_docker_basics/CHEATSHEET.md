# Docker — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/): образы и контейнеры —
[01_images_and_containers.md](./01_theory/01_images_and_containers.md),
Dockerfile — [02_dockerfile_basics.md](./01_theory/02_dockerfile_basics.md),
compose — [03_compose_and_commands.md](./01_theory/03_compose_and_commands.md).
⚠️ — команда удаляет данные или ведёт себя неочевидно.

## Образы и контейнеры

| Задача | Команда |
| :--- | :--- |
| Собрать образ из `Dockerfile` в текущей папке | `docker build -t myapp .` |
| Список образов | `docker images` |
| Запущенные контейнеры / все, включая остановленные | `docker ps` / `docker ps -a` |
| Создать и запустить **новый** контейнер | `docker run <image>` |
| В фоне, с именем, с пробросом порта `host:container` | `docker run -d --name myapp -p 8000:8000 <image>` |
| Удалить контейнер сразу после остановки | `docker run --rm <image>` |
| Зайти в **уже запущенный** контейнер | `docker exec -it <container> bash` |
| Логи (stdout/stderr процесса PID 1) / следить | `docker logs <container>` / `docker logs -f <container>` |
| Мягко остановить (`SIGTERM`, по таймауту `SIGKILL`) | `docker stop <container>` |
| Запустить существующий / перезапустить | `docker start <container>` / `docker restart <container>` |
| Удалить контейнер ⚠️ (его read-write слой пропадёт) | `docker rm <container>` |
| Удалить образ (если нет контейнеров на его основе) | `docker rmi <image>` |
| Сколько места занято | `docker system df` |
| Убрать неиспользуемые контейнеры/сети/dangling-образы ⚠️ | `docker system prune` |

## Compose

| Задача | Команда |
| :--- | :--- |
| Поднять все сервисы / в фоне | `docker compose up` / `docker compose up -d` |
| Пересобрать образы перед запуском | `docker compose up --build` |
| Остановить и удалить контейнеры и сети (volume'ы живут) | `docker compose down` |
| То же + удалить именованные volume'ы ⚠️ (данные БД пропадут) | `docker compose down -v` |
| Статус сервисов | `docker compose ps` |
| Логи сервиса | `docker compose logs -f app` |
| Зайти в контейнер сервиса | `docker compose exec app bash` |

## Инструкции Dockerfile

| Инструкция | Что делает |
| :--- | :--- |
| `FROM` | Базовый образ; первая инструкция (до неё допустим только `ARG`) |
| `WORKDIR` | Рабочая папка (создаётся сама); вместо `RUN cd ...` |
| `COPY` | Копирует файлы с хоста в образ |
| `ADD` | `COPY` + распаковка архивов + скачивание по URL; без нужды — `COPY` |
| `RUN` | Команда **во время сборки**, результат — новый слой |
| `ENV` | Переменная и при сборке, и в контейнере |
| `ARG` | Переменная **только при сборке** (`--build-arg`) |
| `EXPOSE` | Только документация; порт публикует `-p` / `ports:` |
| `CMD` | Команда по умолчанию; заменяется аргументами `docker run image ARGS` |
| `ENTRYPOINT` | Выполняется всегда; аргументы `docker run` дописываются к ней |
| `USER` | От чьего имени процесс (по умолчанию `root` — плохо для прода) |

## Когда что использовать

| Выбор | Правило |
| :--- | :--- |
| `docker run` vs `docker exec` | `run` — новый контейнер из образа; `exec` — ещё процесс в уже запущенном |
| `CMD` vs `ENTRYPOINT` | `ENTRYPOINT ["python", "manage.py"]` + `CMD ["runserver"]` → `docker run img shell` даст `python manage.py shell` |
| `COPY` vs `ADD` | `COPY` всегда, `ADD` — только если нужна распаковка архива |
| exec form vs shell form | `CMD ["python", "app.py"]` — процесс получает `SIGTERM` как PID 1; `CMD python app.py` — PID 1 у `/bin/sh` |
| Named volume vs bind mount | `pgdata:/var/lib/postgresql/data` — данные сервисов; `./app:/app` — код при разработке |
| Anonymous volume | Избегать — плодит безымянные volume'ы |
| `ports:` у сервиса | Только если к нему нужен доступ с хоста; БД внутри сети — без `ports` |

## Порядок слоёв (кэш)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .                              # меняется редко
RUN pip install --no-cache-dir -r requirements.txt   # кэшируется, пока не изменился requirements.txt
COPY . .                                             # меняется часто — в конце
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Multi-stage: `FROM python:3.12 AS builder` → собрать → `FROM python:3.12-slim`
+ `COPY --from=builder /deps ...` — в финальном образе нет компиляторов.

## Частые ошибки

- ⚠️ Изменилась инструкция N — кэш сброшен для неё **и всех следующих**: `COPY . .` до `pip install` пересобирает зависимости при любой правке кода.
- ⚠️ Данные в read-write слое контейнера пропадают при `docker rm` — БД и загрузки держать в volume.
- ⚠️ Shell form `CMD` → приложение не PID 1, `docker stop` ждёт таймаут и убивает через `SIGKILL`.
- `EXPOSE` не публикует порт — без `-p`/`ports:` с хоста сервис недоступен.
- В compose к другому сервису обращаются по имени сервиса (`db:5432`), не по `localhost`.
- `depends_on` ждёт только **старта** контейнера, не готовности; нужен `healthcheck` + `condition: service_healthy` или retry в клиенте.
- Без `.dockerignore` в контекст сборки (и через `COPY . .` в образ) попадают `.git`, `.venv`, `.env`.
- `docker start` запускает **существующий** контейнер, а не новый из образа.

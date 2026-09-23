# docker-compose, volumes, networks

## Зачем compose

`docker-compose` (сейчас — плагин `docker compose`, без дефиса) описывает
**несколько контейнеров как единую систему** для локальной разработки: само
приложение, база данных, кэш и т.д., одной командой:

```bash
docker compose up            # поднять все сервисы (соберёт образы при необходимости)
docker compose up -d          # в фоне
docker compose up --build      # принудительно пересобрать образы перед запуском
docker compose down            # остановить и удалить контейнеры (и сети, но не volume'ы)
docker compose down -v          # то же самое, но ещё удалить именованные volume'ы

docker compose ps               # статус сервисов
docker compose logs -f app       # логи конкретного сервиса
docker compose exec app bash      # зайти в контейнер сервиса
```

## Минимальный docker-compose.yml

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=appdb
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## Сети: сервисы видят друг друга по имени

⚠️ Ключевая, неочевидная для новичков деталь: compose автоматически создаёт
**общую сеть** для всех сервисов проекта, и внутри неё сервисы обращаются
друг к другу **по имени сервиса как по hostname**, а не по `localhost`.
В примере выше `app` подключается к базе по адресу `db:5432` — `db` тут не
placeholder, а буквально имя сервиса из `docker-compose.yml`, которое
резолвится встроенным DNS Docker'а.

`depends_on` контролирует только **порядок запуска контейнера**, а не
готовность приложения внутри него (Postgres может ещё не принимать
подключения, пока контейнер уже "запущен"). Для настоящего ожидания
готовности используют `healthcheck` + `condition: service_healthy` в
`depends_on`, либо retry-логику на стороне клиента приложения.

## Volumes: именованные vs bind mount

| Тип | Синтаксис | Где хранится | Когда использовать |
| :--- | :--- | :--- | :--- |
| **Named volume** | `pgdata:/var/lib/postgresql/data` | Управляется Docker'ом (обычно `/var/lib/docker/volumes/...`) | Персистентные данные сервисов (БД, кэши) — переживают `docker compose down` (без `-v`) |
| **Bind mount** | `./app:/app` | Обычная папка на хосте, путь вы указываете сами | Локальная разработка — правки кода на хосте сразу видны в контейнере, без пересборки образа |
| **Anonymous volume** | `/var/lib/postgresql/data` (без имени слева) | Управляется Docker'ом, но без явного имени | Обычно избегают — сложно переиспользовать между запусками, легко случайно расплодить "мусорные" volume'ы |

Типичный паттерн для разработки — совместить оба: bind mount кода для
горячей перезагрузки + named volume для данных БД:

```yaml
services:
  app:
    build: .
    volumes:
      - ./app:/app          # bind mount: код меняется на хосте — виден в контейнере
    ports:
      - "8000:8000"
  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data   # named volume: данные переживают down
volumes:
  pgdata:
```

## EXPOSE / ports — ещё раз про публикацию портов

`EXPOSE` в Dockerfile — просто документация. Реальная публикация порта наружу
(на хост) задаётся только в `docker run -p host:container` или в
`ports: ["host:container"]` в compose. Без этого сервис доступен **только**
другим контейнерам той же сети — что часто и является желаемым поведением
для внутренних сервисов вроде базы данных, которую наружу светить не нужно.

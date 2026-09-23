# Примеры: Python + PostgreSQL

Рабочий стенд на Docker Compose и набор самостоятельных Python-скриптов,
каждый из которых иллюстрирует один раздел теории из `../01_theory/README.md`.

## Состав

- `docker-compose.yml` -- один сервис PostgreSQL 16 с именованным томом,
  портом 5432 и healthcheck.
- `requirements.txt` -- psycopg (v3, `psycopg[binary]`), SQLAlchemy 2.x,
  python-dotenv.
- `schema.sql` -- схема и сид-данные: `accounts` (перевод денег),
  `authors`/`books` (ORM, N+1), `customers`/`orders` (~200 000 строк, для
  индексов и EXPLAIN ANALYZE), `products` (блокировки).
- `db_config.py` -- общие настройки подключения (DSN для psycopg и
  SQLAlchemy), читаются из переменных окружения с fallback на значения из
  `docker-compose.yml`.
- Скрипты-примеры (`01_...py` .. `04_...py`), см. ниже.

## Как запустить

1. Поднять базу:

```bash
docker compose up -d
docker compose ps   # дождаться healthy
```

2. Установить зависимости (лучше в виртуальном окружении):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Загрузить схему и сид-данные (~200 000 строк в orders генерируются тут
   же, это может занять несколько секунд):

```bash
docker compose exec -T postgres psql -U kb_user -d kb_shop -v ON_ERROR_STOP=1 < schema.sql
```

Либо через `psql` с хоста, если он установлен локально и порт 5432 свободен:

```bash
PGPASSWORD=kb_password psql -h localhost -U kb_user -d kb_shop -f schema.sql
```

4. Запускать примеры по одному (каждый скрипт самодостаточен и печатает
   пояснения в stdout):

```bash
python 01_transactions_bank_transfer.py
python 02_sqlalchemy_orm_basics.py
python 03_indexes_and_explain.py
python 04_n_plus_one_problem.py
```

## Что показывает каждый скрипт

| Скрипт | Тема | Что демонстрирует |
|--------|------|--------------------|
| `01_transactions_bank_transfer.py` | Транзакции / ACID | Корректный перевод денег в одной транзакции vs антипаттерн с двумя autocommit-запросами; явный rollback при недостатке средств |
| `02_sqlalchemy_orm_basics.py` | SQLAlchemy ORM | Декларативные модели 2.0-стиля, связь один-ко-многим, базовый CRUD через Session |
| `03_indexes_and_explain.py` | Индексы / EXPLAIN ANALYZE | План запроса до и после `CREATE INDEX` на `orders.customer_id`: Seq Scan -> Index/Bitmap Scan |
| `04_n_plus_one_problem.py` | Проблема N+1 | Подсчёт реальных SQL-запросов: антипаттерн (1+N) vs `selectinload` (2 запроса) vs `joinedload` (1 запрос) |

## Переменные окружения (опционально)

По умолчанию скрипты подключаются к `localhost:5432` с учётными данными из
`docker-compose.yml`. Чтобы переопределить (например, для другого порта),
создайте файл `.env` рядом со скриптами:

```
PG_HOST=localhost
PG_PORT=5432
PG_USER=kb_user
PG_PASSWORD=kb_password
PG_DB=kb_shop
```

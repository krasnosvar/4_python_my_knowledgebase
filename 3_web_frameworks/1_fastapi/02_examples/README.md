# Пример: FastAPI + SQLAlchemy 2.0 + Alembic

Небольшое рабочее приложение "items service": пара эндпоинтов, Pydantic v2
модели с валидацией и вложенной схемой, SQLAlchemy 2.0 (`Mapped`/`mapped_column`)
и миграция схемы через Alembic.

Для простоты запуска используется sqlite-файл (`app.db`) вместо PostgreSQL —
не нужно поднимать внешнюю БД. В реальном async-сервисе на месте
`create_engine`/`sessionmaker` (синхронный SQLAlchemy) был бы
`create_async_engine`/`async_sessionmaker` поверх `asyncpg` — см.
`01_theory/01_async_endpoints.md` о том, когда это действительно нужно.

## Структура

```
app/
  main.py          — создание FastAPI(), подключение роутера
  database.py       — engine, SessionLocal, Base
  models.py          — SQLAlchemy-модель Item
  schemas.py          — Pydantic-схемы: ItemCreate (валидация), ItemRead (с вложенной ItemMeta)
  dependencies.py      — get_db(): yield-зависимость для сессии БД
  routers/items.py       — эндпоинты /items
alembic/
  env.py              — настроен на Base.metadata из app.database/app.models
  versions/0001_...     — миграция создания таблицы items
alembic.ini
requirements.txt
```

## Установка и запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# накатить миграции (создаст app.db и таблицу items)
alembic upgrade head

# запустить сервер
uvicorn app.main:app --reload
```

Приложение поднимется на `http://127.0.0.1:8000`, интерактивная документация —
на `http://127.0.0.1:8000/docs`.

## Примеры запросов

Создать item (валидация: `name` непустой, `price > 0`):

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H 'Content-Type: application/json' \
  -d '{"name": "Widget", "price": 9.99, "description": "test item"}'
```

Список items:

```bash
curl http://127.0.0.1:8000/items
```

Получить один item по id:

```bash
curl http://127.0.0.1:8000/items/1
```

`async def`-эндпоинт с имитацией await над внешним сервисом:

```bash
curl http://127.0.0.1:8000/items/1/with-external-check
```

Провалить валидацию (пустое имя, отрицательная цена) — вернётся `422` со
списком ошибок от Pydantic:

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H 'Content-Type: application/json' \
  -d '{"name": "", "price": -1}'
```

## Полезные команды Alembic

```bash
alembic current       # какая миграция применена сейчас
alembic history         # цепочка миграций
alembic downgrade -1    # откатить последнюю миграцию
alembic revision --autogenerate -m "описание изменения"   # сгенерировать новую миграцию по diff с моделями
```

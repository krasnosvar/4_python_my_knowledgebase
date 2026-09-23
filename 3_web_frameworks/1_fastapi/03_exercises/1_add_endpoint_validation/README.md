# Упражнение 1: эндпоинт с валидацией (PATCH /items/{id})

Это копия приложения из `02_examples` с недостающими частями, помеченными
`# TODO:`. Нужно реализовать частичное обновление ресурса `Item`.

## Задание

1. В `app/schemas.py` — доделать `ItemUpdate`:
   - все поля опциональны (`str | None`, `float | None` с дефолтом `None`);
   - если `price` передан — должен быть `> 0`;
   - если `name` передан — не должен быть пустой строкой после `.strip()`
     (валидатор аналогичен тому, что уже есть в `ItemCreate`).

2. В `app/routers/items.py` — доделать тело `update_item`:
   - обновить в БД только те поля объекта `item`, которые реально пришли в
     `payload` (см. подсказку про `model_dump(exclude_unset=True)` в коде);
   - роут уже возвращает 404, если item не найден, и коммитит/возвращает
     результат — это менять не нужно.

## Как проверить

В этом упражнении своей alembic-конфигурации нет (она не нужна для задачи про
эндпоинт) — таблицу проще создать напрямую перед запуском:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python3 -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(engine)"
uvicorn app.main:app --reload
```

Создать item, затем частично обновить только цену:

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H 'Content-Type: application/json' \
  -d '{"name": "Widget", "price": 10.0}'

curl -X PATCH http://127.0.0.1:8000/items/1 \
  -H 'Content-Type: application/json' \
  -d '{"price": 12.5}'
```

Ожидаемое поведение:
- `name` и `description` в ответе не изменились, `price` стал `12.5`;
- `PATCH` с `{"price": -5}` должен вернуть `422` (валидация `gt=0`);
- `PATCH /items/999` (несуществующий id) должен вернуть `404`.

Решение — в `04_exercises_answers/1_add_endpoint_validation/`.

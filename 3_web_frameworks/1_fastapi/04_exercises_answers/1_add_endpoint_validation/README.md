# Решение упражнения 1: эндпоинт с валидацией (PATCH /items/{id})

Готовое решение задачи из `03_exercises/1_add_endpoint_validation/`: `ItemUpdate`
с опциональными полями и валидацией, `PATCH /items/{item_id}`, обновляющий
только реально переданные поля через `model_dump(exclude_unset=True)`.

## Как запустить и проверить

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

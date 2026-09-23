# Решения упражнений: FastAPI

Готовые решения для упражнений из `../03_exercises/`, с той же структурой
директорий — можно сравнить своё решение с эталонным через `diff -r`:

```bash
diff -r ../03_exercises/1_add_endpoint_validation ./1_add_endpoint_validation
diff -r ../03_exercises/2_alembic_migration ./2_alembic_migration
```

1. **[1_add_endpoint_validation](./1_add_endpoint_validation/)** — `PATCH /items/{id}`
   с валидацией через `ItemUpdate`.
2. **[2_alembic_migration](./2_alembic_migration/)** — миграция, добавляющая
   колонку `in_stock` к существующей таблице `items`.

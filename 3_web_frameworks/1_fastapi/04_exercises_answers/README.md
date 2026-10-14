# Решения упражнений: FastAPI

Готовые решения для упражнений из `../03_exercises/`, с той же структурой
директорий — можно сравнить своё решение с эталонным через `diff -r`:

```bash
diff -r ../03_exercises/01_add_endpoint_validation ./01_add_endpoint_validation
diff -r ../03_exercises/02_alembic_migration ./02_alembic_migration
```

1. **[01_add_endpoint_validation](./01_add_endpoint_validation/)** — `PATCH /items/{id}`
   с валидацией через `ItemUpdate`.
2. **[02_alembic_migration](./02_alembic_migration/)** — миграция, добавляющая
   колонку `in_stock` к существующей таблице `items`.

# Упражнения: FastAPI

Обе директории — самостоятельные копии приложения из `02_examples` с
недостающими частями, помеченными `# TODO:`.

1. **[01_add_endpoint_validation](./01_add_endpoint_validation/)** — доделать
   `PATCH /items/{id}` с валидацией через Pydantic-схему `ItemUpdate`.
2. **[02_alembic_migration](./02_alembic_migration/)** — написать Alembic-миграцию,
   добавляющую колонку `in_stock` к уже существующей таблице `items`.

Внутри каждой папки — свой `README.md` с условием задачи и шагами проверки.
Готовые решения — в `../04_exercises_answers/`, с той же структурой директорий,
так что можно сравнить построчно (`diff -r`).

# Тема 1. FastAPI

## Зачем эта тема

До сих пор весь код в репо запускался как скрипт: `python file.py`,
результат — в терминал. Реальный backend работает иначе: программа
постоянно запущена, слушает сеть и отвечает на HTTP-запросы от браузеров,
мобильных приложений и других сервисов. FastAPI — современный
async-first фреймворк для таких сервисов. После темы ты сможешь поднять
HTTP API с валидацией входных данных, подключением к БД и миграциями
схемы, и понимать, где в нём можно незаметно «положить» весь сервис
одним неудачным `async def`.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — роуты и параметры, `async def` vs `def`, Pydantic v2, `Depends`, Alembic.

## Что нужно знать заранее

- `async`/`await` из [1_python/6_concurrency](../../1_python/6_concurrency/).
- Базовый SQL из
  [2_data_and_messaging/1_sql_relational_databases](../../2_data_and_messaging/1_sql_relational_databases/).
- Виртуальное окружение и `pip install -r requirements.txt` —
  [other/01_environments_and_packaging](../../other/01_environments_and_packaging/).

## Структура темы

- **[01_theory/](./01_theory/)** — теория, читать по порядку:
  1. [01_http_and_first_app.md](./01_theory/01_http_and_first_app.md) —
     HTTP с нуля (методы, статус-коды, path/query/тело/заголовки), что
     такое фреймворк и роут, WSGI vs ASGI, минимальное приложение,
     почему аннотации типов в FastAPI — часть логики.
  2. [02_async_endpoints.md](./01_theory/02_async_endpoints.md) —
     `async def` vs `def`: когда асинхронность даёт выгоду, а когда
     блокирует весь сервис.
  3. [03_pydantic.md](./01_theory/03_pydantic.md) — модели данных,
     валидация, вложенные схемы, особенности Pydantic v2.
  4. [04_dependency_injection.md](./01_theory/04_dependency_injection.md)
     — `Depends`: сессия БД, текущий пользователь, подмена в тестах.
  5. [05_alembic.md](./01_theory/05_alembic.md) — миграции схемы БД
     поверх SQLAlchemy.
- **[02_examples/](./02_examples/)** — рабочее CRUD-приложение
  (FastAPI + SQLAlchemy + Alembic), см. его README.
- **[03_exercises/](./03_exercises/)** — доделать эндпоинт с валидацией,
  написать миграцию.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные
  решения той же структуры (`diff -r` для сравнения).

## Как проходить тему

1. Прочитать `01_http_and_first_app.md` и запустить минимальное
   приложение из него — убедиться, что `/docs` открывается.
2. Прочитать остальную теорию по порядку.
3. Поднять пример по инструкции в
   [02_examples/README.md](./02_examples/README.md) и погонять запросы.
4. Выполнить упражнения из `03_exercises/`, сверить с
   `04_exercises_answers/`.

## Когда двигаться дальше

Когда ты можешь добавить в приложение новый эндпоинт с Pydantic-валидацией,
объяснить, почему блокирующий вызов внутри `async def` тормозит весь сервис,
и написать Alembic-миграцию под новое поле — переходи к
[2_django](../2_django/).

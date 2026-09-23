# Упражнение 2: Alembic-миграция под новое поле

В `app/models.py` в модель `Item` уже добавлено поле `in_stock: bool`. Таблица
`items` в БД про него пока не знает — миграция `0001` создавала таблицу без
этой колонки. Нужно написать миграцию `0002`, которая добавит колонку в уже
существующую таблицу.

## Задание

Открой `alembic/versions/0002_add_in_stock_column.py` и допиши:

1. `upgrade()` — добавить колонку `in_stock` (`Boolean`, `NOT NULL`) в таблицу
   `items` через `op.add_column`. Обрати внимание: у строк, уже существующих в
   таблице, нет значения для новой `NOT NULL` колонки — без `server_default`
   в БД такая миграция упадёт на существующих данных. Значение по умолчанию
   должно совпадать с тем, что задано в модели (`server_default="1"`, то есть
   "в наличии").
2. `downgrade()` — обратная операция: удалить колонку `in_stock`
   (`op.drop_column`).

## Как проверить

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# накатить миграцию 0001 (создаёт items без in_stock)
alembic upgrade 0001

# создать строку "до" миграции напрямую через SQL (не через ORM: модель Item
# в app/models.py уже содержит in_stock, поэтому ORM-инсерт потребовал бы
# колонку, которой в БД на этом шаге ещё нет — это и имитирует продовые
# данные, накопленные до миграции)
python3 -c "
import sqlite3
con = sqlite3.connect('app.db')
con.execute(\"INSERT INTO items (name, description, price, created_at) VALUES ('Old item', NULL, 1.0, '2026-01-01 00:00:00')\")
con.commit()
"

# теперь накатить твою миграцию 0002
alembic upgrade head
```

Проверь результат:

```bash
python3 -c "
import sqlite3
con = sqlite3.connect('app.db')
print(con.execute('SELECT id, name, in_stock FROM items').fetchall())
"
```

Ожидается, что у ранее созданной строки `in_stock` окажется `1` (True) — то
есть `server_default` действительно применился к уже существующим данным, а
не только к новым. Проверь также `alembic downgrade -1`, а затем `alembic
upgrade head` ещё раз — обе миграции должны быть обратимы.

Решение — в `04_exercises_answers/2_alembic_migration/`.

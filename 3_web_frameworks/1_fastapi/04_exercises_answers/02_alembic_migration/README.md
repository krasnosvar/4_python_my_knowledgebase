# Решение упражнения 2: Alembic-миграция под новое поле

Готовое решение задачи из `03_exercises/02_alembic_migration/`: миграция
`0002_add_in_stock_column.py` добавляет колонку `in_stock` (`Boolean NOT NULL`)
к уже существующей таблице `items`, используя `server_default="1"`, чтобы не
сломаться на строках, добавленных до миграции.

## Как проверить

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# накатить миграцию 0001 (создаёт items без in_stock)
alembic upgrade 0001

# создать строку "до" миграции напрямую через SQL (модель Item уже содержит
# in_stock, поэтому ORM-инсерт потребовал бы колонку, которой в БД на этом
# шаге ещё нет)
python3 -c "
import sqlite3
con = sqlite3.connect('app.db')
con.execute(\"INSERT INTO items (name, description, price, created_at) VALUES ('Old item', NULL, 1.0, '2026-01-01 00:00:00')\")
con.commit()
"

# теперь накатить миграцию 0002
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

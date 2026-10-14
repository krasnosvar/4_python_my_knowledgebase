# Реляционные БД (PostgreSQL) — шпаргалка

Подробности — в [01_theory/](./01_theory/README.md). Диалект — PostgreSQL;
⚠️ — частая ловушка.

## Базовый SQL

Подробнее: [01_sql_in_5_minutes.md](./01_theory/01_sql_in_5_minutes.md).

| Задача | SQL |
| :--- | :--- |
| Создать таблицу с PK и FK | `CREATE TABLE novels (id INT PRIMARY KEY, writer_id INT REFERENCES writers(id), title TEXT NOT NULL);` |
| Вставить несколько строк | `INSERT INTO t (id, name) VALUES (1, 'a'), (2, 'b');` |
| Фильтр, сортировка, лимит | `SELECT title FROM novels WHERE year < 1850 ORDER BY year DESC LIMIT 2;` |
| Изменить / удалить ⚠️ | `UPDATE t SET x = 1 WHERE id = 2;` / `DELETE FROM t WHERE id = 3;` — без `WHERE` затронет **все** строки |
| Только пары с совпадением | `... FROM writers w JOIN novels n ON n.writer_id = w.id` |
| Все строки левой таблицы (+ `NULL` справа) | `... FROM writers w LEFT JOIN novels n ON n.writer_id = w.id` |
| Посчитать по группам | `SELECT w.name, COUNT(n.id) FROM writers w LEFT JOIN novels n ON ... GROUP BY w.name;` |
| Вставить, если нет (идемпотентно) | `INSERT ... ON CONFLICT (event_id) DO NOTHING;` |

- ⚠️ Без `ORDER BY` порядок строк не гарантирован.
- ⚠️ `COUNT(col)` не считает `NULL`, `COUNT(*)` — считает все строки.
- ⚠️ `JOIN` + `GROUP BY` теряет строки без пары: для «0» нужен `LEFT JOIN`.

## Связи и ключи

Подробнее: [02_relational_model.md](./01_theory/02_relational_model.md).

| Связь | Как выразить |
| :--- | :--- |
| 1:1 | FK в дочерней таблице одновременно `PRIMARY KEY` (или `UNIQUE`) |
| 1:N | FK на стороне «многих»: `books.author_id REFERENCES authors(id)` |
| N:M | Связующая таблица с составным `PRIMARY KEY (book_id, author_id)` |

| `ON DELETE` | Поведение | Когда |
| :--- | :--- | :--- |
| `CASCADE` | Дочерние строки удаляются | Владение: книга без автора бессмысленна |
| `SET NULL` | FK обнуляется | Необязательная связь |
| `RESTRICT` / `NO ACTION` | Удаление родителя запрещено | Нужно явно разобраться с зависимостями |

Нормальные формы: 1NF — атомарные значения; 2NF — нет зависимости от части
составного ключа; 3NF — нет зависимости неключевого от неключевого. OLTP —
до 3NF, аналитика — осознанная денормализация.

## Транзакции и изоляция

Подробнее: [03_transactions_acid.md](./01_theory/03_transactions_acid.md).

```sql
BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE name = 'Alice';
UPDATE accounts SET balance = balance + 200 WHERE name = 'Bob';
COMMIT;   -- или ROLLBACK
```

| Уровень | Dirty read | Non-repeatable | Phantom | В PostgreSQL |
| :--- | :---: | :---: | :---: | :--- |
| Read Uncommitted | возможен | возможен | возможен | = Read Committed, грязного чтения нет |
| Read Committed | нет | возможен | возможен | **по умолчанию** |
| Repeatable Read | нет | нет | нет* | снимок на старте транзакции; возможна ошибка сериализации |
| Serializable | нет | нет | нет | SSI; `could not serialize access` → retry в приложении |

| Задача | Как |
| :--- | :--- |
| Уровень в psycopg 3 | `conn.isolation_level = psycopg.IsolationLevel.SERIALIZABLE` |
| «Прочитать — посчитать — записать» безопасно | `SELECT ... FOR UPDATE` или Repeatable Read/Serializable + retry |

## Индексы

Подробнее: [04_indexes.md](./01_theory/04_indexes.md).

| Задача / условие | Индекс |
| :--- | :--- |
| Универсально: `=`, `>`/`<`/`BETWEEN`, `ORDER BY`, `LIKE 'abc%'` | B-Tree (по умолчанию): `CREATE INDEX ON orders (customer_id);` |
| Только точное `=`, диапазонов никогда не будет | Hash: `CREATE INDEX ON users USING HASH (email);` |
| Фильтр по нескольким столбцам | Составной `(city, status)` — работает для `city` и `city+status`, **не** для одного `status` |
| Запросы всегда с одним и тем же условием | Частичный: `CREATE INDEX ON orders (order_date) WHERE status <> 'cancelled';` |
| Условие по функции от столбца | Функциональный: `CREATE INDEX ON users (lower(email));` |

- ⚠️ Каждый индекс замедляет `INSERT`/`UPDATE`/`DELETE` — индексируйте то, что
  реально в `WHERE`/`JOIN`/`ORDER BY`.

## EXPLAIN ANALYZE и планировщик

Подробнее: [05_explain_analyze.md](./01_theory/05_explain_analyze.md),
[11_query_planner.md](./01_theory/11_query_planner.md).

| Узел плана | Значит |
| :--- | :--- |
| `Seq Scan` | Читает всю таблицу; плохо на большой таблице ради малой выборки |
| `Index Scan` | Индекс → `ctid` → строка из heap; хорош при малом числе совпадений |
| `Index Only Scan` | Все столбцы есть в индексе, heap не читается |
| `Bitmap Index Scan` + `Bitmap Heap Scan` | Много совпадений: карта страниц, затем чтение по порядку |

| Поле | Как читать |
| :--- | :--- |
| `cost=0.29..8.45` | Условные единицы: до первой строки..до всех |
| `rows` в cost vs в actual | Оценка vs факт; большое расхождение → `ANALYZE` |
| `actual time=a..b` | мс до первой / последней строки |
| `loops=N` | Узел выполнялся N раз: время × loops |

| Индекс не используется — почему | Что делать |
| :--- | :--- |
| Несоответствие типов (`= '777'` на `INT`) | Передавать значение нужного типа |
| Функция над столбцом (`lower(email)`) | Функциональный индекс |
| Низкая селективность (полтаблицы) | Это нормально: Seq Scan дешевле |
| Устаревшая статистика после массовой загрузки | `ANALYZE table;`, не отключать autovacuum |

## N+1 в ORM

Подробнее: [06_n_plus_one.md](./01_theory/06_n_plus_one.md).

| Задача | SQLAlchemy 2.0 | Django |
| :--- | :--- | :--- |
| Связь 1:N, «хвост» большой (2 запроса, `IN (...)`) | `select(Author).options(selectinload(Author.books))` | `prefetch_related("books")` |
| FK / 1:1 вперёд (1 запрос, `JOIN`) | `select(Author).options(joinedload(Author.books))` (+ `.unique()` для 1:N) | `select_related("publisher")` |
| Найти N+1 | `create_engine(..., echo=True)`, событие `before_cursor_execute` | `django-debug-toolbar` |

- ⚠️ Обращение к ленивой связи (`author.books`) в цикле = запрос на каждую итерацию.

## Блокировки

Подробнее: [07_locking.md](./01_theory/07_locking.md).

| Подход | Как | Когда |
| :--- | :--- | :--- |
| Пессимистичный | `SELECT ... FOR UPDATE` внутри транзакции | Конфликты частые, транзакции короткие (склад, счёт) |
| Оптимистичный | `UPDATE ... SET version = version + 1 WHERE id = 42 AND version = 5`, проверить `rowcount == 0` → retry | Конфликты редкие, данные долго «на руках» (формы) |
| Избежать deadlock | Брать блокировки в едином порядке: `lo, hi = sorted([from_id, to_id])` | Всегда, когда трогаете несколько строк |

- ⚠️ Долгий внешний вызов внутри `FOR UPDATE` держит всех конкурентов.
- ⚠️ `deadlock detected` — транзакцию прервали, её нужно повторить.

## Репликация, CAP, WAL

Подробнее: [08_replication.md](./01_theory/08_replication.md),
[09_cap_and_eventual_consistency.md](./01_theory/09_cap_and_eventual_consistency.md),
[10_wal.md](./01_theory/10_wal.md).

| Режим | Плюс | Минус |
| :--- | :--- | :--- |
| Асинхронная реплика | Быстрый `COMMIT` | Replication lag, stale reads, потеря хвоста при failover |
| Синхронная реплика | Нет потери подтверждённого `COMMIT` | Задержка записи; реплика недоступна → запись встаёт |
| Гибрид | `synchronous_commit`, `synchronous_standby_names` | Настраивать под нагрузку |

| Ситуация | Решение |
| :--- | :--- |
| Пользователь не видит только что сохранённое | Read your own writes: читать с primary сразу после записи |
| Масштабировать чтение | Read replicas для данных, терпимых к несвежести |
| Разрыв сети (CAP) | CP — отказать/ждать (sync-репликация, etcd); AP — ответить старым (async-реплика, Cassandra) |
| Без разрыва (PACELC) | Выбор между задержкой и согласованностью |

- WAL: запись в лог + `fsync` до подтверждения `COMMIT`; страницы данных — позже,
  на checkpoint; streaming replication = трансляция WAL на реплику.
- ⚠️ «C» в CAP ≠ «C» в ACID.

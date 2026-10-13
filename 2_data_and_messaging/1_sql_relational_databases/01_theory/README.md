# Реляционные базы данных: теория (PostgreSQL + Python)

Этот конспект объясняет не только "что это", но и "почему так, а не иначе" —
какие проблемы решает каждая концепция и какую цену приходится платить за
решение. Примеры даны на SQL (диалект PostgreSQL); там, где это важно для
Python-разработчика, добавлены пометки про psycopg / SQLAlchemy / Django ORM.

Уроки читаются по порядку, каждый следующий опирается на предыдущие:

1. [01_sql_in_5_minutes.md](./01_sql_in_5_minutes.md) — SQL с нуля: таблица,
   строка, столбец, `PRIMARY KEY`, `SELECT`/`WHERE`/`ORDER BY`/`LIMIT`,
   `INSERT`/`UPDATE`/`DELETE`, `JOIN`, `GROUP BY` + `COUNT`.
2. [02_relational_model.md](./02_relational_model.md) — связи 1:1, 1:N, N:M,
   первичные и внешние ключи, нормализация.
3. [03_transactions_acid.md](./03_transactions_acid.md) — транзакции, ACID,
   MVCC, уровни изоляции и аномалии.
4. [04_indexes.md](./04_indexes.md) — B-Tree и Hash, составные и частичные
   индексы.
5. [05_explain_analyze.md](./05_explain_analyze.md) — как читать план
   запроса и почему индекс может не использоваться.
6. [06_n_plus_one.md](./06_n_plus_one.md) — что такое ORM, проблема N+1 и
   eager loading.
7. [07_locking.md](./07_locking.md) — пессимистичные и оптимистичные
   блокировки, deadlock.
8. [08_replication.md](./08_replication.md) — primary/replica, replication
   lag, синхронная и асинхронная репликация.
9. [09_cap_and_eventual_consistency.md](./09_cap_and_eventual_consistency.md)
   — CAP-теорема и eventual consistency на примере репликации.
10. [10_wal.md](./10_wal.md) — Write-Ahead Log, восстановление после сбоя,
    checkpoint, связь с репликацией.
11. [11_query_planner.md](./11_query_planner.md) — cost-based optimizer,
    статистика, `ANALYZE` и автовакуум.

Как проходить всю тему (стенд, примеры, упражнения) — в
[README темы](../README.md).

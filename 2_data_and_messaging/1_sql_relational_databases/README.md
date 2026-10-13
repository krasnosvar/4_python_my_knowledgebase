# Реляционные базы данных (PostgreSQL + Python)

## Зачем эта тема

Почти любой backend-сервис хранит данные в реляционной базе. Пока данных
мало и пользователь один, работает что угодно. Проблемы начинаются в проде:

- перевод денег наполовину выполнился, потому что процесс упал между двумя
  запросами;
- запрос, который локально отвечал мгновенно, на миллионе строк идёт
  секунды;
- страница делает сотни запросов к базе вместо двух (проблема N+1);
- два запроса одновременно меняют одну строку и затирают правки друг друга;
- пользователь сохранил данные и тут же видит старую версию с реплики.

После темы ты сможешь писать базовый SQL, оборачивать операции в
транзакции, понимать, когда нужен индекс, читать `EXPLAIN ANALYZE`, находить
N+1 в коде на ORM и выбирать между пессимистичной и оптимистичной
блокировкой.

Нужно заранее: раздел [1_python](../../1_python/), Docker на уровне
[0_tooling_and_workflow](../../0_tooling_and_workflow/) и виртуальное
окружение из
[other/01_environments_and_packaging](../../other/01_environments_and_packaging/).
SQL с нуля разбирается в первом уроке.

## Структура темы

- **[01_theory/](./01_theory/README.md)** — 11 уроков по порядку:
  1. [SQL за 5 минут](./01_theory/01_sql_in_5_minutes.md)
  2. [Реляционная модель](./01_theory/02_relational_model.md)
  3. [Транзакции и ACID](./01_theory/03_transactions_acid.md)
  4. [Индексы](./01_theory/04_indexes.md)
  5. [EXPLAIN ANALYZE](./01_theory/05_explain_analyze.md)
  6. [ORM и проблема N+1](./01_theory/06_n_plus_one.md)
  7. [Блокировки](./01_theory/07_locking.md)
  8. [Репликация](./01_theory/08_replication.md)
  9. [CAP-теорема и eventual consistency](./01_theory/09_cap_and_eventual_consistency.md)
  10. [WAL (Write-Ahead Log)](./01_theory/10_wal.md)
  11. [Планировщик запросов](./01_theory/11_query_planner.md)
- **[02_examples/](./02_examples/README.md)** — стенд PostgreSQL на Docker
  Compose, `schema.sql` с сид-данными и 4 скрипта: транзакция перевода денег,
  основы SQLAlchemy ORM, индексы и `EXPLAIN`, демонстрация N+1.
- **[03_exercises/](./03_exercises/README.md)** — задания с `TODO`: индексы
  и `EXPLAIN ANALYZE`, перевод денег в транзакции, исправление N+1,
  (опционально) pessimistic vs optimistic locking.
- **[04_exercises_answers/](./04_exercises_answers/README.md)** — готовые
  решения под теми же именами файлов.

## Как проходить тему

1. Прочитайте уроки `01_theory/` по порядку от `01` до `11`.
2. Поднимите стенд и загрузите схему (подробно — в
   [02_examples/README.md](./02_examples/README.md)):

   ```bash
   cd 02_examples
   docker compose up -d
   docker compose ps   # дождаться healthy
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   docker compose exec -T postgres psql -U kb_user -d kb_shop -v ON_ERROR_STOP=1 < schema.sql
   ```

3. Запустите примеры по одному, например:

   ```bash
   python 01_transactions_bank_transfer.py
   ```

4. Выполните задания из `03_exercises/` и только потом сверьтесь с
   `04_exercises_answers/`.
5. Остановить стенд: `docker compose down` (данные сохранятся в томе),
   `docker compose down -v` — остановить и удалить данные.

[К оглавлению раздела](../README.md).

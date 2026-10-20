# Тема 2. Django

## Зачем эта тема

Django — «batteries-included» фреймворк: ORM, миграции, админка,
авторизация и формы идут в комплекте. На нём написано огромное количество
production-проектов, и почти в каждом рано или поздно всплывает одна и
та же проблема производительности — N+1 запросов к базе. После темы ты
будешь понимать, как устроен Django-проект, как ORM превращает Python-код
в SQL, почему безобидный цикл может отправить в базу сотни запросов и
как это исправить.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — `manage.py`, когда QuerySet идёт в БД, `select_related` vs `prefetch_related`, сигналы.

## Что нужно знать заранее

- Классы и объекты из [1_python/3_oop](../../1_python/3_oop/) — модели
  Django описываются классами.
- Базовый SQL (`SELECT`, `JOIN`, внешние ключи) и проблема N+1 из
  [2_data_and_messaging/1_sql_relational_databases](../../2_data_and_messaging/1_sql_relational_databases/).
- Виртуальное окружение и `pip install -r requirements.txt` —
  [other/01_environments_and_packaging](../../other/01_environments_and_packaging/).

## Структура темы

- **[01_theory/](./01_theory/)** — теория, читать по порядку (оглавление —
  в [01_theory/README.md](./01_theory/README.md)):
  1. [01_project_structure.md](./01_theory/01_project_structure.md) —
     project vs apps, `manage.py`, модель и первый запрос через ORM.
  2. [02_lazy_querysets.md](./01_theory/02_lazy_querysets.md) — ленивые
     QuerySet'ы и откуда берётся N+1.
  3. [03_select_related_prefetch_related.md](./01_theory/03_select_related_prefetch_related.md)
     — два способа избавиться от N+1 и когда какой выбирать.
  4. [04_signals.md](./01_theory/04_signals.md) — сигналы и их подвохи.
- **[02_examples/](./02_examples/)** — приложение `library`, которое
  считает SQL-запросы до и после оптимизации.
- **[03_exercises/](./03_exercises/)** — найти и исправить N+1.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные
  решения.

## Как проходить тему

1. Прочитать теорию по порядку.
2. Запустить пример по [02_examples/README.md](./02_examples/README.md)
   и сравнить число запросов naive vs optimized.
3. Выполнить упражнения из `03_exercises/`, сверить с
   `04_exercises_answers/`.

## Когда двигаться дальше

Когда ты можешь по коду цикла над QuerySet предсказать, сколько SQL-запросов
он сделает, и выбрать между `select_related` и `prefetch_related` —
переходи к [3_celery](../3_celery/).

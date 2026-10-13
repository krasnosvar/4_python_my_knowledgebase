# Тема 7. Стандартная библиотека (Standard Library)

Обзорный проход по важной части стандартной библиотеки Python:
`collections`, `functools`/`itertools` (сверх базового), `datetime`/`zoneinfo`,
`re`, `json`/`csv`, `pathlib`/`os`, `logging`.

## Зачем этот раздел

Стандартная библиотека устанавливается вместе с Python и решает множество
повседневных задач без сторонних пакетов: посчитать частоты слов, работать
с датами и часовыми поясами, разобрать лог регулярным выражением, прочитать
JSON/CSV, пройтись по файлам в папке, писать логи вместо `print`. Тот, кто
не знает стандартную библиотеку, пишет руками то, что уже есть (и обычно
с ошибками — особенно с датами и часовыми поясами). После раздела вы
будете знать, какой готовый инструмент взять для типовой задачи, и
избегать его классических ловушек.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_collections_module.md](./01_theory/01_collections_module.md) —
    специализированные контейнеры (`Counter`, `defaultdict`, `deque`,
    `namedtuple`).
  - [02_functools_itertools_extra.md](./01_theory/02_functools_itertools_extra.md)
    — кэширование, `partial`, комбинаторные рецепты `itertools`.
  - [03_datetime_time_timezones.md](./01_theory/03_datetime_time_timezones.md)
    — даты, время и часовые пояса без типичных ошибок.
  - [04_re_regular_expressions.md](./01_theory/04_re_regular_expressions.md)
    — регулярные выражения: шпаргалка по синтаксису и функции `re`.
  - [05_json_csv_serialization.md](./01_theory/05_json_csv_serialization.md)
    — сериализация в JSON и CSV.
  - [06_pathlib_os_filesystem.md](./01_theory/06_pathlib_os_filesystem.md)
    — пути, файлы и папки через `pathlib`/`os`.
  - [07_logging_basics.md](./01_theory/07_logging_basics.md) — логирование
    вместо `print`.
- **[02_examples/](./02_examples/)** — runnable-примеры на каждую тему.
- **[03_exercises/](./03_exercises/)** — 7 упражнений с `TODO`.
- **[04_exercises_answers/](./04_exercises_answers/)** — готовые решения.

## Как проходить

Темы независимы друг от друга — можно проходить в любом порядке, но
логичнее по номерам: от контейнеров и функциональных инструментов
(используются почти в любом коде) к более прикладным темам (даты,
regex, сериализация, файлы, логирование).

## Запуск примеров и упражнений

```bash
python 02_examples/01_collections_toolkit/main.py
python 03_exercises/01_word_frequency_counter/main.py
```

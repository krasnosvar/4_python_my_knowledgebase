# Тема 1. Основы Python (Basics)

Этот раздел посвящён базовым типам данных и структурам Python: изменяемости (mutable/immutable), хеш-свойствам и их влиянию на выбор структуры данных и производительность, базовым встроенным типам, коллекциям, comprehensions и управляющим конструкциям.

## Структура раздела

* **[01_theory/](./01_theory/)** — теория (разбита по подтемам):
  * [01_mutability_and_identity.md](./01_theory/01_mutability_and_identity.md) — изменяемость и неизменяемость, `is` против `==`, кэширование мелких int/строк в CPython, алиасинг и классическая ловушка с изменяемым значением по умолчанию.
  * [02_hashability_and_performance.md](./01_theory/02_hashability_and_performance.md) — **протокол `hash()`, контракт `__hash__`/`__eq__`, почему списки нехешируемы, а кортежи хешируемы, и почему `dict`/`set` работают за O(1), а `list` — за O(n)**.
  * [03_builtin_types.md](./01_theory/03_builtin_types.md) — `int` произвольной точности, подводные камни `float` (IEEE 754), `bool` как подкласс `int`, синглтон `None`.
  * [04_collections_lists_tuples_sets_dicts.md](./01_theory/04_collections_lists_tuples_sets_dicts.md) — устройство и особенности `list`/`tuple`/`set`/`dict`, гарантия порядка вставки в dict с 3.7, типичные ловушки.
  * [05_comprehensions.md](./01_theory/05_comprehensions.md) — list/dict/set comprehensions, почему они быстрее и читаемее ручных циклов, вложенные comprehensions, walrus-оператор.
  * [06_control_flow.md](./01_theory/06_control_flow.md) — `if`/`for`/`while`, редкая конструкция `for...else`, структурное сопоставление с образцом `match`/`case` (с 3.10).
* **[02_examples/](./02_examples/)** — практические примеры:
  * [01_cli_utilities.py](./02_examples/01_cli_utilities.py) — разбор CLI-конфигурации с приведением типов и валидацией флагов через set.
  * [02_system_infrastructure.py](./02_examples/02_system_infrastructure.py) — дедупликация событий, **замер производительности list vs set при проверке принадлежности**, dict-счётчики.
  * [03_product_backend.py](./02_examples/03_product_backend.py) — трансформация данных заказов через comprehensions и ветвление через `match`/`case`.
* **[03_exercises/](./03_exercises/)** — практические задачи с самопроверкой `PASS`/`FAIL`:
  * `01_mutable_default_arg` — исправление классической ошибки с изменяемым значением по умолчанию.
  * `02_hashable_key` — реализация хешируемого класса-значения `Point` (`__eq__`/`__hash__`).
  * `03_set_dedup` — дедупликация с сохранением порядка через set (без деградации до O(n²)).
  * `04_comprehension_transform` — построение lookup-словаря через dict comprehension.
  * `05_tuple_vs_list_identity` — **демонстрация неизменяемости кортежа и разницы `is`/`==`**.
  * `06_frequency_counter` — счётчик частоты слов на чистом dict (паттерн get-or-default).
  * `07_match_statement` — диспетчеризация команд через `match`/`case`.
  * `08_membership_performance` — **замер и доказательство преимущества set над list при проверке принадлежности**.
* **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию по порядку, начиная с [01_mutability_and_identity.md](./01_theory/01_mutability_and_identity.md), уделив особое внимание [02_hashability_and_performance.md](./01_theory/02_hashability_and_performance.md).
2. Запустите и изучите примеры из папки `02_examples/`:
   ```bash
   python 02_examples/02_system_infrastructure.py
   ```
3. Выполните задачи в `03_exercises/`. Запустите файл для самопроверки:
   ```bash
   python 03_exercises/08_membership_performance.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.

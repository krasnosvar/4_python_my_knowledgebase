# Тема 2. Типы и коллекции изнутри

## Зачем этот раздел

В [1_python_fundamentals](../1_python_fundamentals/README.md) ты научился
*писать* код: переменные, условия, циклы, функции. Здесь — почему этот код
иногда ведёт себя неожиданно, и как этого избежать:

- функция со списком по умолчанию «помнит» данные с прошлого вызова;
- изменил один список — внезапно изменился «другой»;
- `0.1 + 0.2 == 0.3` даёт `False`;
- список нельзя сделать ключом словаря, а кортеж — можно;
- проверка `x in items` на списке из миллиона элементов тормозит, а на
  множестве — мгновенна.

Плюс здесь впервые формально разбираются коллекции (`list`, `tuple`, `set`,
`dict`) — в fundamentals их не было.

## Что нужно знать заранее

Весь [1_python_fundamentals](../1_python_fundamentals/README.md), включая
[06_exceptions](../1_python_fundamentals/06_exceptions/) (`try`/`except`)
и [07_modules_and_imports](../1_python_fundamentals/07_modules_and_imports/)
(`import`). В примерах и упражнениях у функций стоят **аннотации типов**
(`def f(x: int) -> str`) — это необязательные подсказки, Python их не
проверяет; подробно — в разделе «Аннотации типов» файла
[01_functions_basics.md](../1_python_fundamentals/05_functions_basics/01_theory/01_functions_basics.md).

## Структура раздела

- **[01_theory/](./01_theory/)** — теория, порядок важен: каждый следующий
  файл опирается на предыдущие.
  - [01_builtin_types.md](./01_theory/01_builtin_types.md) — `int` без
    переполнения, почему `float` неточен, `bool` как число, `None`.
  - [02_collections_lists_tuples_sets_dicts.md](./01_theory/02_collections_lists_tuples_sets_dicts.md)
    — синтаксис коллекций с нуля, затем чем `list`/`tuple`/`set`/`dict`
    отличаются по устройству и скорости.
  - [03_mutability_and_identity.md](./01_theory/03_mutability_and_identity.md)
    — изменяемые и неизменяемые объекты, `is` против `==`, общие ссылки,
    ловушка с изменяемым значением по умолчанию.
  - [04_hashability_and_performance.md](./01_theory/04_hashability_and_performance.md)
    — почему список нельзя положить в `set`, и почему `set`/`dict` ищут
    быстро, а `list` — медленно.
  - [05_comprehensions.md](./01_theory/05_comprehensions.md) — короткий
    синтаксис для построения списков/словарей/множеств из других коллекций.
  - [06_control_flow.md](./01_theory/06_control_flow.md) — **только новое**
    поверх уже известных `if`/`for`/`while`: `for...else`/`while...else` и
    `match`/`case`.
- **[02_examples/](./02_examples/)** — практические примеры:
  - [01_cli_utilities.py](./02_examples/01_cli_utilities.py) — разбор
    параметров командной строки: приведение типов, проверка флагов через
    `set`.
  - [02_system_infrastructure.py](./02_examples/02_system_infrastructure.py)
    — дедупликация событий, **замер скорости `list` против `set`**,
    словарь-счётчик.
  - [03_product_backend.py](./02_examples/03_product_backend.py) —
    обработка заказов через comprehensions и `match`/`case`.
- **[03_exercises/](./03_exercises/)** — задачи с самопроверкой
  `PASS`/`FAIL`:
  - `01_mutable_default_arg` — исправить ловушку с изменяемым значением по
    умолчанию.
  - `02_hashable_key` — дописать два метода готового класса `Point`, чтобы
    его можно было класть в `set`/`dict`.
  - `03_set_dedup` — убрать дубли, сохранив порядок.
  - `04_comprehension_transform` — построить словарь через comprehension.
  - `05_tuple_vs_list_identity` — **показать неизменяемость кортежа и
    разницу `is`/`==`**.
  - `06_frequency_counter` — посчитать частоту слов через `dict`.
  - `07_match_statement` — разобрать команды через `match`/`case`.
  - `08_membership_performance` — **замерить и доказать, что `set`
    быстрее `list` при проверке `in`**.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные
  решения.

## Как проходить тему

1. Прочитайте теорию по порядку от `01` до `06`. Коллекции (`02`) идут
   раньше изменяемости и хешируемости (`03`-`04`), потому что те опираются
   на синтаксис `list`/`tuple`/`set`/`dict`. Главный файл раздела —
   [04_hashability_and_performance.md](./01_theory/04_hashability_and_performance.md).
2. Запустите примеры из `02_examples/`:
   ```bash
   python 02_examples/02_system_infrastructure.py
   ```
3. Выполните задачи в `03_exercises/`, запуская файл для самопроверки:
   ```bash
   python 03_exercises/08_membership_performance.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.

## Когда двигаться дальше

Когда можешь объяснить, почему `def f(items=[])` — ошибка, и почему для
проверки «видели ли мы этот id» нужен `set`, а не `list` — переходи к
[3_functions_and_decorators](../3_functions_and_decorators/README.md).

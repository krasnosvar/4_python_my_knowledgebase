# Основы Python — шпаргалка

Подробности — в `01_theory/` каждой подтемы (ссылки в заголовках ниже).
⚠️ — частая ошибка.

## 1.0 Установка и запуск

Теория: [01_install_and_run.md](./00_setup/01_theory/01_install_and_run.md)

| Задача | Команда |
| :--- | :--- |
| Версия Python (нужна 3.12+) | `python3 --version` (Windows: `py --version`) |
| Запустить скрипт | `python3 путь/к/файлу.py` |
| Открыть REPL / выйти | `python3` / `exit()`, `Ctrl+D` (Windows: `Ctrl+Z`, Enter) |
| Где я / что тут лежит | `pwd` / `ls` |
| Перейти в папку / на уровень выше | `cd <папка>` / `cd ..` |

- ⚠️ `can't open file` / `No such file or directory` — вы не в той папке:
  проверьте `pwd`, `ls`.
- ⚠️ На Linux/macOS `python` может отсутствовать — пишите `python3` (внутри
  venv подходит и `python`).
- Отступы — 4 пробела; `pip install` — только внутри venv
  ([other/01_environments_and_packaging](../../other/01_environments_and_packaging/)).

## 1.1 Переменные и типы

Теория:
[01_variables_and_types.md](./01_variables_and_types/01_theory/01_variables_and_types.md)

| Тип | Литерал | Преобразование |
| :--- | :--- | :--- |
| `int` | `42`, `-7`, `2 ** 1000` (без переполнения) | `int("42")` → `42` |
| `float` | `3.14` (двоичная дробь IEEE 754) | `float("3.5")` → `3.5` |
| `str` | `"hello"` | `str(42)` → `"42"` |
| `bool` | `True`, `False` (подвид `int`: `True + True == 2`) | `bool(0)` → `False` |
| `NoneType` | `None` — «значения нет» | — |

| Задача | Синтаксис |
| :--- | :--- |
| Присвоить несколько сразу | `x, y = 1, 2` |
| Обменять значения | `x, y = y, x` |
| Одно значение двум именам | `a = b = 0` |
| Тип значения / имя типа строкой | `type(42)` / `type(42).__name__` → `'int'` |
| Проверить принадлежность к типу | `isinstance(True, int)` → `True` |

- Динамическая типизация: тип у значения, а не у имени переменной.
- Имена — `snake_case`; `CamelCase` — для классов.
- ⚠️ `int("abc")` → `ValueError`, а не «пустое» значение.
- ⚠️ `"10" + "10"` → `"1010"` (склейка строк, а не сложение).

## 1.2 Операторы и выражения

Теория:
[01_operators_and_expressions.md](./02_operators_and_expressions/01_theory/01_operators_and_expressions.md)

| Оператор | Пример | Результат |
| :--- | :--- | :--- |
| `/` деление (всегда `float`) | `10 / 2` | `5.0` |
| `//` целочисленное деление | `7 // 3` | `2` |
| `%` остаток | `7 % 3` | `1` |
| `**` степень | `7 ** 3` | `343` |
| `== != > < >= <=` | `5 >= 5` | `True` |
| `and` / `or` / `not` | `age >= 18 and age < 65` | `bool` |
| `+=`, `-=`, `*=` | `x += 1` | `x = x + 1` |
| f-строка | `f"{name}, тебе {age + 1}"` | выражения внутри `{}` |

- Приоритет: `**` → `* / // %` → `+ -` → сравнения → `not` → `and` → `or`.
- Инвариант: `(a // b) * b + a % b == a`.
- ⚠️ `0.1 + 0.2 == 0.3` → `False` (`0.30000000000000004`); сравнивайте
  через `math.isclose(0.1 + 0.2, 0.3)` (см. 1.8).
- ⚠️ Проверку на `None` пишите через `x is None` / `x is not None`.

## 1.3 Ввод и вывод

Теория:
[01_input_output.md](./03_input_output/01_theory/01_input_output.md)

| Задача | Синтаксис |
| :--- | :--- |
| Напечатать несколько значений через пробел | `print("Имя:", name)` |
| Свой разделитель | `print("a", "b", "c", sep="-")` → `a-b-c` |
| Без перевода строки | `print("Загрузка", end="...")` |
| Прочитать строку с подсказкой | `name = input("Как тебя зовут? ")` |
| Прочитать число | `age = int(input("Возраст: "))` |
| 2 знака после запятой | `f"{19.999:.2f}"` → `'20.00'` |

- ⚠️ `input()` всегда возвращает `str`: `input() * 2` для ввода `5` даст
  `"55"`.

## 1.4 Ветвления и циклы

Теория:
[01_control_flow.md](./04_control_flow/01_theory/01_control_flow.md)

```python
if age < 18:
    ...
elif age < 65:          # выполняется только первая подходящая ветка
    ...
else:
    ...

for n in numbers:
    if n < 0:
        break
else:                   # выполнится, только если цикл прошёл без break
    print("Отрицательных нет")

match command:          # структурное сопоставление (Python 3.10+)
    case ("move", x, y):
        ...
    case {"action": "quit"}:
        ...
    case [first, *rest] if len(rest) > 0:
        ...
    case _:
        ...
```

| Задача | Синтаксис |
| :--- | :--- |
| Числа `0..n-1` / `a..b-1` | `range(n)` / `range(a, b)` |
| Прервать цикл / пропустить итерацию | `break` / `continue` |
| Проверить «не пусто ли» | `if items:` / `if not items:` |

- Falsy: `0`, `0.0`, `""`, `None`, `[]`, `()`, `{}`, `set()`. Остальное —
  truthy.
- ⚠️ `else` у цикла срабатывает, когда **не было `break`**.
- ⚠️ Смесь табов и пробелов → `IndentationError`.

## 1.5 Составные типы данных

Теория:
[01_lists_tuples_sets_dicts.md](./05_collections/01_theory/01_lists_tuples_sets_dicts.md),
[02_mutability_and_references.md](./05_collections/01_theory/02_mutability_and_references.md),
[03_comprehensions.md](./05_collections/01_theory/03_comprehensions.md)

| Задача | `list` | `tuple` | `set` | `dict` |
| :--- | :--- | :--- | :--- | :--- |
| Литерал | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{"a": 1}` |
| Пустой | `[]` | `()` | `set()` ⚠️ не `{}` | `{}` |
| Доступ | `lst[0]`, `lst[-1]` | `t[0]` | — | `d["a"]`, `d.get("a", 0)` |
| Добавить | `lst.append(x)` | нельзя | `s.add(x)` | `d["k"] = v` |
| Поиск `in` | `x in lst` (O(n)) | `x in t` (O(n)) | `x in s` (O(1)) | `k in d` (O(1), по ключам) |
| Изменяемый | да | нет | да | да |
| Годится в ключ `dict` / `set` | нет | да (если элементы неизменяемы) | нет | нет |

| Задача | Синтаксис |
| :--- | :--- |
| Срез / копия / разворот | `lst[0:2]` / `lst[:]` / `lst[::-1]` |
| Распаковка | `x, y = point` |
| Перебор пар словаря | `for k, v in d.items():` |
| List comprehension | `[x * 2 for x in data if x % 2 == 0]` |
| Dict / Set comprehension | `{k: len(k) for k in words}` / `{len(w) for w in words}` |
| Вычислить один раз (walrus `:=`) | `[y for s in raw if (y := s.strip()) != ""]` |

- `a == b` сравнивает значения, `a is b` — один ли это объект в памяти
  (`id(a) == id(b)`).
- ⚠️ `alias = original` не копирует список — оба имени ведут к одному
  объекту.
- ⚠️ `[[0] * 3] * 3` создаёт три ссылки на одну и ту же строку; правильно
  `[[0] * 3 for _ in range(3)]`.
- ⚠️ `{"a": 1, "a": 2}` → `{'a': 2}`: дубль ключа молча перезаписывается.

## 1.6 Функции

Теория:
[01_functions_basics.md](./06_functions_basics/01_theory/01_functions_basics.md)

```python
def apply_discount(price: float, discount_percent: float = 10) -> float:
    """Возвращает цену со скидкой."""
    return price - price * discount_percent / 100

def add_item(item, bucket=None):   # правильно: None вместо bucket=[]
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

| Задача | Синтаксис |
| :--- | :--- |
| Вернуть значение | `return x` (функция сразу завершается) |
| Нет `return` | функция возвращает `None` |
| Параметр по умолчанию | `def greet(name, greeting="Привет")` |
| Docstring | строка `"""..."""` первой строкой тела; видна в `help(f)` |
| Аннотации типов | `x: int`, `-> str` — Python их **не проверяет** при запуске |

- ⚠️ Изменяемое значение по умолчанию (`def f(x=[])`) создаётся **один раз**
  при объявлении `def` и делится между всеми вызовами — используйте `None`.

## 1.7 Исключения

Теория: [01_exceptions.md](./07_exceptions/01_theory/01_exceptions.md)

```python
try:
    number = int(text)
except ValueError as e:        # конкретный тип, а не голый except
    print(f"Ошибка: {e}")
else:
    print(number)              # только если ошибки не было
finally:
    print("готово")            # всегда
```

| Исключение | Когда | Пример |
| :--- | :--- | :--- |
| `ValueError` | тип верный, значение нет | `int("abc")` |
| `TypeError` | операция не для этого типа | `"5" + 5`, `hash([1, 2])` |
| `ZeroDivisionError` | деление на ноль | `10 / 0` |
| `NameError` | имя не объявлено | `print(user_nmae)` |
| `KeyError` / `IndexError` | нет ключа / индекса | `d["x"]` / `lst[10]` |

- Traceback читается **снизу вверх**: последняя строка — тип и сообщение.
- Выбросить своё исключение: `raise ValueError("...")`; пробросить текущее
  дальше внутри `except`: `raise`.
- ⚠️ Голый `except:` прячет баги в коде (`NameError`, `TypeError`).

## 1.8 Модули и import

Теория:
[01_modules_and_imports.md](./08_modules_and_imports/01_theory/01_modules_and_imports.md)

| Задача | Синтаксис |
| :--- | :--- |
| Подключить модуль целиком | `import math` → `math.sqrt(16)` |
| Взять отдельные имена | `from math import sqrt, pi` |
| Псевдоним | `import random as rnd` |
| Сравнить `float` с допуском | `math.isclose(0.1 + 0.2, 0.3)` → `True` |
| Точная десятичная дробь (деньги) | `from decimal import Decimal`; `Decimal("0.1")` |
| Глубокая копия вложенных коллекций | `import copy`; `copy.deepcopy(nested)` |
| Случайное целое `a..b` / `[0.0, 1.0)` | `random.randint(1, 6)` / `random.random()` |
| Округлить до n знаков (без import) | `round(3.14159, 2)` → `3.14` |
| Код только при прямом запуске | `if __name__ == "__main__":` |

- При `import` файл выполняется сверху вниз; `__name__` равно имени модуля,
  а при прямом запуске — `"__main__"`.
- ⚠️ `Decimal(0.1)` из `float` уже неточен — передавайте строку
  `Decimal("0.1")`.

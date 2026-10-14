# Типы и коллекции изнутри — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.

## Числа, bool, None

Теория: [01_builtin_types.md](./01_theory/01_builtin_types.md)

| Задача | Синтаксис |
| :--- | :--- |
| Большие целые (переполнения нет) | `2 ** 1000` — обычный `int` |
| Сравнить `float` | `math.isclose(0.1 + 0.2, 0.3)` → `True` |
| Точная десятичная арифметика (деньги) | `Decimal("0.1") + Decimal("0.2")` (или храните копейки в `int`) |
| Посчитать, сколько подходит под условие | `passed += score >= 60` (`True` = 1) |
| Проверка на «нет значения» | `if x is None:` |
| Аннотация «значение или None» | `def f() -> str \| None:` |

- ⚠️ `0.1 + 0.2 == 0.3` → `False` (`0.30000000000000004`).
- ⚠️ `Decimal(0.1)` из `float` уже неточен — передавайте строку `Decimal("0.1")`.
- `isinstance(True, int)` → `True`: `bool` — подвид `int`.

## Коллекции: синтаксис

Теория: [02_collections_lists_tuples_sets_dicts.md](./01_theory/02_collections_lists_tuples_sets_dicts.md)

| Задача | `list` | `tuple` | `set` | `dict` |
| :--- | :--- | :--- | :--- | :--- |
| Литерал | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{"a": 1}` |
| Пустой | `[]` | `()` | `set()` ⚠️ не `{}` | `{}` |
| Доступ | `lst[0]`, `lst[-1]` | `t[0]` | — | `d["a"]`, `d.get("a", 0)` |
| Добавить | `lst.append(x)` | нельзя | `s.add(x)` | `d["k"] = v` |
| Есть ли | `x in lst` | `x in t` | `x in s` | `k in d` (по ключам) |

| Задача | Синтаксис |
| :--- | :--- |
| Срез / копия списка | `lst[0:2]` / `lst[:]`, `list(lst)` |
| Распаковка | `x, y = point` |
| Перебор пар словаря | `for k, v in d.items():` |
| Словарь из пар | `dict([("x", 1), ("y", 2)])` |
| Глубокая копия | `copy.deepcopy(nested)` |

## Сложность операций

Теория: [02_collections…](./01_theory/02_collections_lists_tuples_sets_dicts.md), [04_hashability_and_performance.md](./01_theory/04_hashability_and_performance.md)

| Операция | Сложность |
| :--- | :--- |
| `lst[i]`, `lst.append(x)` | O(1) (`append` — в среднем) |
| `lst.insert(0, x)`, `del lst[0]` | O(n) — сдвиг элементов |
| `x in lst`, `x in tuple` | O(n) — перебор |
| `x in set`, `k in dict`, `d[k]` | O(1) в среднем |

| Тип | Изменяемый | Хешируемый |
| :--- | :--- | :--- |
| `int`, `float`, `bool`, `str`, `bytes`, `None` | нет | да |
| `tuple` | нет | да, если все элементы хешируемы |
| `frozenset` | нет | да |
| `list`, `dict`, `set` | да | нет |

## Когда что использовать

| Нужно | Тип |
| :--- | :--- |
| Изменяемая последовательность произвольной длины | `list` |
| «Запись» фиксированной формы, ключ словаря | `tuple` |
| Быстрая проверка «есть ли», уникальность, порядок не важен | `set` |
| Поиск значения по ключу (порядок вставки сохраняется с 3.7) | `dict` |
| Убрать дубли с сохранением порядка | `seen = set()` + цикл, или `list(dict.fromkeys(items))` |

## Изменяемость и идентичность

Теория: [03_mutability_and_identity.md](./01_theory/03_mutability_and_identity.md)

| Сравнение | Смысл | Когда |
| :--- | :--- | :--- |
| `a == b` | равны ли значения (`__eq__`) | числа, строки, коллекции |
| `a is b` | тот же ли объект (`id(a) == id(b)`) | только `is None` и проверка идентичности |

```python
def add_item(item, bucket=None):   # не bucket=[]
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

- ⚠️ `alias = original` не копирует: изменения видны через оба имени.
- ⚠️ `lst[:]` / `list(lst)` — поверхностная копия: вложенные списки остаются общими.
- ⚠️ `[[0] * 3] * 3` — три ссылки на один список; правильно `[[0] * 3 for _ in range(3)]`.
- ⚠️ `x is 1000` / `s is "abc"` — деталь кэша CPython (−5..256, короткие строки); с 3.8 даёт `SyntaxWarning`. Используйте `==`.
- ⚠️ `def f(x=[])` — список создаётся один раз при `def`.

## Хешируемость

Теория: [04_hashability_and_performance.md](./01_theory/04_hashability_and_performance.md)

- `hash([1, 2])` → `TypeError: unhashable type: 'list'`; ключи `dict` и элементы `set` — только хешируемые.
- Составной ключ кэша — кортеж: `cache[("GET", "/users", 1)] = ...`.
- Правило: `a == b` ⇒ `hash(a) == hash(b)`. Определили `__eq__` без `__hash__` → объекты класса нехешируемы.
- ⚠️ `hash()` строк меняется между запусками (`PYTHONHASHSEED`) — не сохраняйте его.
- ⚠️ `{"a": 1, "a": 2}` → `{'a': 2}`: дубль ключа молча перезаписывается.

## Comprehensions

Теория: [05_comprehensions.md](./01_theory/05_comprehensions.md)

| Что | Синтаксис |
| :--- | :--- |
| list | `[x * 2 for x in data if x % 2 == 0]` |
| dict | `{name: len(name) for name in names}` |
| set | `{len(w) for w in words}` |
| generator (ленивый) | `(x ** 2 for x in range(10))` |
| Сплющить матрицу | `[x for row in matrix for x in row]` — порядок `for` как во вложенных циклах |
| Транспонировать | `[[row[i] for row in matrix] for i in range(cols)]` |
| Вычислить один раз (walrus, 3.8+) | `[y for x in data if (y := f(x)) > 0]` |

- Обычно быстрее цикла с `append` на 20–50%, но не на порядки.
- ⚠️ Вложенные `if/else`, побочные эффекты, 3+ уровня — пишите обычный цикл.

## for...else и match

Теория: [06_control_flow.md](./01_theory/06_control_flow.md)

```python
for n in numbers:
    if n < 0:
        break
else:                       # выполнится, только если не было break
    print("Отрицательных нет")

match command:              # Python 3.10+
    case ("move", x, y):            # распаковка последовательности
        ...
    case {"action": "quit"}:        # лишние ключи словаря игнорируются
        ...
    case [first, *rest] if rest:    # guard
        ...
    case _:                         # default
        ...
```

- `match` — для разбора **структуры** (кортежи, словари, `Point(x=0, y=0)`); для пары констант хватает `if/elif`.
- ⚠️ `else` у цикла относится к «не было `break`», а не к пустому циклу.
- ⚠️ Голое имя в `case name:` — это захват (совпадёт с чем угодно), а не сравнение с переменной; константы — через точку (`case Color.RED:`).

# collections: специализированные контейнеры

Стандартный `dict`/`list` покрывают большинство случаев, но для частых
паттернов stdlib даёт более выразительные и часто более быстрые структуры.

## Counter — подсчёт элементов

```python
from collections import Counter

words = "the cat sat on the mat the cat ran".split()
counts = Counter(words)
print(counts)                # Counter({'the': 3, 'cat': 2, 'sat': 1, ...})
print(counts.most_common(2)) # [('the', 3), ('cat', 2)]
```

- Наследует `dict`, но отсутствующий ключ возвращает `0`, а не бросает `KeyError`.
- Арифметика между `Counter`: `c1 + c2`, `c1 - c2` (отбрасывает отрицательные
  и нулевые значения), `c1 & c2` (минимум), `c1 | c2` (максимум) — удобно
  для сравнения мультимножеств.
- `Counter(iterable).update(more_iterable)` — накопление счётчика по частям.

## defaultdict — словарь с фабрикой значений по умолчанию

```python
from collections import defaultdict

groups: defaultdict[str, list[int]] = defaultdict(list)
for n in range(10):
    groups[("even" if n % 2 == 0 else "odd")].append(n)
```

Без `defaultdict` пришлось бы писать `groups.setdefault(key, []).append(n)`
или проверять `if key not in groups`. Фабрика (`list`, `int`, `set`, любая
функция без аргументов) вызывается только при обращении к отсутствующему
ключу — важно не путать с `dict.get(key, [])`, которая не создаёт запись
в словаре.

**Ловушка**: `defaultdict` создаёт запись даже при простом чтении
отсутствующего ключа через `[]` (не только при записи):

```python
d = defaultdict(int)
print(d["missing"])  # 0, но теперь "missing" реально есть в d
print(len(d))          # 1
```

## deque — двусторонняя очередь

```python
from collections import deque

dq = deque(maxlen=3)   # ограниченная по размеру — кольцевой буфер
dq.extend([1, 2, 3, 4])
print(dq)  # deque([2, 3, 4], maxlen=3) — старые элементы вытеснены

dq.appendleft(0)
dq.pop()
```

- `append`/`pop` с обоих концов — O(1). У обычного `list` `pop(0)`/`insert(0, x)`
  — O(n), потому что сдвигает все элементы.
- `maxlen` делает deque готовым кольцевым буфером — удобно для «последние N
  событий», скользящих окон, истории команд.
- Не поддерживает быстрый доступ по индексу в середине — O(n), в отличие от
  `list`. Выбор между `list` и `deque` — по тому, с какого конца работа идёт чаще.

## namedtuple / typing.NamedTuple

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(p.x, p[0])  # доступ и по имени, и по индексу
```

В новом коде обычно предпочитают `typing.NamedTuple` (тот же неизменяемый
tuple-based тип, но с аннотациями типов и поддержкой IDE):

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
```

Оба варианта — иммутабельные, легковесные (без overhead обычного класса на
`__dict__`), сравниваются по значению «из коробки» — хороший выбор для
простых структур данных без поведения.

## ChainMap — обзор поверх нескольких словарей (кратко)

```python
from collections import ChainMap

config = ChainMap(cli_args, env_vars, defaults)
config["timeout"]  # ищет по порядку: cli_args -> env_vars -> defaults
```

Полезно для слоёв конфигурации (аргументы командной строки переопределяют
переменные окружения, которые переопределяют дефолты) без копирования словарей.

## Когда что использовать

| Задача | Структура |
|---|---|
| Подсчёт частоты элементов | `Counter` |
| Группировка по ключу без ручной проверки | `defaultdict` |
| Очередь/стек с быстрыми операциями на обоих концах, скользящее окно | `deque` |
| Простая неизменяемая структура данных без методов | `NamedTuple` |
| Слои конфигурации без копирования | `ChainMap` |

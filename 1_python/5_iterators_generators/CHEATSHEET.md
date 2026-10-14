# Итераторы и генераторы — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.

## Iterable и iterator

Подробно: [01_iterator_protocol.md](./01_theory/01_iterator_protocol.md).

| | Iterable | Iterator |
| :--- | :--- | :--- |
| Методы | `__iter__()` → новый итератор | `__iter__()` → `self` и `__next__()` |
| Примеры | `list`, `tuple`, `str`, `set`, `dict`, `range` | `iter(lst)`, генератор, `map`, `zip`, `enumerate`, `open(...)`, `itertools.*` |
| Повторный проход | да, каждый `iter()` — с начала | нет, одноразовый |
| Конец данных | — | `__next__` бросает `StopIteration` |

| Задача | Код |
| :--- | :--- |
| Получить итератор | `it = iter(obj)` |
| Следующий элемент | `next(it)`; со значением по умолчанию вместо `StopIteration`: `next(it, None)` |
| Это итератор? | `iter(x) is x` |
| Что делает `for x in obj` | `_it = iter(obj)`, затем `next(_it)` до `StopIteration` |

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start
    def __iter__(self) -> "Countdown":
        return self
    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print(list(Countdown(3)))   # [3, 2, 1]
```

## Генераторы

Подробно: [02_generators_and_yield.md](./01_theory/02_generators_and_yield.md),
[03_yield_from_and_subgenerators.md](./01_theory/03_yield_from_and_subgenerators.md),
[07_generator_based_coroutines.md](./01_theory/07_generator_based_coroutines.md).

| Задача | Код |
| :--- | :--- |
| Генераторная функция | любой `def` с `yield` внутри; вызов не выполняет тело, а возвращает генератор |
| Отдать значение и замереть | `yield value` |
| Завершить с результатом | `return value` → `StopIteration.value` |
| Делегировать вложенному iterable | `yield from sub` (значения, `send`/`throw` и `return` подгенератора) |
| Получить `return` подгенератора | `result = yield from inner()` |
| Передать значение внутрь | `gen.send(value)` → результат выражения `x = yield ...` |
| Запустить до первого `yield` («прайминг») | `next(gen)` или `gen.send(None)` |
| Остановить и выполнить `finally` | `gen.close()` (внутри — `GeneratorExit`) |
| Бросить исключение в точку остановки | `gen.throw(exc)` |

```python
def flatten_deep(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten_deep(item)
        else:
            yield item

def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

print(list(flatten_deep([1, [2, 3, [4, 5]], 6])))  # [1, 2, 3, 4, 5, 6]
acc = accumulator()
next(acc)                                          # прайминг, вернул 0
print(acc.send(10), acc.send(5))                   # 10 15
```

## Список или генератор

Подробно: [04_laziness_and_memory.md](./01_theory/04_laziness_and_memory.md),
[05_generator_expressions.md](./01_theory/05_generator_expressions.md).

| | `[x for x in ...]` | `(x for x in ...)` |
| :--- | :--- | :--- |
| Вычисление | сразу, всё | лениво, по одному на `next()` |
| Память | O(N) | O(1) (~200 байт независимо от N) |
| Повторный проход | да | нет |
| `len()`, индекс `[i]` | да | нет |

| Ситуация | Выбор |
| :--- | :--- |
| Данные не влезают в память, построчный файл, поток из сети | генератор |
| Пайплайн `read -> filter -> transform -> write` | цепочка генераторов |
| Бесконечная последовательность | генератор |
| Нужны `len()`, индекс или несколько проходов | список |
| Данных мало и они уже в памяти | список |
| Единственный аргумент агрегатора | `sum(x * x for x in data)` — без лишних скобок |
| Несколько аргументов | `sum((x for x in data), start=100)` — скобки обязательны |

## `itertools`

Подробно: [06_itertools.md](./01_theory/06_itertools.md). Всё возвращает ленивые итераторы.

| Задача | Вызов | Результат |
| :--- | :--- | :--- |
| Склеить источники без `+` | `chain(a, b)` | `a...`, затем `b...` |
| Развернуть список списков | `chain.from_iterable(lists)` | элементы подряд |
| «Срез» итератора | `islice(it, 5)` / `islice(it, 10, 20)` | первые 5 / элементы 10..19 |
| Группировать **соседние** | `groupby(sorted(data, key=k), key=k)` | пары `(ключ, итератор группы)` |
| Размножить итератор | `a, b = tee(it, 2)` | два независимых итератора |
| Счётчик | `count(10, 2)` | 10, 12, 14, ... бесконечно |
| По кругу | `cycle("abc")` | a, b, c, a, ... бесконечно |
| Повтор | `repeat("x", 3)` | x, x, x |
| Декартово произведение | `product([1, 2], "ab")` | `(1,'a') (1,'b') (2,'a') (2,'b')` |
| Упорядоченные выборки | `permutations([1, 2, 3], 2)` | 6 пар |
| Неупорядоченные выборки | `combinations([1, 2, 3], 2)` | 3 пары |

```python
from itertools import groupby, islice, count

words = ["apple", "bob", "avocado", "banana"]
key = lambda w: w[0]
print({k: list(g) for k, g in groupby(sorted(words, key=key), key=key)})
# {'a': ['apple', 'avocado'], 'b': ['bob', 'banana']}
print(list(islice(count(10, 2), 3)))   # [10, 12, 14]
```

## Ловушки

- ⚠️ Второй проход по итератору/генератору молча даёт пусто: `list(gen)` → `[]`.
- ⚠️ `groupby` без предварительной сортировки по тому же ключу → одна и та же группа повторится.
- ⚠️ Группу из `groupby` не материализовали до следующего шага → её данные потеряны.
- ⚠️ После `tee` исходный итератор не трогать; сильно разная скорость клонов → буфер растёт в памяти.
- ⚠️ `count`/`cycle` в `for` без `break`/`islice`/`zip` → бесконечный цикл.
- ⚠️ `list(permutations(...))` на большом входе — факториальный рост.
- ⚠️ `islice` на уже частично прочитанном итераторе продолжает с текущей позиции, а не с начала.
- ⚠️ `gen.send(10)` до первого `next()` → `TypeError: can't send non-None value to a just-started generator`.
- ⚠️ `async def`-корутина — не генератор: её нельзя передать в `for` или `next()`.

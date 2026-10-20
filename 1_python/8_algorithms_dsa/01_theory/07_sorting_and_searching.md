# Сортировка и поиск

## Встроенная сортировка: Timsort

`list.sort()`/`sorted()` в CPython используют Timsort — гибрид merge sort
и insertion sort, оптимизированный под реальные (частично упорядоченные)
данные:

- Гарантированная сложность **O(n log n)** в худшем случае.
- **O(n)** на уже отсортированных или почти отсортированных данных —
  Timsort находит существующие упорядоченные подпоследовательности
  ("runs") и сливает их, не пересортировывая с нуля.
- **Стабильная** сортировка: элементы с равными ключами сохраняют
  взаимный порядок — важно при многоступенчатой сортировке (сначала по
  одному ключу, потом по другому).

```python
data = [{"name": "b", "age": 30}, {"name": "a", "age": 30}, {"name": "c", "age": 25}]

by_age = sorted(data, key=lambda d: d["age"])
# затем стабильная сортировка по имени сохранит относительный порядок
# элементов с одинаковым возрастом из предыдущей сортировки
by_age_then_name = sorted(by_age, key=lambda d: d["name"])
```

Практическое правило: **в реальном коде почти всегда `sorted()`/`.sort()`**,
а не собственная реализация — встроенная сортировка быстрее любой
написанной вручную реализации на Python (написана на C, использует
Timsort). Ручные реализации сортировок — учебное упражнение для понимания
алгоритмов, а не то, что стоит использовать в проде.

## Быстрая сортировка (quicksort) — идея

Divide and conquer («разделяй и властвуй»): выбираем опорный элемент
(pivot), разбиваем массив на "меньше pivot" и "больше pivot", рекурсивно
(см. [05_recursion_basics.md](./05_recursion_basics.md)) сортируем части.

```python
def quicksort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]
    return quicksort(less) + equal + quicksort(greater)
```

Average O(n log n), worst case O(n²) (например, всегда выбирать первый
элемент как pivot на уже отсортированном массиве — каждое разбиение
вырождается в "один элемент против остальных").

## Сортировка слиянием (merge sort) — идея

Гарантированная O(n log n) в любом случае, ценой O(n) дополнительной памяти:

```python
def merge_sort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)

def _merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## Бинарный поиск

Требует **отсортированного** входа, O(log n) вместо O(n) линейного поиска:

```python
def binary_search(items: list[int], target: int) -> int:
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Стандартная библиотека уже даёт готовую реализацию через `bisect`:

```python
import bisect

items = [1, 3, 5, 7, 9]
index = bisect.bisect_left(items, 5)      # индекс, куда вставить 5 (или где он есть)
exists = index < len(items) and items[index] == 5
```

`bisect.bisect_left`/`bisect_right` — не только поиск, но и удобная вставка
с сохранением сортировки (`bisect.insort`) без написания бинарного поиска руками.

## Бинарный поиск на модифицированных условиях

Частый паттерн продвинутых задач — бинарный поиск не по значению
напрямую, а по **булеву предикату**, монотонному на отрезке (найти первую
позицию, где условие становится истинным):

```python
def find_first_true(predicate, low: int, high: int) -> int:
    """predicate монотонен: False...False True...True на [low, high]."""
    while low < high:
        mid = (low + high) // 2
        if predicate(mid):
            high = mid
        else:
            low = mid + 1
    return low
```

Применимо и к отсортированному массиву с поворотом ("rotated sorted
array"), и к задачам "минимальное значение X, при котором выполняется
условие" (бинарный поиск по ответу).

## Сравнение сложностей поиска

| Метод | Требование | Сложность |
|---|---|---|
| Линейный поиск (`in`, цикл) | нет | O(n) |
| Бинарный поиск | отсортированный вход | O(log n) |
| Поиск по ключу в `dict`/`set` | хешируемый ключ | O(1) в среднем |

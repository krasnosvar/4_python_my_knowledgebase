# Алгоритмы и структуры данных — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/), начиная с
[01_big_o_notation.md](./01_theory/01_big_o_notation.md). ⚠️ — частая
ловушка производительности.

## Классы сложности

Подробнее: [01_big_o_notation.md](./01_theory/01_big_o_notation.md).

| O(...) | Название | Пример |
| :--- | :--- | :--- |
| O(1) | константная | `l[i]`, `d[key]`, `x in s` (set) |
| O(log n) | логарифмическая | бинарный поиск, `heappush`/`heappop` |
| O(n) | линейная | один проход по списку, `x in l` |
| O(n log n) | линейно-логарифмическая | `sorted()`, merge sort |
| O(n²) | квадратичная | вложенные циклы по одному входу |
| O(2ⁿ) | экспоненциальная | наивная рекурсия Фибоначчи |
| O(n!) | факториальная | перебор всех перестановок |

Последовательные циклы складываются (`O(n) + O(n) = O(n)`), вложенные —
перемножаются (`O(n) · O(n) = O(n²)`).

## Стоимость операций встроенных структур

| Структура | Операция | Сложность |
| :--- | :--- | :--- |
| `list` | `l[i]`, `l[i] = x`, `len(l)` | O(1) |
| `list` | `append(x)`, `pop()` (с конца) | O(1) амортизированно |
| `list` | `insert(0, x)`, `pop(0)` ⚠️ | O(n) — сдвиг всех элементов |
| `list` | `x in l`, `l.index(x)`, `l.remove(x)` | O(n) |
| `list` | срез `l[a:b]` | O(b − a) — копия |
| `list` | `l.sort()` / `sorted(l)` | O(n log n), O(n) на почти отсортированных |
| `dict` / `set` | вставка, поиск, удаление, `in` | O(1) в среднем, O(n) в худшем (коллизии) |
| `deque` | `append` / `appendleft` / `pop` / `popleft` | O(1) |
| `heapq` | `heapify(l)` | O(n) |
| `heapq` | `heappush` / `heappop` | O(log n) |
| `heapq` | `nlargest(k, it)` / `nsmallest(k, it)` | O(n log k) |
| `bisect` | `bisect_left` / `bisect_right` | O(log n) |
| `bisect` | `insort(l, x)` | O(log n) поиск + O(n) вставка |
| `str` | `s += t` в цикле ⚠️ | O(n²) суммарно — используйте `"".join(parts)` |

## Какую структуру взять

Подробнее: [04_stacks_and_queues.md](./01_theory/04_stacks_and_queues.md),
[06_trees_and_hash_tables.md](./01_theory/06_trees_and_hash_tables.md).

| Задача | Структура |
| :--- | :--- |
| Отмена последнего действия, скобки, DFS | стек: `list` + `append`/`pop` |
| Обработка по порядку поступления, BFS | очередь: `collections.deque` + `append`/`popleft` |
| Всегда нужен текущий минимум/максимум, top-K | `heapq` (только min-heap; max — через `-x`) |
| Быстрый поиск по ключу, порядок не важен | `dict` / `set` |
| Отсортированный порядок, диапазонные запросы | `bisect` над отсортированным списком |
| Иерархия (ФС, DOM, оргструктура) | дерево |
| LRU-кэш, O(1) удаление по ключу | `collections.OrderedDict` / `dict`, не самописный связный список |

## Паттерны на массивах и строках

Подробнее: [02_arrays_and_strings.md](./01_theory/02_arrays_and_strings.md).

| Паттерн | Когда | Сложность |
| :--- | :--- | :--- |
| Два указателя с концов | палиндром, пара с суммой в отсортированном | O(n) времени, O(1) памяти |
| Скользящее окно | самый длинный/короткий подотрезок со свойством | O(n) вместо O(n²) |
| Префиксные суммы | много запросов «сумма на `[l, r)`» | O(n) подготовка, O(1) на запрос |
| Хеш-таблица «видели ли» | пара с суммой (two sum), дубликаты | O(n) времени, O(n) памяти |
| Сортировка + линейный проход | упростить задачу ценой O(n log n) | O(n log n) |
| Быстрый/медленный указатель | середина связного списка, поиск цикла | O(n), O(1) памяти |

```python
def two_sum(nums, target):            # хеш-таблица вместо вложенного цикла
    seen = {}                          # значение -> индекс
    for i, x in enumerate(nums):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None

def longest_unique_substring(s):       # скользящее окно
    seen, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best

prefix = [0]                            # префиксные суммы
for x in [3, 1, 4, 1, 5]:
    prefix.append(prefix[-1] + x)
print(two_sum([2, 7, 11, 15], 9), longest_unique_substring("abcabcbb"), prefix[4] - prefix[1])
# (0, 1) 3 6
```

## Обходы: BFS и DFS

Подробнее: [04_stacks_and_queues.md](./01_theory/04_stacks_and_queues.md),
[06_trees_and_hash_tables.md](./01_theory/06_trees_and_hash_tables.md).

| Обход | Структура | Порядок |
| :--- | :--- | :--- |
| BFS (в ширину) | очередь `deque` | «волнами» по расстоянию от старта |
| DFS (в глубину) | стек `list` или рекурсия | по одному пути до упора, затем откат |
| In-order (BST) | рекурсия | левое → узел → правое: **отсортированный** порядок |
| Pre-order / post-order | рекурсия | узел → дети / дети → узел |

```python
from collections import deque

graph = {1: [2, 3], 2: [4], 3: [4], 4: []}

def bfs_levels(graph, start):
    visited, queue, levels = {start}, deque([start]), []
    while queue:
        level = []
        for _ in range(len(queue)):        # размер очереди = ширина уровня
            node = queue.popleft()
            level.append(node)
            for nb in graph[node]:
                if nb not in visited:       # отмечаем при постановке в очередь
                    visited.add(nb)
                    queue.append(nb)
        levels.append(level)
    return levels

def dfs_iterative(graph, start):           # явный стек вместо рекурсии
    visited, stack, order = set(), [start], []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        stack.extend(reversed(graph[node]))
    return order

print(bfs_levels(graph, 1), dfs_iterative(graph, 1))
# [[1], [2, 3], [4]] [1, 2, 4, 3]
```

## Сортировка и поиск

Подробнее: [07_sorting_and_searching.md](./01_theory/07_sorting_and_searching.md).

| Алгоритм | Лучший | Средний | Худший | Память | Стабильна |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Timsort (`sorted`, `.sort()`) | O(n) | O(n log n) | O(n log n) | O(n) | да |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | да |
| Quicksort | O(n log n) | O(n log n) | O(n²) — плохой pivot | O(log n) стек* | нет* |
| Линейный поиск (`in`) | O(1) | O(n) | O(n) | O(1) | — |
| Бинарный поиск / `bisect` | O(1) | O(log n) | O(log n) | O(1) | — |

\* для классической in-place версии; учебная версия из теории со списками
`less`/`equal`/`greater` тратит O(n) памяти и сохраняет порядок равных.

```python
import bisect

items = [1, 3, 5, 7, 9]
i = bisect.bisect_left(items, 5)                 # куда вставить / где лежит 5
print(i, i < len(items) and items[i] == 5)       # 2 True
bisect.insort(items, 4)                          # вставка с сохранением порядка
print(items)                                     # [1, 3, 4, 5, 7, 9]

def find_first_true(pred, low, high):            # бинарный поиск по ответу
    while low < high:                            # pred: False…False True…True
        mid = (low + high) // 2
        if pred(mid):
            high = mid
        else:
            low = mid + 1
    return low

print(find_first_true(lambda x: x * x >= 50, 0, 100))   # 8

data = [("b", 30), ("a", 30), ("c", 25)]
print(sorted(data, key=lambda p: (p[1], p[0])))  # несколько ключей одним кортежем
# [('c', 25), ('a', 30), ('b', 30)]
```

## Рекурсия и динамическое программирование

Подробнее: [05_recursion_basics.md](./01_theory/05_recursion_basics.md),
[08_dynamic_programming.md](./01_theory/08_dynamic_programming.md).

| Вопрос | Ответ |
| :--- | :--- |
| Из чего состоит рекурсия | базовый случай + переход к меньшей задаче |
| Лимит глубины | `sys.getrecursionlimit()` — по умолчанию 1000, дальше `RecursionError` |
| Хвостовая рекурсия | CPython её **не** оптимизирует |
| Признаки задачи на DP | оптимальная подструктура + перекрывающиеся подзадачи |
| Первый шаг оптимизации | `@lru_cache(maxsize=None)` (или `@functools.cache`) — top-down |
| Нет риска `RecursionError`, предсказуемая память | табуляция снизу вверх (bottom-up) |
| Когда DP не поможет | подзадачи не пересекаются: merge sort, бинарный поиск |

```python
from functools import lru_cache

@lru_cache(maxsize=None)                  # top-down: O(n) вместо O(2ⁿ)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def coin_change(coins, amount):           # bottom-up: O(amount · len(coins))
    INF = float("inf")
    dp = [0] + [INF] * amount             # dp[i] — минимум монет для суммы i
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1

print(fib(50), coin_change([1, 2, 5], 11), coin_change([2], 3))
# 12586269025 3 -1
```

## Типичные ошибки

- ⚠️ `x in big_list` внутри цикла — O(n²); сначала `s = set(big_list)`.
- ⚠️ `list.pop(0)` / `insert(0, x)` как очередь — O(n) на операцию; берите `deque`.
- ⚠️ `s += part` в цикле — O(n²); копите в список и делайте `"".join(parts)`.
- ⚠️ BST из уже отсортированных данных вырождается в цепочку — O(n) вместо O(log n).
- ⚠️ Quicksort с первым элементом как pivot на отсортированном входе — O(n²).
- ⚠️ `heapq` — только min-heap; для max-heap кладите `-x` или `(-priority, item)`.
- ⚠️ Бинарный поиск по **несортированному** списку молча вернёт неверный ответ.
- ⚠️ Реверс связного списка: сохраните `curr.next` до перезаписи, иначе потеряете хвост.
- ⚠️ `sys.setrecursionlimit()` не лечит глубокую рекурсию — перепишите на явный стек.
- ⚠️ Ручная сортировка в проде — используйте `sorted()`/`.sort()` (Timsort на C).

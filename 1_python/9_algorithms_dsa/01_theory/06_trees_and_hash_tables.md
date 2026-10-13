# Деревья и хеш-таблицы

Обходы и вставка в дерево ниже записаны рекурсивно — если рекурсия ещё
непривычна, сначала прочитайте [05_recursion_basics.md](./05_recursion_basics.md).

## Бинарное дерево: определение и обходы

**Бинарное дерево** — структура из узлов, где у каждого узла есть значение
и не больше двух «детей»: левый и правый узел. Верхний узел называется
корнем, узлы без детей — листьями. Каждый ребёнок сам является корнем
меньшего дерева (поддерева) — поэтому деревья так естественно
обрабатывать рекурсией.

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None
```

### Обходы в глубину (DFS): pre-order, in-order, post-order

```python
def preorder(node: TreeNode | None) -> list[int]:
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right)

def inorder(node: TreeNode | None) -> list[int]:
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

def postorder(node: TreeNode | None) -> list[int]:
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.value]
```

Для **бинарного дерева поиска (BST)** in-order обход всегда даёт значения
в отсортированном порядке — это ключевое свойство, на котором строятся
многие BST-алгоритмы (проверка корректности BST, поиск k-го наименьшего).

### Обход в ширину (BFS) по уровням

```python
from collections import deque

def level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    levels = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels
```

## Бинарное дерево поиска (BST): поиск, вставка

```python
def bst_search(node: TreeNode | None, target: int) -> bool:
    if node is None:
        return False
    if node.value == target:
        return True
    return bst_search(node.left if target < node.value else node.right, target)

def bst_insert(node: TreeNode | None, value: int) -> TreeNode:
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = bst_insert(node.left, value)
    else:
        node.right = bst_insert(node.right, value)
    return node
```

Сложность поиска/вставки в BST — O(log n) для **сбалансированного**
дерева, но O(n) в худшем случае (дерево выродилось в цепочку, например
после вставки уже отсортированных данных). Самобалансирующиеся деревья
(AVL, red-black) решают эту проблему гарантированным O(log n) — в стандартной
библиотеке Python готовой реализации нет, для практики обычно достаточно
`dict`/`heapq`/`bisect` поверх обычного списка вместо ручного дерева.

## heapq — двоичная куча (heap)

Куча — не то же самое, что дерево поиска: гарантирует быстрый доступ
только к **минимуму** (или максимуму), а не полную сортировку.

```python
import heapq

nums = [5, 1, 8, 2, 9]
heapq.heapify(nums)              # O(n) — превращает список в min-heap на месте
smallest = heapq.heappop(nums)   # O(log n) — извлечь минимум
heapq.heappush(nums, 3)          # O(log n) — добавить элемент
```

`heapq` в Python реализует только **min-heap**. Для max-heap — либо
хранить отрицательные значения, либо обернуть в кортеж с инвертированным
ключом:

```python
max_heap = [-x for x in nums]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)
```

### Типичное применение: top-K элементов

```python
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    from collections import Counter
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)
```

`heapq.nlargest`/`heapq.nsmallest` — O(n log k), эффективнее полной
сортировки O(n log n), когда `k` заметно меньше `n`.

## Хеш-таблицы: dict и set

`dict`/`set` в CPython реализованы как хеш-таблицы: O(1) в среднем на
вставку/поиск/удаление за счёт вычисления хеша ключа и прямого доступа
по слоту, O(n) в худшем случае при массовых коллизиях хешей (на практике
крайне редко при разумных ключах).

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}   # значение -> индекс
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:               # O(1) в среднем
            return seen[complement], i
        seen[x] = i
    return None
```

Классический паттерн: заменить вложенный цикл (O(n²) — искать пару
перебором) на один проход с хеш-таблицей (O(n) времени, O(n) памяти) —
компромисс "время за счёт памяти" встречается в задачах на массивы
постоянно.

## Когда дерево, когда хеш-таблица

| Задача | Структура |
|---|---|
| Нужен порядок (отсортированный обход, диапазонные запросы) | дерево / `bisect` над отсортированным списком |
| Нужен только быстрый поиск по ключу, порядок не важен | `dict`/`set` |
| Нужен постоянный доступ к минимуму/максимуму среди текущих | `heapq` |
| Иерархические данные (файловая система, DOM, оргструктура) | дерево |

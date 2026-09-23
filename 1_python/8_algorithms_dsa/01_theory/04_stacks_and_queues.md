# Стек и очередь

## Стек (LIFO — last in, first out)

`list` — естественный стек в Python: `append`/`pop` (без аргумента, с
конца) — обе операции O(1) амортизированно.

```python
stack: list[int] = []
stack.append(1)
stack.append(2)
stack.append(3)
top = stack.pop()   # 3 — последний добавленный уходит первым
```

**Важно**: `pop(0)` (с начала списка) — O(n), потому что сдвигает все
элементы. Стек должен работать только с концом списка.

### Типичное применение: проверка сбалансированности скобок

```python
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack
```

Стек хранит "открытые" скобки; при встрече закрывающей — проверяем, что
верхний элемент стека ей соответствует.

### Типичное применение: вычисление выражений (RPN)

```python
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "*": lambda a, b: a * b, "/": lambda a, b: int(a / b)}
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()   # порядок важен для - и /
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]
```

## Очередь (FIFO — first in, first out)

`collections.deque` — правильный выбор для очереди: `append`/`popleft`
— обе O(1). **Не используйте `list.pop(0)`** для очереди — O(n) на каждое
извлечение из-за сдвига всех оставшихся элементов.

```python
from collections import deque

queue: deque[int] = deque()
queue.append(1)
queue.append(2)
first = queue.popleft()   # 1 — первый добавленный уходит первым
```

### Типичное применение: обход в ширину (BFS)

```python
from collections import deque

def bfs_levels(graph: dict[int, list[int]], start: int) -> list[list[int]]:
    visited = {start}
    queue = deque([start])
    levels = []
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        levels.append(level)
    return levels
```

Обработка "по уровням" (level_size = текущий размер очереди перед началом
уровня) — стандартный паттерн BFS для деревьев/графов, когда важна
группировка по расстоянию от старта.

## Стек через две очереди / очередь через два стека

Классическое учебное упражнение на понимание структур: показать, что одну
структуру можно эмулировать другой ценой амортизированной сложности
операций (см. упражнение `08_queue_using_two_stacks`).

## Приоритетная очередь — отдельная структура

Стек и очередь извлекают строго по порядку вставки (с одного из концов).
Когда нужно всегда извлекать **наименьший/наибольший** элемент — это уже
не стек/очередь, а heap (см. следующую тему, `heapq`).

## Когда что выбрать

| Задача | Структура |
|---|---|
| Отмена последнего действия, разбор вложенных скобок/выражений, DFS | стек (`list` + `append`/`pop`) |
| Обработка в порядке поступления, BFS, rate-limiting окна | очередь (`collections.deque`) |
| Всегда нужен минимум/максимум среди текущих элементов | heap (`heapq`) |

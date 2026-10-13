"""
Стек через list, очередь через deque, проверка скобок, BFS по графу.

Запуск: python main.py
"""
from __future__ import annotations

from collections import deque


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


def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),
    }
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]


def bfs_levels(graph: dict[int, list[int]], start: int) -> list[list[int]]:
    visited = {start}
    queue = deque([start])
    levels = []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        levels.append(level)
    return levels


def main() -> None:
    print("--- стек: проверка скобок ---")
    for s in ["([]{})", "([)]", "((("]:
        print(f"{s!r} -> {is_balanced(s)}")

    print("\n--- стек: вычисление RPN ---")
    print(eval_rpn(["2", "1", "+", "3", "*"]))  # (2+1)*3 = 9

    print("\n--- очередь: BFS по уровням ---")
    graph = {1: [2, 3], 2: [4], 3: [4], 4: []}
    print(bfs_levels(graph, 1))  # [[1], [2, 3], [4]]


if __name__ == "__main__":
    main()

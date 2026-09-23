"""
Бинарное дерево (обходы, BST insert/search), heapq для top-K,
хеш-таблица для two_sum.

Запуск: python main.py
"""
from __future__ import annotations

import heapq
from collections import Counter, deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def inorder(node: TreeNode | None) -> list[int]:
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)


def bst_insert(node: TreeNode | None, value: int) -> TreeNode:
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = bst_insert(node.left, value)
    else:
        node.right = bst_insert(node.right, value)
    return node


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


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return seen[complement], i
        seen[x] = i
    return None


def main() -> None:
    print("--- BST: вставка + in-order обход даёт отсортированный список ---")
    root = None
    for v in [5, 3, 8, 1, 4, 7, 9]:
        root = bst_insert(root, v)
    print(inorder(root))

    print("\n--- level_order обход дерева ---")
    print(level_order(root))

    print("\n--- heapq: top-K частых элементов ---")
    print(top_k_frequent([1, 1, 1, 2, 2, 3], k=2))  # [1, 2]

    print("\n--- хеш-таблица: two_sum ---")
    print(two_sum([2, 7, 11, 15], target=9))  # (0, 1)


if __name__ == "__main__":
    main()

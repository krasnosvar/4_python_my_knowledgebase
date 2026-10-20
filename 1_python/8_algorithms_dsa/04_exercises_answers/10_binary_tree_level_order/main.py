"""Решение: 10_binary_tree_level_order"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


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


def main() -> None:
    checks_passed = 0
    total_checks = 3
    root = TreeNode(1,
        left=TreeNode(2, left=TreeNode(4), right=TreeNode(5)),
        right=TreeNode(3, right=TreeNode(6)),
    )

    result = level_order(root)
    assert result == [[1], [2, 3], [4, 5, 6]], f"получили {result}"
    checks_passed += 1

    assert level_order(None) == []
    checks_passed += 1
    assert level_order(TreeNode(1)) == [[1]]
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

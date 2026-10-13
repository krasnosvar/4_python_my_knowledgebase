"""
Задача (средний уровень): обойти бинарное дерево в ширину (BFS),
группируя значения по уровням.

Запусти: python main.py
"""
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
    """
    TODO: используя collections.deque как очередь, обойти дерево по
    уровням. На каждой итерации внешнего цикла зафиксировать текущий
    размер очереди (level_size = len(queue)) и обработать ровно
    столько узлов, добавляя их детей в очередь для следующего уровня.
    Вернуть список списков значений по уровням.
    """
    raise NotImplementedError


def main() -> None:
    #         1
    #        / \
    #       2   3
    #      / \   \
    #     4   5   6
    root = TreeNode(1,
        left=TreeNode(2, left=TreeNode(4), right=TreeNode(5)),
        right=TreeNode(3, right=TreeNode(6)),
    )

    result = level_order(root)
    assert result == [[1], [2, 3], [4, 5, 6]], f"получили {result}"

    assert level_order(None) == []
    assert level_order(TreeNode(1)) == [[1]]

    print("Все тесты прошли:", result)


if __name__ == "__main__":
    main()

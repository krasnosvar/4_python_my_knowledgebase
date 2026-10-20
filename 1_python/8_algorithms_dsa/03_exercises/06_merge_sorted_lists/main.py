"""
Задача (средний уровень): слить два отсортированных связных списка в
один отсортированный список, O(n + m) времени, без создания новых узлов
(переиспользуй существующие).

Запусти: python main.py
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    value: int
    next: Optional["ListNode"] = None


def from_list(values: list[int]) -> ListNode | None:
    head = None
    for v in reversed(values):
        head = ListNode(v, next=head)
    return head


def to_list(head: ListNode | None) -> list[int]:
    result = []
    node = head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result


def merge_two_lists(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """
    TODO: использовать dummy-узел и указатель tail. Пока оба списка
    непусты — сравнивать головы, присоединять к tail меньший узел,
    сдвигать соответствующий указатель списка и tail. После цикла
    присоединить остаток непустого списка (l1 или l2) целиком.
    Вернуть dummy.next.
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 4
    l1 = from_list([1, 3, 5])
    l2 = from_list([2, 4, 6])
    merged = merge_two_lists(l1, l2)
    assert to_list(merged) == [1, 2, 3, 4, 5, 6]
    checks_passed += 1

    assert to_list(merge_two_lists(None, from_list([1, 2]))) == [1, 2]
    checks_passed += 1
    assert to_list(merge_two_lists(from_list([1, 2]), None)) == [1, 2]
    checks_passed += 1
    assert merge_two_lists(None, None) is None
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

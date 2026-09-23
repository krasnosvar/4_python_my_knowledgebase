"""Решение: 06_merge_sorted_lists"""
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
    dummy = ListNode(0)
    tail = dummy
    while l1 is not None and l2 is not None:
        if l1.value <= l2.value:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 if l1 is not None else l2
    return dummy.next


def main() -> None:
    l1 = from_list([1, 3, 5])
    l2 = from_list([2, 4, 6])
    merged = merge_two_lists(l1, l2)
    assert to_list(merged) == [1, 2, 3, 4, 5, 6]

    assert to_list(merge_two_lists(None, from_list([1, 2]))) == [1, 2]
    assert to_list(merge_two_lists(from_list([1, 2]), None)) == [1, 2]
    assert merge_two_lists(None, None) is None

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

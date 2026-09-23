"""Решение: 04_reverse_linked_list"""
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


def reverse(head: ListNode | None) -> ListNode | None:
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev


def main() -> None:
    head = from_list([1, 2, 3, 4, 5])
    reversed_head = reverse(head)
    assert to_list(reversed_head) == [5, 4, 3, 2, 1]

    empty_result = reverse(None)
    assert empty_result is None

    single = from_list([42])
    assert to_list(reverse(single)) == [42]

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

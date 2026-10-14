"""Решение: 05_detect_cycle_linked_list"""
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


def make_cycle(head: ListNode, pos: int) -> ListNode:
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    nodes[-1].next = nodes[pos]
    return head


def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def main() -> None:
    checks_passed = 0
    total_checks = 4
    no_cycle = from_list([1, 2, 3, 4])
    assert has_cycle(no_cycle) is False
    checks_passed += 1

    with_cycle = make_cycle(from_list([1, 2, 3, 4]), pos=1)
    assert has_cycle(with_cycle) is True
    checks_passed += 1

    assert has_cycle(None) is False
    checks_passed += 1

    single_no_cycle = from_list([1])
    assert has_cycle(single_no_cycle) is False
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

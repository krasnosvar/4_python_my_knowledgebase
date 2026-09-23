"""
Реализация связного списка: обход, вставка/удаление, реверс,
поиск середины (slow/fast pointer), обнаружение цикла.

Запуск: python main.py
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


def reverse(head: ListNode | None) -> ListNode | None:
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev


def find_middle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def main() -> None:
    head = from_list([1, 2, 3, 4, 5])
    print(f"исходный список: {to_list(head)}")

    reversed_head = reverse(head)
    print(f"развёрнутый:     {to_list(reversed_head)}")

    head2 = from_list([1, 2, 3, 4, 5])
    middle = find_middle(head2)
    print(f"середина списка [1,2,3,4,5]: {middle.value}")  # 3

    head3 = from_list([1, 2, 3])
    print(f"есть цикл (нет цикла): {has_cycle(head3)}")

    head3.next.next.next = head3.next  # искусственно создаём цикл на узел "2"
    print(f"есть цикл (после создания цикла): {has_cycle(head3)}")


if __name__ == "__main__":
    main()

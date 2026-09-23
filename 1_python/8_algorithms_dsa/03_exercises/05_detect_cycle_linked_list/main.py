"""
Задача (средний уровень): определить, есть ли цикл в связном списке,
используя алгоритм Флойда (slow/fast pointer), O(n) времени, O(1) памяти.

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


def make_cycle(head: ListNode, pos: int) -> ListNode:
    """Создаёт цикл: последний узел указывает на узел с индексом pos."""
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    nodes[-1].next = nodes[pos]
    return head


def has_cycle(head: ListNode | None) -> bool:
    """
    TODO: два указателя slow и fast, оба начинают с head. slow двигается
    на 1 узел за шаг, fast — на 2. Если fast (или fast.next) станет None —
    цикла нет. Если slow и fast когда-нибудь совпадут (slow is fast) —
    цикл есть.
    """
    raise NotImplementedError


def main() -> None:
    no_cycle = from_list([1, 2, 3, 4])
    assert has_cycle(no_cycle) is False

    with_cycle = make_cycle(from_list([1, 2, 3, 4]), pos=1)
    assert has_cycle(with_cycle) is True

    assert has_cycle(None) is False

    single_no_cycle = from_list([1])
    assert has_cycle(single_no_cycle) is False

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

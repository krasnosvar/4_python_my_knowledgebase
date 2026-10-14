"""Решение: 08_queue_using_two_stacks"""
from __future__ import annotations


class QueueViaStacks:
    def __init__(self) -> None:
        self._in_stack: list[int] = []
        self._out_stack: list[int] = []

    def enqueue(self, value: int) -> None:
        self._in_stack.append(value)

    def dequeue(self) -> int:
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())
        if not self._out_stack:
            raise IndexError("dequeue from empty queue")
        return self._out_stack.pop()

    def is_empty(self) -> bool:
        return not self._in_stack and not self._out_stack


def main() -> None:
    checks_passed = 0
    total_checks = 6
    q = QueueViaStacks()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    assert q.dequeue() == 1
    checks_passed += 1
    q.enqueue(4)
    assert q.dequeue() == 2
    checks_passed += 1
    assert q.dequeue() == 3
    checks_passed += 1
    assert q.dequeue() == 4
    checks_passed += 1
    assert q.is_empty()
    checks_passed += 1

    try:
        q.dequeue()
        assert False, "должно было бросить IndexError"
    except IndexError:
        pass
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

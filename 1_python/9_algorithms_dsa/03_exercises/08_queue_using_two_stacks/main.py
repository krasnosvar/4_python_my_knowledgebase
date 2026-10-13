"""
Задача (средний уровень): реализовать очередь (FIFO) с использованием
только двух стеков (списков с append/pop с конца). enqueue — O(1)
амортизированно, dequeue — O(1) амортизированно (O(n) в худшем случае,
но каждый элемент переносится между стеками не более одного раза).

Запусти: python main.py
"""
from __future__ import annotations


class QueueViaStacks:
    def __init__(self) -> None:
        self._in_stack: list[int] = []
        self._out_stack: list[int] = []

    def enqueue(self, value: int) -> None:
        """TODO: просто добавить value в _in_stack (append)."""
        raise NotImplementedError

    def dequeue(self) -> int:
        """
        TODO:
          1. Если _out_stack пуст — перелить ВСЕ элементы из _in_stack
             в _out_stack (по одному через pop/append) — это разворачивает
             порядок и делает первый вставленный элемент верхним в _out_stack.
          2. Если после этого _out_stack всё ещё пуст — бросить IndexError
             ("dequeue from empty queue").
          3. Вернуть _out_stack.pop().
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        return not self._in_stack and not self._out_stack


def main() -> None:
    q = QueueViaStacks()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    assert q.dequeue() == 1
    q.enqueue(4)
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    assert q.is_empty()

    try:
        q.dequeue()
        assert False, "должно было бросить IndexError"
    except IndexError:
        pass

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

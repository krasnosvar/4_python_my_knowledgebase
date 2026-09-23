"""Решение: 02_find_and_break_reference_cycle"""
from __future__ import annotations

import gc
import weakref


destroyed: list[str] = []


class StrongNode:
    def __init__(self, name: str) -> None:
        self.name = name
        self.other: "StrongNode | None" = None

    def __del__(self):
        destroyed.append(self.name)


def create_cycle_and_collect() -> int:
    gc.disable()

    a = StrongNode("a")
    b = StrongNode("b")
    a.other = b
    b.other = a

    del a
    del b

    collected = gc.collect()
    gc.enable()
    return collected


class WeakNode:
    def __init__(self, name: str) -> None:
        self.name = name
        self.other: "weakref.ReferenceType[WeakNode] | None" = None

    def __del__(self):
        destroyed.append(self.name)


def create_without_cycle() -> None:
    c = WeakNode("c")
    d = WeakNode("d")
    c.other = weakref.ref(d)
    d.other = weakref.ref(c)

    del c
    del d


def main() -> None:
    collected = create_cycle_and_collect()
    assert collected >= 2, f"gc.collect() должен был собрать хотя бы 2 объекта, собрал {collected}"
    assert set(destroyed) == {"a", "b"}, f"ожидали {{'a', 'b'}}, получили {set(destroyed)}"

    destroyed.clear()
    create_without_cycle()
    assert set(destroyed) == {"c", "d"}, f"ожидали {{'c', 'd'}}, получили {set(destroyed)}"

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

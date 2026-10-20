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
    checks_passed = 0
    total_checks = 3
    collected = create_cycle_and_collect()
    assert collected >= 2, f"gc.collect() должен был собрать хотя бы 2 объекта, собрал {collected}"
    checks_passed += 1
    assert set(destroyed) == {"a", "b"}, f"ожидали {{'a', 'b'}}, получили {set(destroyed)}"
    checks_passed += 1

    destroyed.clear()
    create_without_cycle()
    assert set(destroyed) == {"c", "d"}, f"ожидали {{'c', 'd'}}, получили {set(destroyed)}"
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

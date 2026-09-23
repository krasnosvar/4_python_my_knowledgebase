"""
gc module: циклические ссылки, которые refcounting не может собрать сам,
generational collector, weakref как альтернатива.

Запуск: python main.py
"""
from __future__ import annotations

import gc
import weakref


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.other: "Node | None" = None

    def __del__(self):
        print(f"Node({self.name!r}) уничтожен")


def demo_cycle_needs_gc() -> None:
    print("--- цикл ссылок: refcounting не справляется сам ---")
    gc.disable()  # отключаем автоматический GC, чтобы показать эффект явно

    a = Node("a")
    b = Node("b")
    a.other = b
    b.other = a

    del a
    del b
    print("после del a, del b — сообщения об уничтожении ЕЩЁ НЕТ (цикл жив)")

    collected = gc.collect()
    print(f"gc.collect() нашёл и уничтожил объектов: {collected}")

    gc.enable()


def demo_weakref_avoids_cycle() -> None:
    print("\n--- weakref: изначально не создаём цикл ---")

    class Parent:
        def __init__(self):
            self.children: list[Node] = []

    class Child:
        def __init__(self, parent):
            self.parent = weakref.ref(parent)  # слабая ссылка — без цикла

        def __del__(self):
            print("Child уничтожен немедленно (refcounting сработал сам)")

    parent = Parent()
    child = Child(parent)
    parent.children.append(child)

    del child
    print("Child удалён через обычный del — сообщение об уничтожении уже выше")


def demo_is_tracked() -> None:
    print("\n--- gc.is_tracked: какие объекты вообще может отслеживать GC ---")
    print(f"list:  {gc.is_tracked([1, 2])}")
    print(f"tuple: {gc.is_tracked((1, 2))}")
    print(f"str:   {gc.is_tracked('hello')}")


def main() -> None:
    demo_cycle_needs_gc()
    demo_weakref_avoids_cycle()
    demo_is_tracked()


if __name__ == "__main__":
    main()

"""
Задача: создать циклическую структуру ссылок (родитель <-> ребёнок),
показать, что refcounting не может её уничтожить сам (нужен gc.collect()),
затем переписать структуру через weakref так, чтобы цикл вообще не
образовывался и объект уничтожался немедленно через обычный del.

Запусти: python main.py
"""
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
    """
    TODO:
      1. gc.disable() (чтобы явно контролировать момент сборки).
      2. Создать a = StrongNode("a"), b = StrongNode("b"),
         a.other = b, b.other = a (цикл).
      3. del a, del b.
      4. Вернуть результат gc.collect() (число собранных объектов),
         не забыть gc.enable() перед возвратом.
    """
    raise NotImplementedError


class WeakNode:
    def __init__(self, name: str) -> None:
        self.name = name
        self.other: "weakref.ReferenceType[WeakNode] | None" = None

    def __del__(self):
        destroyed.append(self.name)


def create_without_cycle() -> None:
    """
    TODO: создать c = WeakNode("c"), d = WeakNode("d"), связать их через
    weakref.ref (c.other = weakref.ref(d), d.other = weakref.ref(c)) —
    без образования настоящего цикла ссылок. Затем del c, del d.
    Оба объекта должны быть уничтожены НЕМЕДЛЕННО (без gc.collect()).
    """
    raise NotImplementedError


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

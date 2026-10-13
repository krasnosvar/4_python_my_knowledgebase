"""Решение: хешируемый класс-значение.

Синтаксис class разбирается в 4_oop; здесь важны только тела __eq__ и
__hash__: равные точки обязаны давать равный хеш.
"""


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def _self_check() -> None:
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)

    assert p1 == p2, "Точки с одинаковыми координатами должны быть равны"
    print("PASS: Point(1, 2) == Point(1, 2)")

    assert p1 != p3, "Точки с разными координатами не должны быть равны"
    print("PASS: Point(1, 2) != Point(3, 4)")

    assert hash(p1) == hash(p2), "Равные объекты обязаны иметь равный hash()"
    print("PASS: hash(p1) == hash(p2)")

    points_set = {p1, p2, p3}
    assert len(points_set) == 2, f"Ожидалось 2 уникальных точки в множестве, получено {len(points_set)}"
    print("PASS: множество дедуплицировало Point(1, 2) и Point(1, 2)")

    lookup = {p1: "первая точка"}
    assert lookup[p2] == "первая точка", "Point(1, 2) должен находить значение, положенное под p1"
    print("PASS: p2 находит значение, сохранённое под равным ему p1, в словаре")

    print("\nВсе проверки пройдены")


if __name__ == "__main__":
    _self_check()

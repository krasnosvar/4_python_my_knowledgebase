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
    checks_passed = 0
    total_checks = 5

    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)

    assert p1 == p2, "Точки с одинаковыми координатами должны быть равны"
    checks_passed += 1
    print("PASS: Point(1, 2) == Point(1, 2)")

    assert p1 != p3, "Точки с разными координатами не должны быть равны"
    checks_passed += 1
    print("PASS: Point(1, 2) != Point(3, 4)")

    assert hash(p1) == hash(p2), "Равные объекты обязаны иметь равный hash()"
    checks_passed += 1
    print("PASS: hash(p1) == hash(p2)")

    points_set = {p1, p2, p3}
    assert len(points_set) == 2, f"Ожидалось 2 уникальных точки в множестве, получено {len(points_set)}"
    checks_passed += 1
    print("PASS: множество дедуплицировало Point(1, 2) и Point(1, 2)")

    lookup = {p1: "первая точка"}
    assert lookup[p2] == "первая точка", "Point(1, 2) должен находить значение, положенное под p1"
    checks_passed += 1
    print("PASS: p2 находит значение, сохранённое под равным ему p1, в словаре")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

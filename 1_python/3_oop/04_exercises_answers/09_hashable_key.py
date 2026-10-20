"""Решение: реализуйте __eq__ и __hash__ у класса Point(x, y)."""


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


def main() -> None:
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)

    assert p1 == p2, "Точки с одинаковыми координатами должны быть равны"
    assert p1 != p3, "Точки с разными координатами не должны быть равны"
    assert hash(p1) == hash(p2), "Равные объекты обязаны иметь равный hash()"

    points_set = {p1, p2, p3}
    assert len(points_set) == 2, (
        f"Ожидалось 2 уникальных точки в множестве, получено {len(points_set)}"
    )

    lookup = {p1: "первая точка"}
    assert lookup[p2] == "первая точка", (
        "Point(1, 2) должен находить значение, положенное под p1"
    )

    checks = [
        (p1 == p2, "Point(1, 2) == Point(1, 2)"),
        (p1 != p3, "Point(1, 2) != Point(3, 4)"),
        (hash(p1) == hash(p2), "hash(p1) == hash(p2)"),
        (len(points_set) == 2, "дедупликация Point в множестве"),
        (lookup[p2] == "первая точка", "поиск значения в словаре по равному Point"),
    ]

    checks_passed = 0
    total_checks = len(checks)
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if ok:
            checks_passed += 1
        print(f"[{status}] {description}")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

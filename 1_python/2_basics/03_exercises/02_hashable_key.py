"""
Упражнение: хешируемый класс-значение.

Реализуйте класс Point(x, y), экземпляры которого можно использовать
как ключи словаря и элементы множества: два Point с одинаковыми
координатами должны считаться равными и иметь одинаковый хеш.

Синтаксис class разбирается в 4_oop — здесь каркас класса уже готов,
просто заполни тела двух методов:
- __eq__ вызывается при сравнении p1 == p2 (self — левый Point,
  other — правый);
- __hash__ вызывается функцией hash(p) и должен вернуть целое число.
self.x и self.y — координаты точки.

TODO: реализуйте __eq__ и __hash__.
"""


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        # TODO: два Point равны, если совпадают x и y.
        # Сначала проверь isinstance(other, Point); если нет — верни False.
        raise NotImplementedError("Реализуйте __eq__")

    def __hash__(self) -> int:
        # TODO: хеш должен быть согласован с __eq__ (равные -> равные хеши).
        # Подсказка: кортеж (self.x, self.y) хешируем — возьми hash() от него.
        raise NotImplementedError("Реализуйте __hash__")


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

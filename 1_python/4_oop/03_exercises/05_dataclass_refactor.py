"""Задача: замените verbose-класс ManualPoint его эквивалентом на @dataclass,
включая корректную обработку изменяемого поля tags через field(default_factory=...)."""

from dataclasses import dataclass, field


class ManualPoint:
    """Рукописная версия — для сравнения. Не трогайте этот класс."""

    def __init__(self, x: float, y: float, tags: list[str] | None = None) -> None:
        self.x = x
        self.y = y
        self.tags = tags if tags is not None else []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ManualPoint):
            return NotImplemented
        return (self.x, self.y, self.tags) == (other.x, other.y, other.tags)

    def __repr__(self) -> str:
        return f"ManualPoint(x={self.x!r}, y={self.y!r}, tags={self.tags!r})"


# TODO: превратите Point в dataclass, эквивалентный ManualPoint по поведению
# __init__/__eq__/__repr__. Поле tags — изменяемое (list), задайте его
# правильно через field(default_factory=list), а не через tags: list = [].
class Point:
    x: float
    y: float
    tags: list[str]


def main() -> None:
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p1.tags.append("origin-ish")

    checks = [
        (p1 == Point(1, 2, ["origin-ish"]), "dataclass __eq__ сравнивает по значению"),
        (p2.tags == [], "у p2 свой независимый список tags (default_factory сработал)"),
        (repr(Point(1, 2)) == "Point(x=1, y=2, tags=[])", "автосгенерированный __repr__"),
        (ManualPoint(1, 2) == ManualPoint(1, 2), "сверка: ручная версия ведёт себя так же"),
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

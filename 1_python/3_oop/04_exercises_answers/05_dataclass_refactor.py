"""Решение: Point как @dataclass, эквивалентный ручной версии ManualPoint."""

from dataclasses import dataclass, field


class ManualPoint:
    """Рукописная версия — для сравнения."""

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


@dataclass
class Point:
    x: float
    y: float
    tags: list[str] = field(default_factory=list)


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

    all_ok = True
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"[{status}] {description}")

    print("PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()

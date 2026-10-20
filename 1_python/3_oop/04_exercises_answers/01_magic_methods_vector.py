"""Решение: класс Vector с магическими методами __add__, __eq__, __repr__, __mul__."""


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vector(x={self.x!r}, y={self.y!r})"


def main() -> None:
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    checks = [
        (v1 + v2 == Vector(4, 6), "сложение векторов"),
        (v1 * 2 == Vector(2, 4), "умножение на скаляр"),
        (v1 == Vector(1, 2), "сравнение равных векторов"),
        (v1 != v2, "сравнение разных векторов"),
        (repr(v1) == "Vector(x=1, y=2)", "repr"),
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

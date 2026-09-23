"""Задача: реализуйте класс Vector с магическими методами __add__, __eq__,
__repr__ и __mul__ (умножение на скаляр)."""


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # TODO: реализуйте __add__ — сложение двух векторов покомпонентно,
    # результат должен быть новым объектом Vector.
    def __add__(self, other: "Vector") -> "Vector":
        raise NotImplementedError

    # TODO: реализуйте __mul__ — умножение вектора на число (скаляр),
    # other здесь всегда float/int.
    def __mul__(self, scalar: float) -> "Vector":
        raise NotImplementedError

    # TODO: реализуйте __eq__ — два вектора равны, если равны их x и y.
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    # TODO: реализуйте __repr__ в формате Vector(x=1, y=2).
    def __repr__(self) -> str:
        raise NotImplementedError


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

    all_ok = True
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"[{status}] {description}")

    print("PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()

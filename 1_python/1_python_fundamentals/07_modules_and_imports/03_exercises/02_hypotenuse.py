"""
Упражнение: from x import y.

TODO: реализуйте hypotenuse так, чтобы она возвращала длину гипотенузы
      прямоугольного треугольника по двум катетам a и b
      (корень из a**2 + b**2). Добавьте `from math import sqrt` вверху
      файла и вызывайте sqrt без префикса "math.".
"""


def hypotenuse(a: float, b: float) -> float:
    raise NotImplementedError("from math import sqrt; верните sqrt(a ** 2 + b ** 2)")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = hypotenuse(3, 4)
    assert result == 5.0, f"Ожидалось 5.0, получено {result}"
    checks_passed += 1
    print("PASS: hypotenuse(3, 4) == 5.0")

    result = hypotenuse(5, 12)
    assert result == 13.0, f"Ожидалось 13.0, получено {result}"
    checks_passed += 1
    print("PASS: hypotenuse(5, 12) == 13.0")

    result = round(hypotenuse(1, 1), 4)
    assert result == 1.4142, f"Ожидалось 1.4142, получено {result}"
    checks_passed += 1
    print("PASS: hypotenuse(1, 1) ~ 1.4142")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

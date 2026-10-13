"""Решение: import x."""

import math


def circle_area(radius: float) -> float:
    return math.pi * radius ** 2


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = round(circle_area(1), 5)
    assert result == 3.14159, f"Ожидалось 3.14159, получено {result}"
    checks_passed += 1
    print("PASS: circle_area(1) ~ 3.14159")

    result = round(circle_area(5), 2)
    assert result == 78.54, f"Ожидалось 78.54, получено {result}"
    checks_passed += 1
    print("PASS: circle_area(5) ~ 78.54")

    result = circle_area(0)
    assert result == 0, f"Ожидалось 0, получено {result}"
    checks_passed += 1
    print("PASS: circle_area(0) == 0")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

"""Решение: параметр со значением по умолчанию."""


def apply_discount(price: float, discount_percent: float = 10) -> float:
    return price - price * discount_percent / 100


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = apply_discount(100)
    assert result == 90, f"Ожидалось 90 (скидка по умолчанию 10%), получено {result}"
    checks_passed += 1
    print("PASS: apply_discount(100) == 90 (скидка по умолчанию)")

    result = apply_discount(100, 50)
    assert result == 50, f"Ожидалось 50, получено {result}"
    checks_passed += 1
    print("PASS: apply_discount(100, 50) == 50")

    result = apply_discount(200, discount_percent=0)
    assert result == 200, f"Ожидалось 200 (без скидки), получено {result}"
    checks_passed += 1
    print("PASS: apply_discount(200, discount_percent=0) == 200")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

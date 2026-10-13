"""Решение: ветвления."""


def classify_number(number: int) -> str:
    if number < 0:
        return "отрицательное"
    elif number == 0:
        return "ноль"
    else:
        return "положительное"


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    assert classify_number(-5) == "отрицательное"
    checks_passed += 1
    print("PASS: classify_number(-5) == 'отрицательное'")

    assert classify_number(0) == "ноль"
    checks_passed += 1
    print("PASS: classify_number(0) == 'ноль'")

    assert classify_number(7) == "положительное"
    checks_passed += 1
    print("PASS: classify_number(7) == 'положительное'")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

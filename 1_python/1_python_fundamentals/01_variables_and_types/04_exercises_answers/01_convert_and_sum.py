"""Решение: преобразование типов."""


def sum_as_numbers(first: str, second: str) -> int:
    return int(first) + int(second)


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = sum_as_numbers("2", "3")
    assert result == 5, f"Ожидалось 5, получено {result}"
    checks_passed += 1
    print("PASS: sum_as_numbers('2', '3') == 5")

    result = sum_as_numbers("10", "20")
    assert result == 30, f"Ожидалось 30, получено {result}"
    checks_passed += 1
    print("PASS: sum_as_numbers('10', '20') == 30")

    result = sum_as_numbers("-5", "5")
    assert result == 0, f"Ожидалось 0, получено {result}"
    checks_passed += 1
    print("PASS: sum_as_numbers('-5', '5') == 0")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

"""
Упражнение: ветвления.

TODO: реализуйте classify_number так, чтобы она возвращала:
      - "отрицательное", если число меньше 0
      - "ноль", если число равно 0
      - "положительное", если число больше 0
"""


def classify_number(number: int) -> str:
    raise NotImplementedError("Используйте if/elif/else для трёх случаев")


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

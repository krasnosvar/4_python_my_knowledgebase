"""
Упражнение: логические операторы.

Пользователь допущен к акции, если его возраст от 18 до 65 лет включительно
И при этом он ещё не использовал акцию (used_promo is False).

TODO: реализуйте is_eligible с помощью сравнений и and/or.
"""


def is_eligible(age: int, used_promo: bool) -> bool:
    raise NotImplementedError("Верните True, если 18 <= age <= 65 и не used_promo")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 4

    assert is_eligible(25, False) is True
    checks_passed += 1
    print("PASS: is_eligible(25, False) is True")

    assert is_eligible(17, False) is False
    checks_passed += 1
    print("PASS: is_eligible(17, False) is False (младше 18)")

    assert is_eligible(70, False) is False
    checks_passed += 1
    print("PASS: is_eligible(70, False) is False (старше 65)")

    assert is_eligible(30, True) is False
    checks_passed += 1
    print("PASS: is_eligible(30, True) is False (уже использовал)")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

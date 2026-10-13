"""Решение: выбросить исключение самому через raise."""


def check_age(age: int) -> int:
    if age < 0 or age > 150:
        raise ValueError(f"Некорректный возраст: {age}")
    return age


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = check_age(30)
    assert result == 30, f"Ожидалось 30, получено {result}"
    checks_passed += 1
    print("PASS: check_age(30) == 30")

    raised = False
    try:
        check_age(-1)
    except ValueError:
        raised = True
    assert raised, "Для -1 ожидался ValueError"
    checks_passed += 1
    print("PASS: check_age(-1) выбрасывает ValueError")

    raised = False
    try:
        check_age(200)
    except ValueError:
        raised = True
    assert raised, "Для 200 ожидался ValueError"
    checks_passed += 1
    print("PASS: check_age(200) выбрасывает ValueError")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

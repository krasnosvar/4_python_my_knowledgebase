"""
Упражнение: выбросить исключение самому через raise.

TODO: реализуйте check_age так, чтобы она:
      - выбрасывала ValueError, если age меньше 0 или больше 150;
      - иначе возвращала age без изменений.
"""


def check_age(age: int) -> int:
    raise NotImplementedError("Проверьте границы и используйте raise ValueError(...)")


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

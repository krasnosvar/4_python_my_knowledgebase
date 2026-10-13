"""Решение: f-строки."""


def format_report(name: str, total_tasks: int, done_tasks: int) -> str:
    return f"{name}: {total_tasks} задачи, {done_tasks} выполнено"


def _self_check() -> None:
    checks_passed = 0
    total_checks = 2

    result = format_report("Alex", 3, 2)
    expected = "Alex: 3 задачи, 2 выполнено"
    assert result == expected, f"Ожидалось {expected!r}, получено {result!r}"
    checks_passed += 1
    print(f"PASS: format_report('Alex', 3, 2) == {expected!r}")

    result = format_report("Nina", 5, 5)
    expected = "Nina: 5 задачи, 5 выполнено"
    assert result == expected, f"Ожидалось {expected!r}, получено {result!r}"
    checks_passed += 1
    print(f"PASS: format_report('Nina', 5, 5) == {expected!r}")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

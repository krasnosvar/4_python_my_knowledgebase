"""
Упражнение: вывод с разделителями.

TODO: реализуйте build_greeting так, чтобы она ВОЗВРАЩАЛА строку
      (не печатала через print!) вида "Alex-25-Moscow", соединяя три
      значения через дефис. Подсказка: используйте str() для числа.
"""


def build_greeting(name: str, age: int, city: str) -> str:
    raise NotImplementedError("Соберите строку '<name>-<age>-<city>' через дефис")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 2

    result = build_greeting("Alex", 25, "Moscow")
    assert result == "Alex-25-Moscow", f"Получено {result!r}"
    checks_passed += 1
    print("PASS: build_greeting('Alex', 25, 'Moscow') == 'Alex-25-Moscow'")

    result = build_greeting("Nina", 30, "Kazan")
    assert result == "Nina-30-Kazan", f"Получено {result!r}"
    checks_passed += 1
    print("PASS: build_greeting('Nina', 30, 'Kazan') == 'Nina-30-Kazan'")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

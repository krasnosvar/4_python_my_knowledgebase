"""Решение: вывод с разделителями."""


def build_greeting(name: str, age: int, city: str) -> str:
    return f"{name}-{age}-{city}"


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

"""Решение: изменяемое значение по умолчанию."""


def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    first_call = add_item("a")
    assert first_call == ["a"], f"Ожидалось ['a'], получено {first_call}"
    checks_passed += 1
    print("PASS: первый вызов add_item('a') вернул ['a']")

    second_call = add_item("b")
    assert second_call == ["b"], (
        f"Ожидалось ['b'] (независимый список), получено {second_call}. "
        "Похоже, bucket по-прежнему общий между вызовами."
    )
    checks_passed += 1
    print("PASS: второй вызов add_item('b') вернул ['b'], а не ['a', 'b']")

    shared = []
    add_item("x", shared)
    add_item("y", shared)
    assert shared == ["x", "y"], f"Явно переданный bucket должен накапливать элементы, получено {shared}"
    checks_passed += 1
    print("PASS: явно переданный bucket корректно накапливает элементы")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

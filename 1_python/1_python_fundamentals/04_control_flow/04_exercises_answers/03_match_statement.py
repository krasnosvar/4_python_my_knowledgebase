"""Решение: диспетчеризация команд через match/case."""


def dispatch_command(command):
    match command:
        case ("greet", name):
            return f"Привет, {name}!"
        case ("add", a, b):
            return a + b
        case {"action": "reset"}:
            return "Состояние сброшено"
        case {"action": "set", "key": key, "value": value}:
            return f"{key} = {value}"
        case [first, *rest]:
            return f"Первый: {first}, ещё {len(rest)} элементов"
        case _:
            return "Неизвестная команда"


def _self_check() -> None:
    checks_passed = 0
    total_checks = 6

    assert dispatch_command(("greet", "Мир")) == "Привет, Мир!"
    checks_passed += 1
    print("PASS: команда greet")

    assert dispatch_command(("add", 2, 3)) == 5
    checks_passed += 1
    print("PASS: команда add")

    assert dispatch_command({"action": "reset"}) == "Состояние сброшено"
    checks_passed += 1
    print("PASS: команда reset")

    cmd_set = {"action": "set", "key": "timeout", "value": 30}
    assert dispatch_command(cmd_set) == "timeout = 30"
    checks_passed += 1
    print("PASS: команда set")

    assert dispatch_command([1, 2, 3]) == "Первый: 1, ещё 2 элементов"
    checks_passed += 1
    print("PASS: список с первым элементом и остатком")

    assert dispatch_command(42) == "Неизвестная команда"
    checks_passed += 1
    print("PASS: неизвестная команда (число)")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

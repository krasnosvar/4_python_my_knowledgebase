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
        case [first, *rest] if len(rest) >= 0:
            return f"Первый: {first}, ещё {len(rest)} элементов"
        case _:
            return "Неизвестная команда"


def _self_check() -> None:
    assert dispatch_command(("greet", "Мир")) == "Привет, Мир!"
    print("PASS: команда greet")

    assert dispatch_command(("add", 2, 3)) == 5
    print("PASS: команда add")

    assert dispatch_command({"action": "reset"}) == "Состояние сброшено"
    print("PASS: команда reset")

    assert dispatch_command({"action": "set", "key": "timeout", "value": 30}) == "timeout = 30"
    print("PASS: команда set")

    assert dispatch_command([1, 2, 3]) == "Первый: 1, ещё 2 элементов"
    print("PASS: список с первым элементом и остатком")

    assert dispatch_command(42) == "Неизвестная команда"
    print("PASS: неизвестная команда (число)")

    print("\nВсе проверки пройдены")


if __name__ == "__main__":
    _self_check()

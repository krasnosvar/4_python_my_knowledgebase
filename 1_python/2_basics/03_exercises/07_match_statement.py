"""
Упражнение: диспетчеризация команд через match/case.

TODO: реализуйте dispatch_command(command), используя match/case:
  - ("greet", name)                          -> f"Привет, {name}!"
  - ("add", a, b)                            -> сумма a + b (число)
  - {"action": "reset"}                      -> "Состояние сброшено"
  - {"action": "set", "key": k, "value": v}   -> f"{k} = {v}"
  - list с хотя бы одним элементом [first, *rest] -> f"Первый: {first}, ещё {len(rest)} элементов"
  - всё остальное                            -> "Неизвестная команда"
"""


def dispatch_command(command):
    raise NotImplementedError("Реализуйте match/case согласно описанию выше")


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

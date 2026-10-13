"""
Упражнение: определить имя типа значения.

TODO: реализуйте describe_type так, чтобы она возвращала имя типа значения
      в виде строки: "int", "float", "str", "bool" или "NoneType".
      Подсказка: у функции type() есть атрибут __name__.
"""


def describe_type(value) -> str:
    raise NotImplementedError("Верните type(value).__name__")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 5

    cases = [
        (42, "int"),
        (3.14, "float"),
        ("hello", "str"),
        (True, "bool"),
        (None, "NoneType"),
    ]
    for value, expected in cases:
        result = describe_type(value)
        assert result == expected, (
            f"Для {value!r} ожидалось {expected!r}, получено {result!r}"
        )
        checks_passed += 1
        print(f"PASS: describe_type({value!r}) == {expected!r}")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

"""
Упражнение: неизменяемость кортежа против изменяемости списка, is vs ==.

TODO: реализуйте три функции ниже так, чтобы они действительно проверяли
      описанное поведение (а не просто возвращали True).

Подсказки:
- try/except — см. 1_python_fundamentals/06_exceptions;
- id(x) — уникальный номер объекта, см. 2_basics/01_theory/03_mutability_and_identity.md.
"""


def try_mutate_tuple(t: tuple) -> bool:
    """Должна вернуть True, если попытка t[0] = ... вызывает TypeError, иначе False."""
    raise NotImplementedError("Оберните t[0] = ... в try/except TypeError")


def append_returns_same_object(lst: list, item) -> bool:
    """Должна вернуть True, если lst.append(item) не создаёт новый объект (id не меняется)."""
    raise NotImplementedError("Сравните id(lst) до и после lst.append(item)")


def concat_creates_new_string(s: str, suffix: str) -> bool:
    """Должна вернуть True, если s + suffix — НОВЫЙ объект (id отличается от id(s))."""
    raise NotImplementedError("Сравните id(s) и id(s + suffix)")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    assert try_mutate_tuple((1, 2, 3)) is True, "Попытка изменить элемент кортежа должна вызывать TypeError"
    checks_passed += 1
    print("PASS: кортеж действительно неизменяем (TypeError при попытке мутации)")

    assert append_returns_same_object([1, 2], 3) is True, "append должен изменять список на месте, id не должен меняться"
    checks_passed += 1
    print("PASS: list.append не создаёт новый объект (мутация на месте)")

    assert concat_creates_new_string("hello", " world") is True, "Конкатенация строк должна создавать новый объект"
    checks_passed += 1
    print("PASS: конкатенация строк создаёт новый объект (строки неизменяемы)")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

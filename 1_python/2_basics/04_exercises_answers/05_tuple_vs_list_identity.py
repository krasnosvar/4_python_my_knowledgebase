"""Решение: неизменяемость кортежа против изменяемости списка, is vs ==."""


def try_mutate_tuple(t: tuple) -> bool:
    try:
        t[0] = "mutated"
    except TypeError:
        return True
    return False


def append_returns_same_object(lst: list, item) -> bool:
    original_id = id(lst)
    lst.append(item)
    return id(lst) == original_id


def concat_creates_new_string(s: str, suffix: str) -> bool:
    original_id = id(s)
    new_s = s + suffix
    return id(new_s) != original_id


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    assert try_mutate_tuple((1, 2, 3)) is True, "Попытка изменить элемент кортежа должна вызывать TypeError"
    checks_passed += 1
    print("PASS: кортеж действительно неизменяем (TypeError при попытке мутации)")

    assert append_returns_same_object([1, 2], 3) is True, "append должен изменять список на месте"
    checks_passed += 1
    print("PASS: list.append не создаёт новый объект (мутация на месте)")

    assert concat_creates_new_string("hello", " world") is True, "Конкатенация строк должна создавать новый объект"
    checks_passed += 1
    print("PASS: конкатенация строк создаёт новый объект (строки неизменяемы)")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

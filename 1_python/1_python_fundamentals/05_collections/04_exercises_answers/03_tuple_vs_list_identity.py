"""Решение: изменяемость списка против неизменяемости кортежа и строки."""


def add_creates_new_tuple(t: tuple, item) -> bool:
    original_id = id(t)
    new_tuple = t + (item,)
    return id(new_tuple) != original_id


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

    assert add_creates_new_tuple((1, 2), 3) is True, (
        "Сложение кортежей должно создавать новый объект"
    )
    checks_passed += 1
    print("PASS: t + (item,) создаёт новый кортеж (кортежи неизменяемы)")

    sample_list = [1, 2]
    assert append_returns_same_object(sample_list, 3) is True, (
        "append должен менять список на месте, не меняя его id"
    )
    assert sample_list == [1, 2, 3], (
        "Функция должна действительно вызывать lst.append(item)"
    )
    checks_passed += 1
    print("PASS: list.append изменяет тот же список на месте")

    assert concat_creates_new_string("hello", " world") is True, (
        "Конкатенация строк должна создавать новый объект"
    )
    checks_passed += 1
    print("PASS: конкатенация строк создаёт новый объект")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

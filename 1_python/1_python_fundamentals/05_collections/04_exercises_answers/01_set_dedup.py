"""Решение: дедупликация списка с сохранением порядка."""


def dedup_preserve_order(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _self_check() -> None:
    checks_passed = 0
    total_checks = 4

    result = dedup_preserve_order([3, 1, 3, 2, 1, 4])
    assert result == [3, 1, 2, 4], (
        f"Ожидалось [3, 1, 2, 4], получено {result}"
    )
    checks_passed += 1
    print("PASS: базовая дедупликация с сохранением порядка")

    result_empty = dedup_preserve_order([])
    assert result_empty == [], "Пустой вход должен давать пустой выход"
    checks_passed += 1
    print("PASS: пустой список на входе")

    result_no_dups = dedup_preserve_order([1, 2, 3])
    assert result_no_dups == [1, 2, 3], (
        "Список без повторов должен вернуться без изменений"
    )
    checks_passed += 1
    print("PASS: список без повторов остаётся неизменным")

    words = dedup_preserve_order(["a", "b", "a", "c", "b"])
    assert words == ["a", "b", "c"], (
        f"Ожидалось ['a', 'b', 'c'], получено {words}"
    )
    checks_passed += 1
    print("PASS: строковые элементы дедуплицированы по порядку")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

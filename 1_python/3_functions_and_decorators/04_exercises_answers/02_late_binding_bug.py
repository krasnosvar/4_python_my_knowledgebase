"""Решение: исправление позднего связывания через аргумент по умолчанию."""


def make_multipliers_buggy():
    funcs = []
    for factor in range(1, 4):
        funcs.append(lambda x: x * factor)
    return funcs


def make_multipliers_fixed():
    funcs = []
    for factor in range(1, 4):
        funcs.append(lambda x, factor=factor: x * factor)
    return funcs


if __name__ == "__main__":
    checks_passed = 0
    total_checks = 2

    buggy = make_multipliers_buggy()
    buggy_results = [f(10) for f in buggy]
    assert buggy_results == [30, 30, 30], f"ожидали баг с [30, 30, 30], получили {buggy_results}"
    checks_passed += 1

    fixed = make_multipliers_fixed()
    fixed_results = [f(10) for f in fixed]
    assert fixed_results == [10, 20, 30], f"FAIL: получено {fixed_results}"
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")

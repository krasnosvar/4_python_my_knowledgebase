"""Упражнение: исправьте ошибку позднего связывания переменной цикла."""


def make_multipliers_buggy():
    """Баг: все возвращённые функции используют одно и то же последнее значение `factor`."""
    funcs = []
    for factor in range(1, 4):
        funcs.append(lambda x: x * factor)
    return funcs


def make_multipliers_fixed():
    # TODO: реализуйте функцию так, чтобы вернуть список из 3 функций-умножителей
    # (на 1, на 2 и на 3), каждая из которых сохраняет СВОЁ значение factor,
    # а не общую переменную цикла.
    # Подсказка: используйте аргумент по умолчанию или фабрику-замыкание
    # (см. 01_theory/03_first_class_functions_and_closures.md).
    raise NotImplementedError


if __name__ == "__main__":
    buggy = make_multipliers_buggy()
    buggy_results = [f(10) for f in buggy]
    # Демонстрация бага: все функции используют последнее значение factor (3).
    assert buggy_results == [30, 30, 30], f"ожидали баг с [30, 30, 30], получили {buggy_results}"

    fixed = make_multipliers_fixed()
    fixed_results = [f(10) for f in fixed]
    assert fixed_results == [10, 20, 30], f"FAIL: получено {fixed_results}"

    print("PASS")

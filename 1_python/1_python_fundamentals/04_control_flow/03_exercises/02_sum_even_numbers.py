"""
Упражнение: цикл for и continue.

TODO: реализуйте sum_even_numbers так, чтобы она возвращала сумму только
      чётных чисел из списка numbers. Подсказка: число чётное, если
      number % 2 == 0.
"""


def sum_even_numbers(numbers: list) -> int:
    raise NotImplementedError("Пройдитесь циклом for, пропуская нечётные через continue")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = sum_even_numbers([1, 2, 3, 4, 5, 6])
    assert result == 12, f"Ожидалось 12 (2+4+6), получено {result}"
    checks_passed += 1
    print("PASS: sum_even_numbers([1,2,3,4,5,6]) == 12")

    result = sum_even_numbers([1, 3, 5])
    assert result == 0, f"Ожидалось 0 (нет чётных), получено {result}"
    checks_passed += 1
    print("PASS: sum_even_numbers([1,3,5]) == 0")

    result = sum_even_numbers([])
    assert result == 0, f"Ожидалось 0 (пустой список), получено {result}"
    checks_passed += 1
    print("PASS: sum_even_numbers([]) == 0")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

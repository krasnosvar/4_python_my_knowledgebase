"""
Задача (средний уровень): дан отсортированный массив без дубликатов,
"повёрнутый" в неизвестной точке (например [4,5,6,7,0,1,2]). Найти
индекс target за O(log n) — обычный бинарный поиск не работает напрямую,
нужно на каждом шаге определять, какая половина отсортирована.

Запусти: python main.py
"""
from __future__ import annotations


def search_rotated(nums: list[int], target: int) -> int:
    """
    TODO: бинарный поиск с дополнительной проверкой. На каждом шаге:
      1. Если nums[mid] == target — вернуть mid.
      2. Определить, какая половина [left..mid] или [mid..right]
         отсортирована (сравнить nums[left] и nums[mid]).
      3. Проверить, попадает ли target в диапазон отсортированной
         половины — если да, искать там (сузить границы), иначе — в
         другой половине.
    Вернуть -1, если target не найден.
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 6
    nums = [4, 5, 6, 7, 0, 1, 2]

    assert search_rotated(nums, 0) == 4
    checks_passed += 1
    assert search_rotated(nums, 4) == 0
    checks_passed += 1
    assert search_rotated(nums, 2) == 6
    checks_passed += 1
    assert search_rotated(nums, 3) == -1
    checks_passed += 1

    assert search_rotated([1], 1) == 0
    checks_passed += 1
    assert search_rotated([1], 0) == -1
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

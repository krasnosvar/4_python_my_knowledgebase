"""
Бинарный поиск вручную, bisect из stdlib, бинарный поиск по предикату
(поиск первой позиции, где предикат становится истинным).

Запуск: python main.py
"""
from __future__ import annotations

import bisect


def binary_search(items: list[int], target: int) -> int:
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def find_first_true(predicate, low: int, high: int) -> int:
    """predicate монотонен: False...False True...True на [low, high]."""
    while low < high:
        mid = (low + high) // 2
        if predicate(mid):
            high = mid
        else:
            low = mid + 1
    return low


def main() -> None:
    items = [1, 3, 5, 7, 9, 11, 13]

    print("--- бинарный поиск вручную ---")
    print(binary_search(items, 7))   # 3
    print(binary_search(items, 4))   # -1

    print("\n--- bisect из стандартной библиотеки ---")
    index = bisect.bisect_left(items, 7)
    print(f"bisect_left(7) = {index}, items[{index}] = {items[index]}")

    bisect.insort(items, 6)
    print(f"после insort(6): {items}")

    print("\n--- бинарный поиск по предикату ---")
    # первая позиция x, где x*x >= 50
    result = find_first_true(lambda x: x * x >= 50, 0, 100)
    print(f"первое x, где x^2 >= 50: {result} (x^2={result * result})")
    assert result * result >= 50 and (result - 1) ** 2 < 50


if __name__ == "__main__":
    main()

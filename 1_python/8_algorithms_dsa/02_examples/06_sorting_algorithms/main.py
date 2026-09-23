"""
Quicksort и merge sort вручную (учебная реализация), сравнение со
встроенным sorted() (Timsort).

Запуск: python main.py
"""
from __future__ import annotations

import random
import time


def quicksort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]
    return quicksort(less) + equal + quicksort(greater)


def merge_sort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def main() -> None:
    random.seed(42)
    data = [random.randint(0, 10_000) for _ in range(2000)]

    expected = sorted(data)
    assert quicksort(data) == expected
    assert merge_sort(data) == expected
    print("quicksort и merge_sort дают тот же результат, что sorted()")

    start = time.perf_counter()
    sorted(data)
    builtin_time = time.perf_counter() - start

    start = time.perf_counter()
    merge_sort(data)
    merge_time = time.perf_counter() - start

    print(f"\nsorted() (Timsort, встроенная, на C): {builtin_time:.5f}s")
    print(f"merge_sort (чистый Python):            {merge_time:.5f}s")
    print("встроенная сортировка быстрее — используйте её в реальном коде")


if __name__ == "__main__":
    main()

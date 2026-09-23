"""Решение: 09_top_k_frequent"""
from __future__ import annotations

import heapq
from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)


def main() -> None:
    result = top_k_frequent([1, 1, 1, 2, 2, 3], k=2)
    assert set(result) == {1, 2}, f"ожидали {{1, 2}}, получили {set(result)}"

    result2 = top_k_frequent([1], k=1)
    assert result2 == [1]

    result3 = top_k_frequent([4, 4, 4, 6, 6, 5, 5, 5, 5], k=1)
    assert result3 == [5]

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

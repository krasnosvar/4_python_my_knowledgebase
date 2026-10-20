"""
Задача (средний уровень): найти k самых часто встречающихся элементов в
списке за O(n log k), используя collections.Counter + heapq.nlargest
(не полную сортировку O(n log n) всех уникальных элементов).

Запусти: python main.py
"""
from __future__ import annotations


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    TODO:
      1. Построить collections.Counter(nums) — частоты элементов.
      2. Вернуть k элементов с наибольшей частотой через
         heapq.nlargest(k, counts, key=counts.get).
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 3
    result = top_k_frequent([1, 1, 1, 2, 2, 3], k=2)
    assert set(result) == {1, 2}, f"ожидали {{1, 2}}, получили {set(result)}"
    checks_passed += 1

    result2 = top_k_frequent([1], k=1)
    assert result2 == [1]
    checks_passed += 1

    result3 = top_k_frequent([4, 4, 4, 6, 6, 5, 5, 5, 5], k=1)
    assert result3 == [5]
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

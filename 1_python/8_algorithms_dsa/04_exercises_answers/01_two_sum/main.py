"""Решение: 01_two_sum"""
from __future__ import annotations


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return seen[complement], i
        seen[x] = i
    raise ValueError("no two sum solution")


def main() -> None:
    checks_passed = 0
    total_checks = 2
    result = two_sum([2, 7, 11, 15], target=9)
    assert result == (0, 1), f"ожидали (0, 1), получили {result}"
    checks_passed += 1

    result2 = two_sum([3, 2, 4], target=6)
    assert result2 == (1, 2), f"ожидали (1, 2), получили {result2}"
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

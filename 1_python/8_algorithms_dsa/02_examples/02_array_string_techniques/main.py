"""
Два указателя, скользящее окно, префиксные суммы.

Запуск: python main.py
"""
from __future__ import annotations


def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def longest_unique_substring(s: str) -> int:
    seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        best = max(best, right - left + 1)
    return best


def build_prefix_sums(nums: list[int]) -> list[int]:
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    return prefix[right] - prefix[left]


def main() -> None:
    print("--- два указателя: палиндром ---")
    print(is_palindrome("racecar"), is_palindrome("hello"))

    print("\n--- скользящее окно: самая длинная подстрока без повторов ---")
    print(longest_unique_substring("abcabcbb"))  # 3 ("abc")

    print("\n--- префиксные суммы ---")
    nums = [1, 2, 3, 4, 5]
    prefix = build_prefix_sums(nums)
    print(f"nums={nums}, prefix={prefix}")
    print(f"sum(nums[1:4]) = {range_sum(prefix, 1, 4)}")  # 2+3+4=9
    assert range_sum(prefix, 1, 4) == sum(nums[1:4])


if __name__ == "__main__":
    main()

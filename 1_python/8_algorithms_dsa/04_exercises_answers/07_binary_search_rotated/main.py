"""Решение: 07_binary_search_rotated"""
from __future__ import annotations


def search_rotated(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:  # левая половина отсортирована
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # правая половина отсортирована
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


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

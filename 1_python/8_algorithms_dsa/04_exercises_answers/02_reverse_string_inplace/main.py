"""Решение: 02_reverse_string_inplace"""
from __future__ import annotations


def reverse_in_place(chars: list[str]) -> None:
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1


def main() -> None:
    checks_passed = 0
    total_checks = 3
    chars = list("hello")
    reverse_in_place(chars)
    assert chars == list("olleh"), f"ожидали ['o','l','l','e','h'], получили {chars}"
    checks_passed += 1

    chars2 = list("a")
    reverse_in_place(chars2)
    assert chars2 == ["a"]
    checks_passed += 1

    chars3 = list("ab")
    reverse_in_place(chars3)
    assert chars3 == ["b", "a"]
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

"""Решение: 03_valid_parentheses"""
from __future__ import annotations


def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack


def main() -> None:
    checks_passed = 0
    total_checks = 1
    cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("", True),
        ("(((", False),
    ]
    for s, expected in cases:
        result = is_balanced(s)
        assert result == expected, f"is_balanced({s!r}) = {result}, ожидали {expected}"
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

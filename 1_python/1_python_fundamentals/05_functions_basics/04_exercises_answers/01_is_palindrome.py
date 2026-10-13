"""Решение: функция с одним параметром."""


def is_palindrome(text: str) -> bool:
    reversed_text = ""
    for char in text:
        reversed_text = char + reversed_text
    return text == reversed_text


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    assert is_palindrome("топот") is True
    checks_passed += 1
    print("PASS: is_palindrome('топот') is True")

    assert is_palindrome("привет") is False
    checks_passed += 1
    print("PASS: is_palindrome('привет') is False")

    assert is_palindrome("а") is True
    checks_passed += 1
    print("PASS: is_palindrome('а') is True (одна буква - всегда палиндром)")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

"""
Упражнение: функция с одним параметром.

TODO: реализуйте is_palindrome так, чтобы она возвращала True, если строка
      читается одинаково в обе стороны, и False иначе.
      Подсказка: пройдите по text циклом for и соберите перевёрнутую строку,
      приклеивая каждый символ СЛЕВА к уже собранной части (reversed_text =
      char + reversed_text). Затем сравните text с получившейся строкой.
"""


def is_palindrome(text: str) -> bool:
    raise NotImplementedError("Соберите перевёрнутую строку циклом for и сравните с text")


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

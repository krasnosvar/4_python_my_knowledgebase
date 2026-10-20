"""Решение: перехват ValueError."""


def safe_int(text: str, default: int = 0) -> int:
    try:
        return int(text)
    except ValueError:
        return default


def _self_check() -> None:
    checks_passed = 0
    total_checks = 3

    result = safe_int("42")
    assert result == 42, f"Ожидалось 42, получено {result}"
    checks_passed += 1
    print("PASS: safe_int('42') == 42")

    result = safe_int("abc")
    assert result == 0, f"Ожидалось 0 (значение по умолчанию), получено {result}"
    checks_passed += 1
    print("PASS: safe_int('abc') == 0")

    result = safe_int("", default=-1)
    assert result == -1, f"Ожидалось -1, получено {result}"
    checks_passed += 1
    print("PASS: safe_int('', default=-1) == -1")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

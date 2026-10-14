"""Решение: декоратор @timed с сохранением метаданных и записью времени выполнения."""

import time
from functools import wraps


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_duration = time.perf_counter() - start
        return result

    wrapper.last_duration = 0.0
    return wrapper


@timed
def slow_add(a: int, b: int) -> int:
    """Складывает два числа с искусственной задержкой."""
    time.sleep(0.01)
    return a + b


if __name__ == "__main__":
    checks_passed = 0
    total_checks = 5

    result = slow_add(2, 3)
    assert result == 5, f"FAIL: результат {result}"
    checks_passed += 1

    assert slow_add.__name__ == "slow_add", "FAIL: __name__ не сохранён"
    checks_passed += 1
    assert slow_add.__doc__ == "Складывает два числа с искусственной задержкой.", (
        "FAIL: __doc__ не сохранён"
    )
    checks_passed += 1

    assert hasattr(slow_add, "last_duration"), "FAIL: нет атрибута last_duration"
    checks_passed += 1
    assert slow_add.last_duration >= 0.01, "FAIL: время выполнения не зафиксировано корректно"
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")

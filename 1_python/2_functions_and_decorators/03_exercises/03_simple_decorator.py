"""Упражнение: декоратор @timed, измеряющий время выполнения и сохраняющий метаданные."""

import time
from functools import wraps


def timed(func):
    # TODO: реализуйте декоратор, который:
    #   1) сохраняет __name__/__doc__ оборачиваемой функции (functools.wraps);
    #   2) измеряет время выполнения func и сохраняет его в атрибуте wrapper.last_duration
    #      (число секунд, float);
    #   3) возвращает результат func без изменений.
    raise NotImplementedError


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

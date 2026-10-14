"""Решение: декоратор-фабрика @retry(times)."""

from functools import wraps


def retry(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001 - обобщённый retry
                    last_exc = exc
            raise last_exc

        return wrapper

    return decorator


_attempts_needed = {"value": 3}
_calls_made = {"count": 0}


@retry(times=5)
def eventually_succeeds() -> str:
    _calls_made["count"] += 1
    if _calls_made["count"] < _attempts_needed["value"]:
        raise ValueError("ещё не готово")
    return "готово"


@retry(times=2)
def always_fails() -> None:
    raise RuntimeError("никогда не работает")


if __name__ == "__main__":
    checks_passed = 0
    total_checks = 2

    assert eventually_succeeds() == "готово"
    checks_passed += 1
    assert _calls_made["count"] == 3, f"FAIL: сделано попыток {_calls_made['count']}"
    checks_passed += 1

    try:
        always_fails()
        raise AssertionError("FAIL: ожидалось исключение после исчерпания попыток")
    except RuntimeError:
        pass

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")

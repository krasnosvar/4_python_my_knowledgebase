"""Решение: контекст-менеджер через @contextlib.contextmanager."""

from contextlib import contextmanager

events: list[str] = []


@contextmanager
def managed_resource(name: str):
    events.append(f"open:{name}")
    try:
        yield name
    finally:
        events.append(f"close:{name}")


if __name__ == "__main__":
    checks_passed = 0
    total_checks = 3

    events.clear()
    with managed_resource("db") as name:
        assert name == "db"
        checks_passed += 1
    assert events == ["open:db", "close:db"], f"FAIL: {events}"
    checks_passed += 1

    events.clear()
    try:
        with managed_resource("cache"):
            raise ValueError("бум")
    except ValueError:
        pass
    else:
        raise AssertionError("FAIL: исключение должно было пробрасываться наружу")

    assert events == ["open:cache", "close:cache"], f"FAIL: очистка не произошла: {events}"
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")

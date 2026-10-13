"""Решение: контекст-менеджер на классе с гарантированной очисткой."""


events: list[str] = []


class ManagedResource:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        events.append(f"open:{self.name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        events.append(f"close:{self.name}")
        return False


if __name__ == "__main__":
    events.clear()
    with ManagedResource("db") as res:
        assert res.name == "db"
    assert events == ["open:db", "close:db"], f"FAIL: {events}"

    events.clear()
    try:
        with ManagedResource("cache") as res:
            raise ValueError("бум")
    except ValueError:
        pass
    else:
        raise AssertionError("FAIL: исключение должно было пробрасываться наружу")

    assert events == ["open:cache", "close:cache"], f"FAIL: очистка не произошла: {events}"

    print("PASS")

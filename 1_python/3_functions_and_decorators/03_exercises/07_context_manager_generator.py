"""Упражнение: тот же контекст-менеджер, но через @contextlib.contextmanager.

Требует генераторов (`yield`) — их разбирает раздел 5_iterators_generators.
Если он ещё не пройден, отложите это упражнение и вернитесь после него.
"""

from contextlib import contextmanager

events: list[str] = []


@contextmanager
def managed_resource(name: str):
    # TODO: реализуйте генераторную версию контекст-менеджера:
    #   - до yield: добавить f"open:{name}" в events;
    #   - yield должен отдавать наружу сам `name` (для использования через `as`);
    #   - после yield (в finally): добавить f"close:{name}" в events,
    #     очистка должна происходить даже при исключении в теле `with`.
    raise NotImplementedError


if __name__ == "__main__":
    events.clear()
    with managed_resource("db") as name:
        assert name == "db"
    assert events == ["open:db", "close:db"], f"FAIL: {events}"

    events.clear()
    try:
        with managed_resource("cache"):
            raise ValueError("бум")
    except ValueError:
        pass
    else:
        raise AssertionError("FAIL: исключение должно было пробрасываться наружу")

    assert events == ["open:cache", "close:cache"], f"FAIL: очистка не произошла: {events}"

    print("PASS")

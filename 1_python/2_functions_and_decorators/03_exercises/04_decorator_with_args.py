"""Упражнение: декоратор-фабрика @retry(times), повторяющий вызов при исключении."""


def retry(times: int):
    # TODO: реализуйте фабрику декораторов.
    # Обёрнутая функция должна вызываться повторно до `times` раз, пока не завершится
    # без исключения. Если все `times` попыток провалились - должно пробрасываться
    # последнее пойманное исключение.
    raise NotImplementedError


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
    assert eventually_succeeds() == "готово"
    assert _calls_made["count"] == 3, f"FAIL: сделано попыток {_calls_made['count']}"

    try:
        always_fails()
        raise AssertionError("FAIL: ожидалось исключение после исчерпания попыток")
    except RuntimeError:
        pass

    print("PASS")

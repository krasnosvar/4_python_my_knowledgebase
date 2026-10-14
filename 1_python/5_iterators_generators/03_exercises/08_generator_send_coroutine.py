"""
Задача: реализовать генератор-корутину running_average, накапливающую
среднее значение по мере того, как в неё присылают числа через send().
Не забудьте про шаг прайминга.
"""

from __future__ import annotations

from collections.abc import Generator


def running_average() -> Generator[float, float, None]:
    """Генератор-аккумулятор: каждый send(value) должен возвращать
    (через yield) текущее среднее всех присланных до сих пор значений.

    До первого send() (после прайминга) должен вернуть 0.0, если ничего
    ещё не присылали.
    """
    # TODO: реализуйте с помощью while True: value = yield average,
    # накапливая total и count.
    raise NotImplementedError
    yield  # pragma: no cover


def prime(gen: Generator[float, float, None]) -> float:
    """Прайминг генератора: доводит его до первого yield."""
    return next(gen)


def main() -> None:
    checks_passed = 0
    total_checks = 5

    avg = running_average()

    first = prime(avg)
    assert first == 0.0, f"first: {first}"
    checks_passed += 1

    result = avg.send(10)
    assert result == 10.0, f"result: {result}"
    checks_passed += 1

    result = avg.send(20)
    assert result == 15.0, f"result: {result}"
    checks_passed += 1

    result = avg.send(30)
    assert result == 20.0, f"result: {result}"
    checks_passed += 1

    # свежий генератор, независимое состояние
    avg2 = running_average()
    prime(avg2)
    assert avg2.send(100) == 100.0
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

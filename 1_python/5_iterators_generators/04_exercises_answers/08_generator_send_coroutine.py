"""Решение: генератор-корутина running_average."""

from __future__ import annotations

from collections.abc import Generator


def running_average() -> Generator[float, float, None]:
    total = 0.0
    count = 0
    average = 0.0
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count


def prime(gen: Generator[float, float, None]) -> float:
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

    avg2 = running_average()
    prime(avg2)
    assert avg2.send(100) == 100.0
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

"""Решение: статистика через генераторные выражения."""

from __future__ import annotations

READINGS = [12.5, -3.0, 45.2, 0.0, 18.9, -7.1, 100.0, 33.3, -1.5, 22.0]


def sum_positive(readings: list[float]) -> float:
    return sum(r for r in readings if r > 0)


def count_above(readings: list[float], threshold: float) -> int:
    return sum(r > threshold for r in readings)


def max_negative(readings: list[float]) -> float | None:
    return max((r for r in readings if r < 0), default=None)


def mean(readings: list[float]) -> float:
    return sum(readings) / len(readings)


def main() -> None:
    assert abs(sum_positive(READINGS) - 231.9) < 1e-9

    assert count_above(READINGS, 20) == 4

    assert max_negative(READINGS) == -1.5

    assert max_negative([1.0, 2.0]) is None

    expected_mean = sum(READINGS) / len(READINGS)
    assert abs(mean(READINGS) - expected_mean) < 1e-9

    print("PASS")


if __name__ == "__main__":
    main()

"""
Задача: посчитать простую статистику по данным, используя генераторные
выражения, переданные напрямую во встроенные функции - без промежуточных
списков.
"""

from __future__ import annotations

READINGS = [12.5, -3.0, 45.2, 0.0, 18.9, -7.1, 100.0, 33.3, -1.5, 22.0]


def sum_positive(readings: list[float]) -> float:
    """Сумма только положительных значений. Реализовать одним генераторным
    выражением, переданным в sum(), без промежуточного списка/фильтра."""
    # TODO
    raise NotImplementedError


def count_above(readings: list[float], threshold: float) -> int:
    """Количество значений строго больше threshold. Использовать sum()
    от генераторного выражения с bool-условием (True/False суммируются
    как 1/0)."""
    # TODO
    raise NotImplementedError


def max_negative(readings: list[float]) -> float | None:
    """Максимальное среди отрицательных значений (ближайшее к нулю),
    либо None, если отрицательных нет. Использовать max() с default=."""
    # TODO
    raise NotImplementedError


def mean(readings: list[float]) -> float:
    """Среднее арифметическое всех значений."""
    # TODO
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 5

    assert abs(sum_positive(READINGS) - 231.9) < 1e-9
    checks_passed += 1

    assert count_above(READINGS, 20) == 4
    checks_passed += 1

    assert max_negative(READINGS) == -1.5
    checks_passed += 1

    assert max_negative([1.0, 2.0]) is None
    checks_passed += 1

    expected_mean = sum(READINGS) / len(READINGS)
    assert abs(mean(READINGS) - expected_mean) < 1e-9
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

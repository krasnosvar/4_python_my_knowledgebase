"""
Задача: используя cProfile, определить, какая из двух функций внутри
do_work() расходует больше суммарного времени (tottime), и вернуть её имя.

Запусти: python main.py
"""
from __future__ import annotations

import cProfile
import pstats


def fast_part() -> int:
    return sum(range(10_000))


def slow_part() -> int:
    total = 0
    for i in range(500_000):
        total += i
    return total


def do_work() -> None:
    fast_part()
    slow_part()


def find_slowest_function() -> str:
    """
    TODO:
      1. Создать profiler = cProfile.Profile(), profiler.enable(),
         вызвать do_work(), profiler.disable().
      2. Построить pstats.Stats(profiler), отсортировать по "tottime".
      3. Найти функцию с наибольшим tottime среди fast_part/slow_part —
         stats.stats — это словарь {(filename, lineno, func_name): (cc, nc, tt, ct, callers)}.
         Отфильтровать записи, где func_name in {"fast_part", "slow_part"},
         сравнить их tt (индекс 2 в кортеже).
      4. Вернуть имя функции с наибольшим tt.
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 1
    slowest = find_slowest_function()
    assert slowest == "slow_part", f"ожидали 'slow_part', получили {slowest!r}"
    checks_passed += 1
    print(f"Самая медленная функция по tottime: {slowest}")
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

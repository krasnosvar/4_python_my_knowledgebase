"""Решение: 04_profile_slow_function"""
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
    profiler = cProfile.Profile()
    profiler.enable()
    do_work()
    profiler.disable()

    stats = pstats.Stats(profiler)

    candidates = {"fast_part", "slow_part"}
    best_name = None
    best_tottime = -1.0

    for (filename, lineno, func_name), (cc, nc, tt, ct, callers) in stats.stats.items():
        if func_name in candidates and tt > best_tottime:
            best_tottime = tt
            best_name = func_name

    return best_name


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

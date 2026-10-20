"""Решение: 02_memoized_fibonacci"""
from __future__ import annotations

import time
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def cache_stats() -> str:
    return str(fib.cache_info())


def main() -> None:
    checks_passed = 0
    total_checks = 2
    start = time.perf_counter()
    result = fib(35)
    elapsed = time.perf_counter() - start

    assert result == 9227465, f"fib(35) должен быть 9227465, получили {result}"
    checks_passed += 1
    assert elapsed < 0.5, "с lru_cache fib(35) должен считаться быстро"
    checks_passed += 1

    print(f"fib(35) = {result} за {elapsed:.5f}s")
    print(cache_stats())
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

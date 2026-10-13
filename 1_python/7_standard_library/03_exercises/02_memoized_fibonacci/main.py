"""
Задача: реализовать функцию fib(n) с мемоизацией через functools.lru_cache
так, чтобы fib(35) считался практически мгновенно, и функцию, которая
показывает статистику кэша (cache_info).

Запусти: python main.py
"""
from __future__ import annotations

import time


def fib(n: int) -> int:
    """
    TODO: добавить декоратор @lru_cache (импортировать из functools) над
    этой функцией и реализовать рекурсивную формулу Фибоначчи:
    fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2).
    """
    raise NotImplementedError


def cache_stats() -> str:
    """
    TODO: вернуть строковое представление fib.cache_info().
    Если fib не задекорирована lru_cache — атрибута cache_info не будет,
    это тоже проверка того, что декоратор применён.
    """
    raise NotImplementedError


def main() -> None:
    start = time.perf_counter()
    result = fib(35)
    elapsed = time.perf_counter() - start

    assert result == 9227465, f"fib(35) должен быть 9227465, получили {result}"
    assert elapsed < 0.5, "с lru_cache fib(35) должен считаться быстро"

    print(f"fib(35) = {result} за {elapsed:.5f}s")
    print(cache_stats())


if __name__ == "__main__":
    main()

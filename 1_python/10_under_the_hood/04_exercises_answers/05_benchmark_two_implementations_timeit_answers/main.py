"""Решение: 05_benchmark_two_implementations_timeit"""
from __future__ import annotations

import timeit


DATA_LIST = list(range(10_000))
DATA_SET = set(DATA_LIST)


def check_in_list() -> bool:
    return 9999 in DATA_LIST


def check_in_set() -> bool:
    return 9999 in DATA_SET


def benchmark_speedup(number: int = 1000) -> float:
    time_list = timeit.timeit(check_in_list, number=number)
    time_set = timeit.timeit(check_in_set, number=number)
    return time_list / time_set


def main() -> None:
    speedup = benchmark_speedup()
    print(f"set быстрее list в x{speedup:.1f} раз на проверке 'in' по 10000 элементам")

    assert speedup > 5, f"ожидали заметное ускорение (>5x), получили x{speedup:.1f}"


if __name__ == "__main__":
    main()

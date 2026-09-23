"""
reduce, partial, lru_cache, cached_property, itertools рецепты.

Запуск: python main.py
"""
from __future__ import annotations

import itertools
import time
from functools import cached_property, lru_cache, partial, reduce


def demo_reduce_partial() -> None:
    print("--- reduce / partial ---")
    total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    print(f"reduce sum: {total}")

    def power(base: float, exponent: float) -> float:
        return base**exponent

    square = partial(power, exponent=2)
    print(f"square(5) = {square(5)}")


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def demo_lru_cache() -> None:
    print("\n--- lru_cache ---")
    start = time.perf_counter()
    result = fib(30)
    elapsed = time.perf_counter() - start
    print(f"fib(30) = {result} за {elapsed:.5f}s")
    print(fib.cache_info())


class Report:
    def __init__(self, rows: list[dict]) -> None:
        self.rows = rows
        self.compute_count = 0

    @cached_property
    def total(self) -> float:
        self.compute_count += 1
        return sum(r["amount"] for r in self.rows)


def demo_cached_property() -> None:
    print("\n--- cached_property ---")
    r = Report([{"amount": 1}, {"amount": 2}, {"amount": 3}])
    print(r.total, r.total, r.total)
    print(f"вычислено раз: {r.compute_count}")
    assert r.compute_count == 1


def demo_itertools() -> None:
    print("\n--- itertools ---")
    print(list(itertools.chain([1, 2], [3, 4])))
    print([list(g) for _, g in itertools.groupby("aaabbbcca")])
    print(list(itertools.product([1, 2], ["a", "b"])))
    print(list(itertools.combinations([1, 2, 3], 2)))
    print(list(itertools.islice(itertools.count(10), 5)))


def main() -> None:
    demo_reduce_partial()
    demo_lru_cache()
    demo_cached_property()
    demo_itertools()


if __name__ == "__main__":
    main()

"""
Наивная рекурсия vs мемоизация vs табуляция: fib, и DP-пример coin_change.

Запуск: python main.py
"""
from __future__ import annotations

import time
from functools import lru_cache


def fib_naive(n: int) -> int:
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def fib_tabulation(n: int) -> int:
    if n < 2:
        return n
    prev, curr = 0, 1
    for _ in range(n - 1):
        prev, curr = curr, prev + curr
    return curr


def coin_change(coins: list[int], amount: int) -> int:
    INF = float("inf")
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1


def main() -> None:
    n = 28

    start = time.perf_counter()
    naive_result = fib_naive(n)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    memo_result = fib_memo(n)
    memo_time = time.perf_counter() - start

    start = time.perf_counter()
    tab_result = fib_tabulation(n)
    tab_time = time.perf_counter() - start

    assert naive_result == memo_result == tab_result

    print(f"fib_naive({n}):      {naive_time:.5f}s")
    print(f"fib_memo({n}):       {memo_time:.5f}s")
    print(f"fib_tabulation({n}): {tab_time:.5f}s")

    print(f"\ncoin_change([1,5,10,25], 63) = {coin_change([1, 5, 10, 25], 63)}")  # 6 (25+25+10+1+1+1)


if __name__ == "__main__":
    main()

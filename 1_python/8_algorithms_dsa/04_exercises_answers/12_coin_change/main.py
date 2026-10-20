"""Решение: 12_coin_change"""
from __future__ import annotations


def coin_change(coins: list[int], amount: int) -> int:
    INF = float("inf")
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1


def main() -> None:
    checks_passed = 0
    total_checks = 4
    assert coin_change([1, 5, 10, 25], 63) == 6
    checks_passed += 1
    assert coin_change([2], 3) == -1
    checks_passed += 1
    assert coin_change([1], 0) == 0
    checks_passed += 1
    assert coin_change([1, 2, 5], 11) == 3
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

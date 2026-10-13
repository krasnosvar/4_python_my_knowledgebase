"""
Задача (сложный уровень): дан набор номиналов монет и сумма amount.
Найти минимальное число монет, чтобы набрать ровно amount (каждый номинал
можно использовать неограниченное число раз). Если набрать сумму
невозможно — вернуть -1. Решить через табуляцию (1D DP), O(amount * len(coins)).

Запусти: python main.py
"""
from __future__ import annotations


def coin_change(coins: list[int], amount: int) -> int:
    """
    TODO: dp[i] — минимум монет для суммы i, размер массива amount + 1.
      - dp[0] = 0 (базовый случай).
      - dp[i] = min(dp[i], dp[i - coin] + 1) для каждой монеты coin <= i.
      - Используй float("inf") как значение "недостижимо" перед вычислением.
    Вернуть dp[amount], если оно не осталось "inf", иначе -1.
    """
    raise NotImplementedError


def main() -> None:
    assert coin_change([1, 5, 10, 25], 63) == 6   # 25+25+10+1+1+1
    assert coin_change([2], 3) == -1               # нечётную сумму монетами по 2 не набрать
    assert coin_change([1], 0) == 0
    assert coin_change([1, 2, 5], 11) == 3         # 5+5+1

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

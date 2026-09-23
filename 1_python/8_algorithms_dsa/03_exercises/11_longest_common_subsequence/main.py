"""
Задача (сложный уровень): найти длину наибольшей общей подпоследовательности
(LCS) двух строк — не обязательно непрерывной, но с сохранением порядка
символов. Классическая 2D динамика: O(n*m) времени и памяти.

Пример: LCS("abcde", "ace") = "ace", длина 3.

Запусти: python main.py
"""
from __future__ import annotations


def longest_common_subsequence(a: str, b: str) -> int:
    """
    TODO: построить таблицу dp размером (len(a)+1) x (len(b)+1),
    dp[i][j] = длина LCS для a[:i] и b[:j].
      - dp[0][j] = dp[i][0] = 0 (базовый случай — пустая строка).
      - Если a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1.
      - Иначе: dp[i][j] = max(dp[i-1][j], dp[i][j-1]).
    Вернуть dp[len(a)][len(b)].
    """
    raise NotImplementedError


def main() -> None:
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    assert longest_common_subsequence("", "abc") == 0
    assert longest_common_subsequence("bsbininm", "jmjkbkjkv") == 1

    print("Все тесты прошли")


if __name__ == "__main__":
    main()

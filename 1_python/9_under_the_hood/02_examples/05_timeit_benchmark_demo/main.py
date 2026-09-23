"""
timeit: точное сравнение двух реализаций одной задачи.

Запуск: python main.py
"""
from __future__ import annotations

import timeit


def concat_with_plus(words: list[str]) -> str:
    result = ""
    for word in words:
        result += word + " "
    return result


def concat_with_join(words: list[str]) -> str:
    return " ".join(words)


def main() -> None:
    words = [f"word{i}" for i in range(500)]

    time_plus = timeit.timeit(lambda: concat_with_plus(words), number=1000)
    time_join = timeit.timeit(lambda: concat_with_join(words), number=1000)

    print(f"конкатенация через +=:  {time_plus:.4f}s (1000 запусков)")
    print(f"конкатенация через join: {time_join:.4f}s (1000 запусков)")
    print(f"join быстрее в x{time_plus / time_join:.1f} раз")

    assert time_join < time_plus, "join должен быть быстрее += на строках"


if __name__ == "__main__":
    main()

"""
Задача (лёгкий уровень): дан список чисел nums и целевая сумма target.
Найти индексы двух чисел, сумма которых равна target. Решить за O(n)
(не за O(n^2) вложенным циклом) с помощью хеш-таблицы.

Запусти: python main.py
"""
from __future__ import annotations


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """
    TODO: пройти по nums один раз, храня в словаре {значение: индекс}
    уже просмотренные числа. Для каждого x проверять, есть ли в словаре
    (target - x). Вернуть пару индексов (i, j), i < j.
    """
    raise NotImplementedError


def main() -> None:
    result = two_sum([2, 7, 11, 15], target=9)
    assert result == (0, 1), f"ожидали (0, 1), получили {result}"

    result2 = two_sum([3, 2, 4], target=6)
    assert result2 == (1, 2), f"ожидали (1, 2), получили {result2}"

    print("Все тесты прошли:", result, result2)


if __name__ == "__main__":
    main()

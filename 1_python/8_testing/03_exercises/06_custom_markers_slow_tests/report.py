"""Готовый модуль — функции разной "тяжести" для демонстрации маркеров."""
from __future__ import annotations


def quick_sum(n: int) -> int:
    return n * (n + 1) // 2


def heavy_sum(n: int) -> int:
    """Специально неэффективная реализация — для демонстрации @pytest.mark.slow."""
    total = 0
    for i in range(n + 1):
        total += i
    return total

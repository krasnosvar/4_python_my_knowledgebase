"""Модуль с намеренно не полностью покрытой веткой — для демонстрации coverage."""
from __future__ import annotations


def apply_discount(price: float, is_vip: bool) -> float:
    if is_vip:
        return price * 0.8
    else:
        return price  # эта ветка не покрыта тестами в этом примере намеренно

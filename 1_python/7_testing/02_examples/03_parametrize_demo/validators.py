"""Функции-валидаторы — предмет тестирования для примера parametrize."""
from __future__ import annotations


def is_valid_age(age: int) -> bool:
    return 0 <= age <= 150


def classify_number(n: int) -> str:
    if n > 0:
        return "positive"
    if n < 0:
        return "negative"
    return "zero"

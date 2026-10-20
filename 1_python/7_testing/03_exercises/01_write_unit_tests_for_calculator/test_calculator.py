"""
Задача: написать тесты для calculator.py (add, subtract, divide).

Запусти: pytest 03_exercises/01_write_unit_tests_for_calculator -v
Все тесты ниже должны пройти после того, как заполнишь TODO.
"""
from __future__ import annotations

import pytest

from calculator import add, divide, subtract


def test_add():
    # TODO: проверить, что add(2, 3) == 5
    raise NotImplementedError


def test_subtract():
    # TODO: проверить, что subtract(5, 3) == 2
    raise NotImplementedError


def test_divide_normal_case():
    # TODO: проверить, что divide(10, 2) == 5
    raise NotImplementedError


def test_divide_by_zero_raises_value_error():
    # TODO: использовать pytest.raises(ValueError) вокруг divide(10, 0)
    raise NotImplementedError

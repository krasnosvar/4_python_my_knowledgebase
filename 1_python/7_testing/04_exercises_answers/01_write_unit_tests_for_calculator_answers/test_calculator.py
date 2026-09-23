"""Решение: 01_write_unit_tests_for_calculator"""
from __future__ import annotations

import pytest

from calculator import add, divide, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_divide_normal_case():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError):
        divide(10, 0)

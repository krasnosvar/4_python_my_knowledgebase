"""
Базовые тесты pytest: обычный assert, структура Arrange-Act-Assert,
проверка исключений через pytest.raises.

Запуск: pytest 02_examples/01_pytest_basic_tests
"""
from __future__ import annotations

import pytest

from calculator import add, divide


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_divide_normal_case():
    # Arrange
    a, b = 10, 2
    # Act
    result = divide(a, b)
    # Assert
    assert result == 5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="division by zero"):
        divide(10, 0)

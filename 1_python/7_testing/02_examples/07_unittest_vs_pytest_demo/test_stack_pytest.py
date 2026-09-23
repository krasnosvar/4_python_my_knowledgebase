"""
Тот же Stack, pytest-стиль: fixture вместо setUp, assert вместо
assertEqual, parametrize вместо subTest.

Запуск: pytest 02_examples/07_unittest_vs_pytest_demo/test_stack_pytest.py
"""
from __future__ import annotations

import pytest

from stack import Stack


@pytest.fixture
def stack() -> Stack:
    return Stack()


def test_push_pop(stack: Stack):
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_pop_empty_raises(stack: Stack):
    with pytest.raises(IndexError):
        stack.pop()


@pytest.mark.parametrize("value", [1, "two", 3.0, None])
def test_multiple_values(stack: Stack, value):
    stack.push(value)
    assert stack.pop() == value

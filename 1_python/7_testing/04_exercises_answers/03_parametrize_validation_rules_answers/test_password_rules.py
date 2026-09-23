"""Решение: 03_parametrize_validation_rules"""
from __future__ import annotations

import pytest

from password_rules import is_valid_password


@pytest.mark.parametrize("password, expected", [
    ("Short1", False),
    ("nouppercase1", False),
    ("NOLOWERCASE1", False),
    ("NoDigitsHere", False),
    ("ValidPass1", True),
])
def test_is_valid_password(password, expected):
    assert is_valid_password(password) == expected

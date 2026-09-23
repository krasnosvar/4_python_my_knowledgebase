"""
Задача: с помощью @pytest.mark.parametrize проверить is_valid_password
на наборе паролей: короткий, без заглавной буквы, без цифры, без
строчной буквы, и корректный пароль.

Запусти: pytest 03_exercises/03_parametrize_validation_rules -v
"""
from __future__ import annotations

import pytest

from password_rules import is_valid_password


@pytest.mark.parametrize("password, expected", [
    # TODO: заполнить минимум 5 кейсов, например:
    # ("Short1", False),       # короче 8 символов
    # ("nouppercase1", False), # нет заглавной буквы
    # ("NOLOWERCASE1", False), # нет строчной буквы
    # ("NoDigitsHere", False), # нет цифры
    # ("ValidPass1", True),    # удовлетворяет всем правилам
])
def test_is_valid_password(password, expected):
    assert is_valid_password(password) == expected

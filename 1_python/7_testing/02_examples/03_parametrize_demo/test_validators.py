"""
parametrize: базовый синтаксис, ids, несколько parametrize подряд,
параметризованная fixture.

Запуск: pytest 02_examples/03_parametrize_demo -v
"""
from __future__ import annotations

import pytest

from validators import classify_number, is_valid_age


@pytest.mark.parametrize("age, expected", [
    (0, True),
    (150, True),
    (-1, False),
    (151, False),
], ids=["min_valid", "max_valid", "below_range", "above_range"])
def test_is_valid_age(age, expected):
    assert is_valid_age(age) == expected


@pytest.mark.parametrize("n, expected", [
    (5, "positive"),
    (-5, "negative"),
    (0, "zero"),
])
def test_classify_number(n, expected):
    assert classify_number(n) == expected


@pytest.mark.parametrize("currency", ["USD", "EUR"])
@pytest.mark.parametrize("amount", [10, 100])
def test_amount_currency_combinations(amount, currency):
    """Два parametrize перемножаются: 2 x 2 = 4 запуска."""
    label = f"{amount} {currency}"
    assert isinstance(label, str)


@pytest.fixture(params=["sqlite", "in_memory"])
def backend_name(request):
    return request.param


def test_backend_is_known(backend_name):
    assert backend_name in {"sqlite", "in_memory"}

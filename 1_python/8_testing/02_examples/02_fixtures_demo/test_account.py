"""
Fixtures: базовое использование, yield-teardown, scope, композиция,
фабрики.

Запуск: pytest 02_examples/02_fixtures_demo
"""
from __future__ import annotations

import pytest

from account import Account


@pytest.fixture
def account() -> Account:
    """Function-scope: новый экземпляр на каждый тест."""
    acc = Account(balance=100)
    yield acc
    acc.close()


def test_withdraw(account: Account):
    account.withdraw(30)
    assert account.balance == 70


def test_deposit(account: Account):
    account.deposit(50)
    assert account.balance == 150


def test_teardown_closes_account(account: Account):
    assert account.closed is False
    # closed станет True в teardown этой же fixture, после теста


@pytest.fixture
def make_account():
    """Фабрика: несколько экземпляров с разными параметрами в одном тесте."""
    created: list[Account] = []

    def _make(balance: int = 0) -> Account:
        acc = Account(balance=balance)
        created.append(acc)
        return acc

    yield _make

    for acc in created:
        acc.close()


def test_multiple_accounts(make_account):
    rich = make_account(balance=1000)
    poor = make_account(balance=0)
    assert rich.balance > poor.balance

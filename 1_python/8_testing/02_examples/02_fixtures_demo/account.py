"""Простой класс Account — предмет тестирования для примера fixtures."""
from __future__ import annotations


class Account:
    def __init__(self, balance: int = 0) -> None:
        self.balance = balance
        self.closed = False

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount

    def close(self) -> None:
        self.closed = True

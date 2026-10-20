"""SOLID-рефакторинг сервиса заказов (до/после) + value-объект Money."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Money:
    amount: int  # храним в копейках, чтобы избежать ошибок округления float
    currency: str = "RUB"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("нельзя складывать разные валюты")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self) -> str:
        return f"Money({self.amount / 100:.2f} {self.currency})"


# --- "До": один класс отвечает за валидацию, сохранение и уведомление ---

class OrderProcessorBad:
    def process(self, order_id: str, items: list[str], total: Money) -> None:
        if not items:
            raise ValueError("пустой заказ")
        print(f"[db] заказ {order_id} сохранён")
        print(f"[email] уведомление о заказе {order_id} на {total} отправлено")


# --- "После": SRP + DIP через Protocol, зависимости внедряются снаружи ---

class Repository(Protocol):
    def save(self, order_id: str, items: list[str]) -> None: ...


class Notifier(Protocol):
    def notify(self, order_id: str, total: Money) -> None: ...


class OrderValidator:
    def validate(self, items: list[str]) -> None:
        if not items:
            raise ValueError("пустой заказ")


class DatabaseRepository:
    def save(self, order_id: str, items: list[str]) -> None:
        print(f"[db] заказ {order_id} сохранён")


class EmailNotifier:
    def notify(self, order_id: str, total: Money) -> None:
        print(f"[email] уведомление о заказе {order_id} на {total} отправлено")


class OrderProcessor:
    def __init__(self, validator: OrderValidator, repo: Repository, notifier: Notifier) -> None:
        self._validator = validator
        self._repo = repo
        self._notifier = notifier

    def process(self, order_id: str, items: list[str], total: Money) -> None:
        self._validator.validate(items)
        self._repo.save(order_id, items)
        self._notifier.notify(order_id, total)


if __name__ == "__main__":
    price = Money(150000) + Money(29900)  # 1500.00 + 299.00 руб
    print("Итого:", price)

    processor = OrderProcessor(OrderValidator(), DatabaseRepository(), EmailNotifier())
    processor.process("A-1001", ["ноутбук", "мышь"], price)

    # OrderProcessorBad делает то же самое, но три ответственности нельзя
    # ни протестировать по отдельности, ни подменить в тестах без реальной БД/почты.

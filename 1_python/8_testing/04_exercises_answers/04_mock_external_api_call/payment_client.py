"""Готовый модуль — клиент оплаты, использующий внешний HTTP-вызов."""
from __future__ import annotations

import requests


def charge(amount: float, card_token: str) -> bool:
    response = requests.post(
        "https://payments.example.com/charge",
        json={"amount": amount, "card_token": card_token},
        timeout=5,
    )
    return response.status_code == 200

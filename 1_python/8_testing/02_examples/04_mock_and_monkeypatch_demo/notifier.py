"""Модуль с внешней зависимостью (requests) — предмет тестирования для mock/monkeypatch."""
from __future__ import annotations

import time

import requests


def send_notification(message: str, url: str = "https://example.com/notify") -> bool:
    response = requests.post(url, json={"message": message})
    return response.status_code == 200


def get_timestamp() -> float:
    return time.time()

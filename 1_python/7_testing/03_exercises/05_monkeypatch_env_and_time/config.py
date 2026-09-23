"""Готовый модуль — читает конфигурацию из окружения и текущее время."""
from __future__ import annotations

import os
import time


def get_api_url() -> str:
    return os.environ.get("API_URL", "https://default.example.com")


def get_current_timestamp() -> float:
    return time.time()


def is_request_expired(issued_at: float, ttl_seconds: float) -> bool:
    return get_current_timestamp() - issued_at > ttl_seconds

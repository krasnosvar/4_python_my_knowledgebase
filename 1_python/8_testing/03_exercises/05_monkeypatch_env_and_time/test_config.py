"""
Задача: используя fixture monkeypatch, подменить переменную окружения
API_URL и функцию time.time в модуле config, чтобы протестировать
детерминированно.

Запусти: pytest 03_exercises/05_monkeypatch_env_and_time -v
"""
from __future__ import annotations

from config import get_api_url, is_request_expired


def test_get_api_url_uses_env_var(monkeypatch):
    """
    TODO: monkeypatch.setenv("API_URL", "https://custom.example.com"),
    затем проверить, что get_api_url() вернул именно это значение.
    """
    raise NotImplementedError


def test_get_api_url_falls_back_to_default(monkeypatch):
    """
    TODO: monkeypatch.delenv("API_URL", raising=False), затем проверить,
    что get_api_url() вернул дефолтный "https://default.example.com".
    """
    raise NotImplementedError


def test_is_request_expired_with_fixed_time(monkeypatch):
    """
    TODO: monkeypatch.setattr("config.time.time", lambda: 1000.0),
    затем проверить:
      is_request_expired(issued_at=990.0, ttl_seconds=5) is True   (10 > 5)
      is_request_expired(issued_at=999.0, ttl_seconds=5) is False  (1 <= 5)
    """
    raise NotImplementedError

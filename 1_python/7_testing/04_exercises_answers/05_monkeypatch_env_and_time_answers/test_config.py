"""Решение: 05_monkeypatch_env_and_time"""
from __future__ import annotations

from config import get_api_url, is_request_expired


def test_get_api_url_uses_env_var(monkeypatch):
    monkeypatch.setenv("API_URL", "https://custom.example.com")
    assert get_api_url() == "https://custom.example.com"


def test_get_api_url_falls_back_to_default(monkeypatch):
    monkeypatch.delenv("API_URL", raising=False)
    assert get_api_url() == "https://default.example.com"


def test_is_request_expired_with_fixed_time(monkeypatch):
    monkeypatch.setattr("config.time.time", lambda: 1000.0)
    assert is_request_expired(issued_at=990.0, ttl_seconds=5) is True
    assert is_request_expired(issued_at=999.0, ttl_seconds=5) is False

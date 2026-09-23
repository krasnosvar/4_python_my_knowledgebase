"""Решение: 04_mock_external_api_call"""
from __future__ import annotations

from unittest.mock import patch

from payment_client import charge


def test_charge_success():
    with patch("payment_client.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        assert charge(50.0, "tok_abc") is True


def test_charge_failure():
    with patch("payment_client.requests.post") as mock_post:
        mock_post.return_value.status_code = 402
        assert charge(50.0, "tok_abc") is False


def test_charge_calls_api_with_correct_arguments():
    with patch("payment_client.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        charge(99.5, "tok_123")
        mock_post.assert_called_once_with(
            "https://payments.example.com/charge",
            json={"amount": 99.5, "card_token": "tok_123"},
            timeout=5,
        )

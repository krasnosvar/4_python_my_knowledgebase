"""
unittest.mock.patch и monkeypatch: подмена внешней зависимости (requests),
подмена времени, side_effect.

Запуск: pytest 02_examples/04_mock_and_monkeypatch_demo
"""
from __future__ import annotations

from unittest.mock import Mock, patch

from notifier import get_timestamp, send_notification


def test_send_notification_with_patch():
    # Патчим requests.post ИМЕННО в модуле notifier, где он используется,
    # а не в модуле requests, где он определён.
    with patch("notifier.requests.post") as mock_post:
        mock_post.return_value.status_code = 200

        result = send_notification("hello")

        assert result is True
        mock_post.assert_called_once_with(
            "https://example.com/notify", json={"message": "hello"}
        )


@patch("notifier.requests.post")
def test_send_notification_failure(mock_post):
    mock_post.return_value.status_code = 500
    assert send_notification("hello") is False


def test_send_notification_side_effect_sequence():
    with patch("notifier.requests.post") as mock_post:
        mock_post.side_effect = [
            Mock(status_code=200),
            Mock(status_code=500),
        ]
        assert send_notification("first") is True
        assert send_notification("second") is False


def test_get_timestamp_with_monkeypatch(monkeypatch):
    monkeypatch.setattr("notifier.time.time", lambda: 1_700_000_000.0)
    assert get_timestamp() == 1_700_000_000.0

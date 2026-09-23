"""
Задача: используя unittest.mock.patch, подменить requests.post в модуле
payment_client (patch.object или строкой "payment_client.requests.post")
и написать тесты на успешную и неуспешную оплату, а также проверить,
что запрос ушёл с правильными аргументами.

Запусти: pytest 03_exercises/04_mock_external_api_call -v
"""
from __future__ import annotations

from unittest.mock import patch

from payment_client import charge


def test_charge_success():
    """
    TODO: с patch("payment_client.requests.post") замокать успешный ответ
    (status_code=200) и проверить, что charge(...) возвращает True.
    """
    raise NotImplementedError


def test_charge_failure():
    """
    TODO: замокать ответ с status_code=402 (payment required) и проверить,
    что charge(...) возвращает False.
    """
    raise NotImplementedError


def test_charge_calls_api_with_correct_arguments():
    """
    TODO: замокать requests.post, вызвать charge(99.5, "tok_123") и
    проверить через mock_post.assert_called_once_with(...), что вызов
    был сделан с правильным URL, json-телом (amount=99.5, card_token=
    "tok_123") и timeout=5.
    """
    raise NotImplementedError

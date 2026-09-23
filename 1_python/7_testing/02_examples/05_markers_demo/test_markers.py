"""
Маркеры: skip, skipif, xfail, кастомный маркер slow.

Запуск:
  pytest 02_examples/05_markers_demo -v                  # все тесты
  pytest 02_examples/05_markers_demo -m "not slow" -v     # без медленных
"""
from __future__ import annotations

import sys

import pytest


@pytest.mark.skip(reason="функция ещё не реализована")
def test_future_feature():
    assert False, "не должен выполниться"


@pytest.mark.skipif(sys.platform == "win32", reason="не работает на Windows")
def test_unix_specific_behavior():
    assert True


@pytest.mark.xfail(reason="известная проблема с округлением")
def test_known_rounding_bug():
    assert round(2.675, 2) == 2.68  # на практике float даёт 2.67 — ожидаемое падение


@pytest.mark.slow
def test_heavy_computation():
    total = sum(i * i for i in range(1_000_000))
    assert total > 0


def test_fast_and_simple():
    assert 1 + 1 == 2

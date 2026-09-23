"""Решение: 06_custom_markers_slow_tests"""
from __future__ import annotations

import sys

import pytest

from report import heavy_sum, quick_sum


def test_quick_sum():
    assert quick_sum(100) == 5050


@pytest.mark.slow
def test_heavy_sum_matches_quick_sum():
    assert heavy_sum(10_000) == quick_sum(10_000)


@pytest.mark.skipif(
    sys.platform not in {"linux", "darwin", "win32"},
    reason="неизвестная платформа",
)
def test_platform_specific():
    assert sys.platform in {"linux", "darwin", "win32"}

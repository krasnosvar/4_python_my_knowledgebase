"""
Задача:
  1. Зарегистрировать кастомный маркер "slow" (через pytest.ini рядом с
     этим файлом — файл уже создан, но нужно дописать в него маркер).
  2. Пометить тест heavy_sum маркером @pytest.mark.slow.
  3. Добавить тест, который пропускается (skip) на платформах, отличных
     от текущей (используй sys.platform и @pytest.mark.skipif с обратным
     условием, чтобы тест реально шёл на твоей ОС).

Запусти:
  pytest 03_exercises/06_custom_markers_slow_tests -v
  pytest 03_exercises/06_custom_markers_slow_tests -m "not slow" -v
"""
from __future__ import annotations

import sys

import pytest

from report import heavy_sum, quick_sum


def test_quick_sum():
    assert quick_sum(100) == 5050


def test_heavy_sum_matches_quick_sum():
    """TODO: пометить этот тест @pytest.mark.slow (декоратор над функцией)."""
    assert heavy_sum(10_000) == quick_sum(10_000)


def test_platform_specific():
    """
    TODO: добавить @pytest.mark.skipif(sys.platform not in {"linux", "darwin", "win32"}, ...)
    таким образом, чтобы тест пропускался только на неизвестной платформе
    (на практике будет выполняться всегда на linux/macOS/Windows).
    """
    assert sys.platform in {"linux", "darwin", "win32"}

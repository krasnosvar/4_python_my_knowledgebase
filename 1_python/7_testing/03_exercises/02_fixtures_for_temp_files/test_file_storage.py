"""
Задача: написать fixture `storage`, которая создаёт FileStorage во
временной директории (используя tempfile.TemporaryDirectory через
yield-teardown, либо встроенную pytest fixture tmp_path), и тесты,
использующие эту fixture.

Запусти: pytest 03_exercises/02_fixtures_for_temp_files -v
"""
from __future__ import annotations

import pytest

from file_storage import FileStorage


@pytest.fixture
def storage(tmp_path):
    """
    TODO: создать и вернуть FileStorage(tmp_path / "storage").
    Встроенная fixture pytest `tmp_path` (Path) уже создаёт уникальную
    временную директорию на каждый тест и удаляет её автоматически —
    отдельный teardown не нужен.
    """
    raise NotImplementedError


def test_write_and_read(storage: FileStorage):
    # TODO: storage.write("greeting", "hello"), затем проверить
    # storage.read("greeting") == "hello"
    raise NotImplementedError


def test_read_missing_key_raises(storage: FileStorage):
    # TODO: проверить, что storage.read("missing") бросает KeyError
    raise NotImplementedError


def test_delete_removes_value(storage: FileStorage):
    # TODO: записать значение, удалить его, убедиться что повторное
    # чтение бросает KeyError
    raise NotImplementedError

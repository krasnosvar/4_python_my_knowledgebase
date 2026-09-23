"""Решение: 02_fixtures_for_temp_files"""
from __future__ import annotations

import pytest

from file_storage import FileStorage


@pytest.fixture
def storage(tmp_path):
    return FileStorage(tmp_path / "storage")


def test_write_and_read(storage: FileStorage):
    storage.write("greeting", "hello")
    assert storage.read("greeting") == "hello"


def test_read_missing_key_raises(storage: FileStorage):
    with pytest.raises(KeyError):
        storage.read("missing")


def test_delete_removes_value(storage: FileStorage):
    storage.write("temp", "value")
    storage.delete("temp")
    with pytest.raises(KeyError):
        storage.read("temp")

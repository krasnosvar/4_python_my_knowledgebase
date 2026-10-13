"""Решение: flatten через yield from."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any


def flatten(nested: list[Any]) -> Iterator[Any]:
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def main() -> None:
    result = list(flatten([1, [2, 3, [4, 5]], 6]))
    assert result == [1, 2, 3, 4, 5, 6], f"result: {result}"

    deep = list(flatten([1, [2, [3, [4, [5]]]]]))
    assert deep == [1, 2, 3, 4, 5], f"deep: {deep}"

    empty_nested = list(flatten([1, [], [2, []], 3]))
    assert empty_nested == [1, 2, 3], f"empty_nested: {empty_nested}"

    mixed_types = list(flatten(["a", [1, "b"], [True, [None]]]))
    assert mixed_types == ["a", 1, "b", True, None], f"mixed_types: {mixed_types}"

    print("PASS")


if __name__ == "__main__":
    main()

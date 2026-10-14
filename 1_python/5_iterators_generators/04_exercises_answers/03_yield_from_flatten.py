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
    checks_passed = 0
    total_checks = 4

    result = list(flatten([1, [2, 3, [4, 5]], 6]))
    assert result == [1, 2, 3, 4, 5, 6], f"result: {result}"
    checks_passed += 1

    deep = list(flatten([1, [2, [3, [4, [5]]]]]))
    assert deep == [1, 2, 3, 4, 5], f"deep: {deep}"
    checks_passed += 1

    empty_nested = list(flatten([1, [], [2, []], 3]))
    assert empty_nested == [1, 2, 3], f"empty_nested: {empty_nested}"
    checks_passed += 1

    mixed_types = list(flatten(["a", [1, "b"], [True, [None]]]))
    assert mixed_types == ["a", 1, "b", True, None], f"mixed_types: {mixed_types}"
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

"""Решение: пагинация через itertools.islice."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import count, islice
from typing import TypeVar

T = TypeVar("T")


def get_page(source: Iterable[T], page_number: int, page_size: int) -> list[T]:
    start = (page_number - 1) * page_size
    stop = start + page_size
    return list(islice(source, start, stop))


def main() -> None:
    finite_source = list(range(1, 26))

    page_1 = get_page(finite_source, 1, 10)
    assert page_1 == list(range(1, 11)), page_1

    page_3 = get_page(finite_source, 3, 10)
    assert page_3 == [21, 22, 23, 24, 25], page_3

    page_4 = get_page(finite_source, 4, 10)
    assert page_4 == [], page_4

    infinite_source: Iterator[int] = count(start=1)
    page_2_infinite = get_page(infinite_source, 2, 5)
    assert page_2_infinite == [6, 7, 8, 9, 10], page_2_infinite

    print("PASS")


if __name__ == "__main__":
    main()

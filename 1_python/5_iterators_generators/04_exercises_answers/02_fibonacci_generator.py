"""Решение: генератор чисел Фибоначчи."""

from __future__ import annotations

from collections.abc import Iterator


def fibonacci(max_terms: int | None = None, max_value: int | None = None) -> Iterator[int]:
    a, b = 0, 1
    count = 0
    while True:
        if max_terms is not None and count >= max_terms:
            return
        if max_value is not None and a > max_value:
            return
        yield a
        a, b = b, a + b
        count += 1


def main() -> None:
    by_count = list(fibonacci(max_terms=8))
    assert by_count == [0, 1, 1, 2, 3, 5, 8, 13], f"by_count: {by_count}"

    by_value = list(fibonacci(max_value=10))
    assert by_value == [0, 1, 1, 2, 3, 5, 8], f"by_value: {by_value}"

    from itertools import islice

    first_five = list(islice(fibonacci(), 5))
    assert first_five == [0, 1, 1, 2, 3], f"first_five: {first_five}"

    print("PASS")


if __name__ == "__main__":
    main()

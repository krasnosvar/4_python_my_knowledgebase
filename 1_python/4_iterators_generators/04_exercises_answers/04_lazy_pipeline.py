"""Решение: ленивый генераторный пайплайн."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import islice

processed_counter = {"count": 0}


def source(n: int) -> Iterator[int]:
    yield from range(n)


def expensive_filter(numbers: Iterable[int]) -> Iterator[int]:
    for n in numbers:
        processed_counter["count"] += 1
        if n % 2 == 0:
            yield n


def double(numbers: Iterable[int]) -> Iterator[int]:
    for n in numbers:
        yield n * 2


def build_pipeline(n: int) -> Iterator[int]:
    return double(expensive_filter(source(n)))


def main() -> None:
    checks_passed = 0
    total_checks = 2

    processed_counter["count"] = 0

    pipeline = build_pipeline(1_000_000)
    first_three = list(islice(pipeline, 3))

    assert first_three == [0, 4, 8], f"first_three: {first_three}"
    checks_passed += 1

    processed = processed_counter["count"]
    assert processed < 100, (
        f"пайплайн не ленив: expensive_filter обработал {processed} элементов "
        "вместо нескольких - похоже, где-то материализуется список"
    )
    checks_passed += 1

    print(f"Обработано элементов до получения первых трёх результатов: {processed}")
    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

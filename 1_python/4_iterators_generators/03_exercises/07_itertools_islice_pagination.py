"""
Задача: реализовать пагинацию произвольного iterable через itertools.islice,
не превращая весь источник в список заранее (источник может быть большим
или бесконечным генератором).
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import count, islice
from typing import TypeVar

T = TypeVar("T")


def get_page(source: Iterable[T], page_number: int, page_size: int) -> list[T]:
    """Возвращает элементы страницы page_number (нумерация с 1) размера
    page_size из source. Если элементов не хватает - возвращает то, что есть
    (может быть короче page_size или пустым списком).

    Не должна проходить по source целиком, если он бесконечен.
    """
    # TODO: используйте itertools.islice с правильными start/stop,
    # исходя из page_number и page_size.
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 4

    finite_source = list(range(1, 26))  # 1..25

    page_1 = get_page(finite_source, 1, 10)
    assert page_1 == list(range(1, 11)), page_1
    checks_passed += 1

    page_3 = get_page(finite_source, 3, 10)
    assert page_3 == [21, 22, 23, 24, 25], page_3
    checks_passed += 1

    page_4 = get_page(finite_source, 4, 10)
    assert page_4 == [], page_4
    checks_passed += 1

    # источник может быть бесконечным - функция всё равно должна
    # завершиться быстро, не материализуя его целиком
    infinite_source: Iterator[int] = count(start=1)
    page_2_infinite = get_page(infinite_source, 2, 5)
    assert page_2_infinite == [6, 7, 8, 9, 10], page_2_infinite
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

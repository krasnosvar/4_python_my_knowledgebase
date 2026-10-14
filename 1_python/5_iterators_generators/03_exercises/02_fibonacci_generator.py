"""
Задача: реализовать генератор чисел Фибоначчи с двумя ограничивающими
режимами - по количеству членов и по верхней границе значения.
"""

from __future__ import annotations

from collections.abc import Iterator


def fibonacci(max_terms: int | None = None, max_value: int | None = None) -> Iterator[int]:
    """Генерирует последовательность Фибоначчи (0, 1, 1, 2, 3, 5, 8, ...).

    Если задан max_terms - останавливается после этого количества членов.
    Если задан max_value - останавливается, не включая значения > max_value.
    Если оба None - генератор бесконечен.
    """
    # TODO: реализуйте генератор с помощью yield.
    # Подсказка: держите пару (a, b) и на каждом шаге проверяйте условия
    # остановки перед yield.
    raise NotImplementedError
    yield  # pragma: no cover - чтобы функция оставалась генератором до реализации


def main() -> None:
    checks_passed = 0
    total_checks = 3

    by_count = list(fibonacci(max_terms=8))
    assert by_count == [0, 1, 1, 2, 3, 5, 8, 13], f"by_count: {by_count}"
    checks_passed += 1

    by_value = list(fibonacci(max_value=10))
    assert by_value == [0, 1, 1, 2, 3, 5, 8], f"by_value: {by_value}"
    checks_passed += 1

    # генератор должен быть ленивым - можно взять только первые элементы
    # из "бесконечного" вызова без max_terms/max_value
    from itertools import islice

    first_five = list(islice(fibonacci(), 5))
    assert first_five == [0, 1, 1, 2, 3], f"first_five: {first_five}"
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

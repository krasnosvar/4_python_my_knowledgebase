"""Тот же код с аннотациями типов: mypy находит ошибку до запуска."""

from __future__ import annotations


def calculate_total(prices: list[float], discount: float) -> float:
    total = sum(prices)
    return total - (total * discount)


def format_receipt(items: list[tuple[str, float]], total: float) -> str:
    lines = [f"{name}: {price}" for name, price in items]
    lines.append(f"Итого: {total}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Намеренная ошибка для демонстрации: discount передан строкой, а не float.
    # mypy укажет на неё ДО запуска: Argument "discount" has incompatible
    # type "str"; expected "float" — см. вывод `mypy typed_example.py`.
    result = calculate_total([100, 200, 300], "10")
    print(format_receipt([("book", 100), ("pen", 5)], result))

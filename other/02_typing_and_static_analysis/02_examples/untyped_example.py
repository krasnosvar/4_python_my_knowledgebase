# ВНИМАНИЕ: этот скрипт НАМЕРЕННО падает с TypeError при запуске
# (`python3 untyped_example.py`). Это не поломка репозитория, а сама суть
# примера: без аннотаций ошибка типа обнаруживается только во время
# выполнения. Сравните с typed_example.py, где mypy находит её до запуска.
"""Код без аннотаций типов: ошибка находится только в рантайме, когда до
проблемной строки дойдёт выполнение (здесь — TypeError в calculate_total)."""


def calculate_total(prices, discount):
    total = sum(prices)
    return total - (total * discount)


def format_receipt(items, total):
    lines = [f"{name}: {price}" for name, price in items]
    lines.append(f"Итого: {total}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Баг: discount передан как строка "10" (проценты), а не как доля 0.1.
    # `total * "10"` — это повторение строки, а `total - <строка>` падает
    # с TypeError. mypy сообщил бы об этом ДО запуска, а не после деплоя.
    result = calculate_total([100, 200, 300], "10")
    print(format_receipt([("book", 100), ("pen", 5)], result))

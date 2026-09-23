"""Код без аннотаций типов: ошибка находится только в рантайме, если вообще
находится (в данном примере print() "проглотит" любые типы без исключения)."""


def calculate_total(prices, discount):
    total = sum(prices)
    return total - (total * discount)


def format_receipt(items, total):
    lines = [f"{name}: {price}" for name, price in items]
    lines.append(f"Итого: {total}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Баг: discount передан как строка "10" (проценты), а не как доля 0.1.
    # Ничего не упадёт — просто результат будет неверным (total - total*"10" даже
    # не выполнится: TypeError на этой строке, но mypy сообщил бы об этом
    # ДО запуска, а не после деплоя).
    result = calculate_total([100, 200, 300], "10")
    print(format_receipt([("book", 100), ("pen", 5)], result))

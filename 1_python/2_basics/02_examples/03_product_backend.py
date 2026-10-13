"""
Пример: преобразование "сырых" данных заказов через comprehensions и match.

Демонстрирует:
- list/dict comprehensions для трансформации данных;
- match/case для ветвления по типу события.
"""

RAW_ORDERS = [
    {"id": 1, "product": "Клавиатура", "price": 45.0, "qty": 2, "status": "paid"},
    {"id": 2, "product": "Мышь", "price": 20.0, "qty": 1, "status": "pending"},
    {"id": 3, "product": "Монитор", "price": 199.99, "qty": 1, "status": "paid"},
    {"id": 4, "product": "Коврик", "price": 9.5, "qty": 3, "status": "cancelled"},
]


def enrich_orders(raw_orders: list[dict]) -> list[dict]:
    """Comprehension: добавляем поле total к каждому заказу."""
    return [
        {**order, "total": round(order["price"] * order["qty"], 2)}
        for order in raw_orders
    ]


def index_by_id(orders: list[dict]) -> dict[int, dict]:
    """Dict comprehension: строим быстрый доступ по id заказа."""
    return {order["id"]: order for order in orders}


def paid_totals_by_product(orders: list[dict]) -> dict[str, float]:
    """Dict comprehension с фильтрацией: суммы только по оплаченным заказам."""
    return {
        order["product"]: order["total"]
        for order in orders
        if order["status"] == "paid"
    }


def handle_event(event: dict) -> str:
    """match/case ветвление по структуре события."""
    match event:
        case {"type": "order_created", "order_id": order_id}:
            return f"Создан заказ #{order_id}"
        case {"type": "order_cancelled", "order_id": order_id, "reason": reason}:
            return f"Заказ #{order_id} отменён: {reason}"
        case {"type": "payment_failed", "order_id": order_id, "retries": retries} if retries >= 3:
            return f"Заказ #{order_id}: оплата не прошла после {retries} попыток, эскалация"
        case {"type": "payment_failed", "order_id": order_id}:
            return f"Заказ #{order_id}: сбой оплаты, повторная попытка"
        case _:
            return f"Неизвестное событие: {event}"


def main() -> None:
    orders = enrich_orders(RAW_ORDERS)
    print("Заказы с рассчитанной суммой:")
    for order in orders:
        print(f"  #{order['id']} {order['product']}: {order['total']}")

    by_id = index_by_id(orders)
    print(f"\nБыстрый доступ по id: заказ #3 -> {by_id[3]['product']}")

    totals = paid_totals_by_product(orders)
    print("\nСуммы по оплаченным заказам:")
    for product, total in totals.items():
        print(f"  {product}: {total}")

    events = [
        {"type": "order_created", "order_id": 10},
        {"type": "order_cancelled", "order_id": 11, "reason": "клиент передумал"},
        {"type": "payment_failed", "order_id": 12, "retries": 4},
        {"type": "payment_failed", "order_id": 13, "retries": 1},
        {"type": "shipment_delayed", "order_id": 14},
    ]
    print("\nОбработка событий:")
    for event in events:
        print(f"  {handle_event(event)}")


if __name__ == "__main__":
    main()

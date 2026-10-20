"""
Пример: работа со списками, множествами, словарями и comprehensions.

Демонстрирует:
- дедупликацию списка с сохранением порядка через set;
- подсчёт частот через dict.get();
- трансформацию и индексацию заказов через list/dict comprehensions;
- разбор структуры событий через match/case.

Запуск:
    python3 02_examples/01_orders_and_comprehensions.py
"""

# 1. Дедупликация тегов с сохранением порядка первых появлений
incoming_tags = ["backend", "python", "sql", "python", "backend", "linux"]
seen_tags = set()
unique_tags = []

for tag in incoming_tags:
    if tag not in seen_tags:
        seen_tags.add(tag)
        unique_tags.append(tag)

print(f"Уникальные теги по порядку: {unique_tags}")

# 2. Словарь как счётчик частот (паттерн get-or-default)
tag_counts = {}
for tag in incoming_tags:
    tag_counts[tag] = tag_counts.get(tag, 0) + 1

print("Частота тегов:")
for tag, count in tag_counts.items():
    print(f"  {tag}: {count}")

# 3. Обработка заказов через comprehensions
raw_orders = [
    {"id": 1, "product": "Клавиатура", "price": 45.0, "qty": 2, "status": "paid"},
    {"id": 2, "product": "Мышь", "price": 20.0, "qty": 1, "status": "pending"},
    {"id": 3, "product": "Монитор", "price": 199.99, "qty": 1, "status": "paid"},
    {"id": 4, "product": "Коврик", "price": 9.5, "qty": 3, "status": "cancelled"},
]

# List comprehension: создаём новый список словарей с полем total
orders_with_total = [
    {
        "id": order["id"],
        "product": order["product"],
        "status": order["status"],
        "total": round(order["price"] * order["qty"], 2),
    }
    for order in raw_orders
]

# Dict comprehension: быстрый доступ к заказу по его id
orders_by_id = {order["id"]: order for order in orders_with_total}
print(f"\nБыстрый поиск заказа #3: {orders_by_id[3]['product']}")

# Dict comprehension с фильтром: суммы только по оплаченным заказам
paid_totals = {
    order["product"]: order["total"]
    for order in orders_with_total
    if order["status"] == "paid"
}
print("Оплаченные заказы:")
for product, total in paid_totals.items():
    print(f"  {product}: {total}")

# 4. Разбор событий через match/case по структуре словаря
events = [
    {"type": "order_created", "order_id": 10},
    {"type": "payment_failed", "order_id": 12, "retries": 4},
    {"type": "payment_failed", "order_id": 13, "retries": 1},
]

print("\nСобытия:")
for event in events:
    match event:
        case {"type": "order_created", "order_id": order_id}:
            print(f"  Создан заказ #{order_id}")
        case {"type": "payment_failed", "order_id": order_id, "retries": r} if r >= 3:
            print(f"  Заказ #{order_id}: сбой оплаты после {r} попыток, эскалация")
        case {"type": "payment_failed", "order_id": order_id}:
            print(f"  Заказ #{order_id}: повторная попытка оплаты")
        case _:
            print(f"  Неизвестное событие: {event}")

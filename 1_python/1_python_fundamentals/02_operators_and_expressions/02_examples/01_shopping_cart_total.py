"""
Пример: подсчёт стоимости корзины с операторами и f-строками.

Запуск:
    python 02_examples/01_shopping_cart_total.py
"""

price_per_item = 149.90
quantity = 3
discount_percent = 10

subtotal = price_per_item * quantity
discount_amount = subtotal * discount_percent / 100
total = subtotal - discount_amount

print(f"Цена за штуку: {price_per_item}")
print(f"Количество: {quantity}")
print(f"Промежуточный итог: {subtotal:.2f}")
print(f"Скидка {discount_percent}%: -{discount_amount:.2f}")
print(f"Итого к оплате: {total:.2f}")

# Целочисленное деление и остаток - типичная задача "разложить на части".
total_seconds = 125
minutes = total_seconds // 60
seconds = total_seconds % 60
print(f"\n{total_seconds} секунд = {minutes} мин {seconds} сек")

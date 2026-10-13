"""
Пример: небольшой интерактивный скрипт с input() и print().

Запуск:
    python 02_examples/01_greeting_cli.py
"""

name = input("Как тебя зовут? ")
age_text = input("Сколько тебе лет? ")
age = int(age_text)

print(f"Привет, {name}!")
print(f"Через 10 лет тебе будет {age + 10}.")
print("Загрузка", end="")
print("...", end="")
print(" готово!")

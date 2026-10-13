"""
Пример: функции для конвертации температуры.

Запуск:
    python 02_examples/01_temperature_converter.py
"""


def celsius_to_fahrenheit(celsius):
    """Переводит градусы Цельсия в Фаренгейты."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Переводит градусы Фаренгейта в Цельсий."""
    return (fahrenheit - 32) * 5 / 9


def describe_temperature(celsius, unit="C"):
    """Возвращает строку с температурой в указанной единице (C или F)."""
    if unit == "F":
        value = celsius_to_fahrenheit(celsius)
        return f"{value:.1f}°F"
    return f"{celsius:.1f}°C"


print(describe_temperature(25))             # единица по умолчанию - Цельсий
print(describe_temperature(25, unit="F"))    # явно запросили Фаренгейты
print(f"0°C = {celsius_to_fahrenheit(0)}°F")
print(f"98.6°F = {fahrenheit_to_celsius(98.6):.1f}°C")

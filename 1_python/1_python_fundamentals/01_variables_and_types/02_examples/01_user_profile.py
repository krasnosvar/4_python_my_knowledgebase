"""
Пример: простой профиль пользователя через переменные разных типов.

Запуск:
    python 02_examples/01_user_profile.py
"""

name = "Alex"
age = 25
height_m = 1.78
is_admin = False

print("Имя:", name, "- тип:", type(name))
print("Возраст:", age, "- тип:", type(age))
print("Рост (м):", height_m, "- тип:", type(height_m))
print("Админ:", is_admin, "- тип:", type(is_admin))

# Переменная из пользовательского ввода всегда приходит строкой.
age_from_input = "30"
age_in_a_year = int(age_from_input) + 1
print("Через год будет:", age_in_a_year)

# bool - это подвид int: True == 1, False == 0.
print("True + True =", True + True)
print("is_admin + 10 =", is_admin + 10)

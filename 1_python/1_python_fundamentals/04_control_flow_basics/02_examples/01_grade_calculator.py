"""
Пример: калькулятор оценок с if/elif/else и циклом for.

Запуск:
    python 02_examples/01_grade_calculator.py
"""

scores = [95, 82, 67, 45, 100]

for score in scores:
    if score >= 90:
        grade = "отлично"
    elif score >= 75:
        grade = "хорошо"
    elif score >= 60:
        grade = "удовлетворительно"
    else:
        grade = "неудовлетворительно"
    print(f"Балл {score}: {grade}")

# Поиск первого провального балла с остановкой через break.
found_failing = False
for score in scores:
    if score < 60:
        print(f"\nНайден первый провальный балл: {score}")
        found_failing = True
        break
if not found_failing:
    print("\nПровальных баллов нет")

# Сумма только проходных баллов, пропуская провальные через continue.
passing_total = 0
for score in scores:
    if score < 60:
        continue
    passing_total += score
print(f"Сумма проходных баллов: {passing_total}")

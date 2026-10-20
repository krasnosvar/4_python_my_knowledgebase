"""
Пример: калькулятор деления, который не падает на плохом вводе.

Запуск:
    python 02_examples/01_safe_calculator.py
"""


def divide(a_text, b_text):
    """Делит одно число на другое, оба приходят строками (как из input())."""
    try:
        a = float(a_text)
        b = float(b_text)
        result = a / b
    except ValueError:
        return f"Ошибка: {a_text!r} или {b_text!r} - не число"
    except ZeroDivisionError:
        return "Ошибка: делить на ноль нельзя"
    else:
        return f"{a_text} / {b_text} = {result:.2f}"
    finally:
        print(f"[лог] обработан ввод {a_text!r} и {b_text!r}")


def check_percent(value):
    """Своя проверка: процент должен быть от 0 до 100."""
    if value < 0 or value > 100:
        raise ValueError(f"Процент должен быть от 0 до 100, получено {value}")
    return value


print(divide("10", "4"))
print(divide("10", "0"))
print(divide("десять", "2"))

try:
    check_percent(150)
except ValueError as e:
    print(f"Перехвачено: {e}")

print(f"Корректный процент: {check_percent(42)}")

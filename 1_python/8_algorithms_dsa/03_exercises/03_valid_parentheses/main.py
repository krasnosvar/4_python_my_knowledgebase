"""
Задача (лёгкий уровень): проверить, что строка из скобок ()[]{}
сбалансирована (каждая открывающая скобка закрыта в правильном порядке).

Запусти: python main.py
"""
from __future__ import annotations


def is_balanced(s: str) -> bool:
    """
    TODO: использовать стек (list). Для открывающей скобки — push.
    Для закрывающей — если стек пуст или верхний элемент не соответствует
    закрывающей скобке (используй словарь соответствий) — вернуть False.
    В конце — вернуть True, только если стек полностью опустел.
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 1
    cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("", True),
        ("(((", False),
    ]
    for s, expected in cases:
        result = is_balanced(s)
        assert result == expected, f"is_balanced({s!r}) = {result}, ожидали {expected}"
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

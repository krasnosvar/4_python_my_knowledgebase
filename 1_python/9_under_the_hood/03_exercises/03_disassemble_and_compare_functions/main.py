"""
Задача: используя модуль dis, посчитать количество байткод-инструкций
двух эквивалентных функций и сравнить их.

Запусти: python main.py
"""
from __future__ import annotations

import dis
import io


def build_string_with_plus(n: int) -> str:
    result = ""
    for i in range(n):
        result += str(i)
    return result


def build_string_with_join(n: int) -> str:
    return "".join(str(i) for i in range(n))


def count_instructions(func) -> int:
    """
    TODO: вернуть количество байткод-инструкций функции func.
    Подсказка: dis.get_instructions(func) возвращает итератор Instruction —
    можно посчитать через len(list(dis.get_instructions(func))).
    """
    raise NotImplementedError


def main() -> None:
    plus_instructions = count_instructions(build_string_with_plus)
    join_instructions = count_instructions(build_string_with_join)

    print(f"build_string_with_plus:  {plus_instructions} инструкций")
    print(f"build_string_with_join:  {join_instructions} инструкций")

    assert plus_instructions > 0 and join_instructions > 0

    # Не обязательно join всегда компактнее по числу инструкций тела функции —
    # цель упражнения — научиться СЧИТАТЬ инструкции, а не угадать результат.
    print("\nПолный листинг build_string_with_plus:")
    dis.dis(build_string_with_plus)


if __name__ == "__main__":
    main()

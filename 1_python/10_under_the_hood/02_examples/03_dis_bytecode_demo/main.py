"""
dis: разбор байткода простых функций, сравнение эквивалентных реализаций.

Запуск: python main.py
"""
from __future__ import annotations

import dis


def add(a: int, b: int) -> int:
    return a + b


def membership_or(x: int) -> bool:
    return x == 1 or x == 2 or x == 3


def membership_in(x: int) -> bool:
    return x in (1, 2, 3)


def main() -> None:
    print("--- байткод простой функции ---")
    dis.dis(add)

    print("\n--- co_* атрибуты ---")
    code = add.__code__
    print(f"co_varnames: {code.co_varnames}")
    print(f"co_argcount: {code.co_argcount}")

    print("\n--- сравнение: цепочка 'or' vs 'in' с кортежем ---")
    print("membership_or:")
    dis.dis(membership_or)
    print("\nmembership_in:")
    dis.dis(membership_in)
    print(
        "\nчисло инструкций membership_in обычно меньше — "
        "сравнение с константным кортежем компилируется компактнее"
    )


if __name__ == "__main__":
    main()

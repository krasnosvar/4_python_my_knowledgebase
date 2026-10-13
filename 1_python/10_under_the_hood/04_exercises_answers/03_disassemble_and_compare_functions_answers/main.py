"""Решение: 03_disassemble_and_compare_functions"""
from __future__ import annotations

import dis


def build_string_with_plus(n: int) -> str:
    result = ""
    for i in range(n):
        result += str(i)
    return result


def build_string_with_join(n: int) -> str:
    return "".join(str(i) for i in range(n))


def count_instructions(func) -> int:
    return len(list(dis.get_instructions(func)))


def main() -> None:
    plus_instructions = count_instructions(build_string_with_plus)
    join_instructions = count_instructions(build_string_with_join)

    print(f"build_string_with_plus:  {plus_instructions} инструкций")
    print(f"build_string_with_join:  {join_instructions} инструкций")

    assert plus_instructions > 0 and join_instructions > 0

    print("\nПолный листинг build_string_with_plus:")
    dis.dis(build_string_with_plus)


if __name__ == "__main__":
    main()

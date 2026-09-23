"""
Задача (лёгкий уровень): развернуть список символов "на месте"
(без создания нового списка/строки), используя технику двух указателей.

Запусти: python main.py
"""
from __future__ import annotations


def reverse_in_place(chars: list[str]) -> None:
    """
    TODO: используя два указателя (left=0, right=len(chars)-1),
    менять местами chars[left] и chars[right], сдвигая указатели друг
    к другу, пока left < right. Функция ничего не возвращает — она
    изменяет chars на месте.
    """
    raise NotImplementedError


def main() -> None:
    chars = list("hello")
    reverse_in_place(chars)
    assert chars == list("olleh"), f"ожидали ['o','l','l','e','h'], получили {chars}"

    chars2 = list("a")
    reverse_in_place(chars2)
    assert chars2 == ["a"]

    chars3 = list("ab")
    reverse_in_place(chars3)
    assert chars3 == ["b", "a"]

    print("Все тесты прошли, reverse_in_place работает корректно")


if __name__ == "__main__":
    main()

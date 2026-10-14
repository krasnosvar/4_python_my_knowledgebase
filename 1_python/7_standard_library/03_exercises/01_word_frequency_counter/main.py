"""
Задача: по тексту построить частотный словарь слов (без учёта регистра,
без пунктуации) и вернуть 3 самых частых слова с их количеством.

Запусти: python main.py
"""
from __future__ import annotations

import re


TEXT = """
The quick brown fox jumps over the lazy dog.
The dog barks. The fox runs away. The quick fox is quick.
"""


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """
    TODO:
      1. Привести текст к нижнему регистру.
      2. Извлечь слова через re.findall(r"[a-z]+", text_lower).
      3. Построить collections.Counter по списку слов.
      4. Вернуть top-n через counter.most_common(n).
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 2
    result = top_words(TEXT, 3)
    print(result)

    assert result[0] == ("the", 5), f"ожидали ('the', 5) первым, получили {result[0]}"
    checks_passed += 1
    assert len(result) == 3
    checks_passed += 1
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

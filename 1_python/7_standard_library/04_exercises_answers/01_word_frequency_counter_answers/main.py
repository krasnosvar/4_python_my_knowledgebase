"""Решение: 01_word_frequency_counter"""
from __future__ import annotations

import re
from collections import Counter


TEXT = """
The quick brown fox jumps over the lazy dog.
The dog barks. The fox runs away. The quick fox is quick.
"""


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    words = re.findall(r"[a-z]+", text.lower())
    counts = Counter(words)
    return counts.most_common(n)


def main() -> None:
    result = top_words(TEXT, 3)
    print(result)

    assert result[0] == ("the", 5), f"ожидали ('the', 5) первым, получили {result[0]}"
    assert len(result) == 3


if __name__ == "__main__":
    main()

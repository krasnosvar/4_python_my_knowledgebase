"""Решение: счётчик частоты слов на словаре (dict)."""


def word_frequency(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def _self_check() -> None:
    checks_passed = 0
    total_checks = 5

    sample = "the quick brown fox jumps over the lazy dog the fox runs"
    result = word_frequency(sample)

    assert result["the"] == 3, (
        f"Ожидалось 3 вхождения 'the', получено {result.get('the')}"
    )
    checks_passed += 1
    print("PASS: 'the' встречается 3 раза")

    assert result["fox"] == 2, (
        f"Ожидалось 2 вхождения 'fox', получено {result.get('fox')}"
    )
    checks_passed += 1
    print("PASS: 'fox' встречается 2 раза")

    assert result["dog"] == 1, "Ожидалось 1 вхождение 'dog'"
    checks_passed += 1
    print("PASS: 'dog' встречается 1 раз")

    case_result = word_frequency("Hello hello HELLO")
    assert case_result == {"hello": 3}, (
        f"Ожидался регистронезависимый подсчёт, получено {case_result}"
    )
    checks_passed += 1
    print("PASS: подсчёт регистронезависим")

    empty_result = word_frequency("")
    assert empty_result == {}, "Пустая строка должна давать пустой словарь"
    checks_passed += 1
    print("PASS: пустая строка обрабатывается корректно")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

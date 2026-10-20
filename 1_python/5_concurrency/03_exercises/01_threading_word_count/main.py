"""
Задача: есть список "документов" (эмулируем I/O через time.sleep) и функция
подсчёта слов. Нужно обработать все документы конкурентно с помощью потоков
и вернуть суммарное число слов.

Запусти: python main.py
"""
from __future__ import annotations

import threading
import time


def fetch_document(doc_id: int) -> str:
    """Имитация сетевого/файлового I/O."""
    time.sleep(0.1)
    return f"slovo slovo slovo document {doc_id}"


def count_words_threaded(doc_ids: list[int]) -> int:
    """
    TODO: для каждого doc_id запустить отдельный поток, который:
      1. получает документ через fetch_document(doc_id)
      2. считает число слов (str.split())
      3. кладёт результат в общий список/структуру потокобезопасно

    Вернуть суммарное количество слов по всем документам.
    Использовать threading.Thread + threading.Lock (или список с одним
    элементом на поток, чтобы избежать гонки при накоплении суммы).
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 2

    doc_ids = list(range(10))

    start = time.perf_counter()
    total = count_words_threaded(doc_ids)
    elapsed = time.perf_counter() - start

    expected = len("slovo slovo slovo document 0".split()) * len(doc_ids)
    assert total == expected, f"ожидали {expected} слов, получили {total}"
    checks_passed += 1
    assert elapsed < 0.5, "потоки должны обработать документы конкурентно (< 0.5s)"
    checks_passed += 1

    print(f"Суммарно слов: {total}, время: {elapsed:.2f}s")
    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

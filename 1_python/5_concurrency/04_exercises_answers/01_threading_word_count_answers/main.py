"""Решение: 01_threading_word_count"""
from __future__ import annotations

import threading
import time


def fetch_document(doc_id: int) -> str:
    time.sleep(0.1)
    return f"slovo slovo slovo document {doc_id}"


def count_words_threaded(doc_ids: list[int]) -> int:
    lock = threading.Lock()
    total = {"count": 0}

    def worker(doc_id: int) -> None:
        text = fetch_document(doc_id)
        n_words = len(text.split())
        with lock:
            total["count"] += n_words

    threads = [threading.Thread(target=worker, args=(doc_id,)) for doc_id in doc_ids]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return total["count"]


def main() -> None:
    doc_ids = list(range(10))

    start = time.perf_counter()
    total = count_words_threaded(doc_ids)
    elapsed = time.perf_counter() - start

    expected = len("slovo slovo slovo document 0".split()) * len(doc_ids)
    assert total == expected, f"ожидали {expected} слов, получили {total}"
    assert elapsed < 0.5, "потоки должны обработать документы конкурентно (< 0.5s)"

    print(f"Суммарно слов: {total}, время: {elapsed:.2f}s")


if __name__ == "__main__":
    main()

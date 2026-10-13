"""
threading ускоряет I/O-bound работу: пока один поток ждёт "сеть",
GIL освобождается и другой поток может выполняться.

Запуск: python main.py
"""
from __future__ import annotations

import threading
import time


def fake_network_call(name: str, delay: float) -> None:
    print(f"[{name}] запрос отправлен")
    time.sleep(delay)  # имитация ожидания ответа от сети — GIL освобождается
    print(f"[{name}] ответ получен")


def sequential(urls: list[tuple[str, float]]) -> float:
    start = time.perf_counter()
    for name, delay in urls:
        fake_network_call(name, delay)
    return time.perf_counter() - start


def threaded(urls: list[tuple[str, float]]) -> float:
    start = time.perf_counter()
    threads = [
        threading.Thread(target=fake_network_call, args=(name, delay))
        for name, delay in urls
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


def main() -> None:
    urls = [("a", 0.3), ("b", 0.3), ("c", 0.3), ("d", 0.3)]

    seq_time = sequential(urls)
    print(f"Последовательно: {seq_time:.2f}s\n")

    thr_time = threaded(urls)
    print(f"\nВ потоках: {thr_time:.2f}s")

    assert thr_time < seq_time / 2, "потоки должны дать заметное ускорение на I/O-bound"


if __name__ == "__main__":
    main()

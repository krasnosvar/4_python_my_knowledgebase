"""
re: search/match/findall/sub, именованные группы, жадность, флаги.

Запуск: python main.py
"""
from __future__ import annotations

import re


def demo_basic_functions() -> None:
    print("--- базовые функции ---")
    print(re.search(r"\d+", "order-42"))
    print(re.match(r"\d+", "42-order"))
    print(re.findall(r"\d+", "a1 b22 c333"))
    print(re.sub(r"\d+", "#", "a1 b22 c333"))
    print(re.split(r"\s*,\s*", "a, b,c ,  d"))


def demo_named_groups() -> None:
    print("\n--- именованные группы ---")
    pattern = re.compile(r"(?P<user>\w+)@(?P<domain>[\w.]+)")
    m = pattern.search("contact: den@example.com")
    assert m is not None
    print(m.group("user"), m.group("domain"))
    print(m.groupdict())


def demo_greedy_vs_lazy() -> None:
    print("\n--- жадный vs нежадный ---")
    text = "<a><b>"
    print(f"жадный  +: {re.findall(r'<.+>', text)}")
    print(f"нежадный +?: {re.findall(r'<.+?>', text)}")


def demo_flags() -> None:
    print("\n--- флаги ---")
    text = "Hello\nworld"
    print(re.search(r"^hello", text, re.IGNORECASE | re.MULTILINE))
    print(re.search(r"^world", text, re.MULTILINE))


def demo_log_level_extraction() -> None:
    print("\n--- практический паттерн: извлечение уровня лога ---")
    lines = [
        "2026-08-21 12:00:00 ERROR connection refused",
        "2026-08-21 12:00:01 INFO server started",
    ]
    for line in lines:
        m = re.search(r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b", line)
        print(f"{line!r} -> {m.group(1) if m else None}")


def main() -> None:
    demo_basic_functions()
    demo_named_groups()
    demo_greedy_vs_lazy()
    demo_flags()
    demo_log_level_extraction()


if __name__ == "__main__":
    main()

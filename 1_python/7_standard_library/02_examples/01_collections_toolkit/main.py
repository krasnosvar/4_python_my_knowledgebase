"""
Counter, defaultdict, deque, namedtuple на практике.

Запуск: python main.py
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque, namedtuple


def demo_counter() -> None:
    print("--- Counter ---")
    words = "the cat sat on the mat the cat ran".split()
    counts = Counter(words)
    print(counts)
    print(counts.most_common(2))

    a = Counter(a=3, b=1)
    b = Counter(a=1, b=2)
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")


def demo_defaultdict() -> None:
    print("\n--- defaultdict ---")
    groups: defaultdict[str, list[int]] = defaultdict(list)
    for n in range(10):
        key = "even" if n % 2 == 0 else "odd"
        groups[key].append(n)
    print(dict(groups))


def demo_deque() -> None:
    print("\n--- deque ---")
    recent_events: deque[str] = deque(maxlen=3)
    for event in ["login", "click", "purchase", "logout"]:
        recent_events.append(event)
        print(f"после {event}: {list(recent_events)}")


def demo_namedtuple() -> None:
    print("\n--- namedtuple ---")
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    print(p, p.x, p[0])


def main() -> None:
    demo_counter()
    demo_defaultdict()
    demo_deque()
    demo_namedtuple()


if __name__ == "__main__":
    main()

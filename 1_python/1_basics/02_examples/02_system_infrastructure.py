"""
Пример: обработка потока событий мониторинга.

Демонстрирует:
- дедупликацию списка через set;
- разницу в производительности list vs set при проверке принадлежности (замер времени);
- dict-счётчики для агрегации метрик.
"""

import random
import time


def make_event_stream(size: int, unique_ratio: float = 0.1) -> list[str]:
    """Генерирует поток event_id с повторами (unique_ratio задаёт долю уникальных id)."""
    unique_count = max(1, int(size * unique_ratio))
    pool = [f"evt-{i}" for i in range(unique_count)]
    return [random.choice(pool) for _ in range(size)]


def dedup_with_set(events: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_events = []
    for event_id in events:
        if event_id not in seen:
            seen.add(event_id)
            unique_events.append(event_id)
    return unique_events


def membership_check_list(events: list[str], lookups: list[str]) -> int:
    hits = 0
    for lookup in lookups:
        if lookup in events:   # O(n) на каждую проверку
            hits += 1
    return hits


def membership_check_set(events: set[str], lookups: list[str]) -> int:
    hits = 0
    for lookup in lookups:
        if lookup in events:   # O(1) в среднем на каждую проверку
            hits += 1
    return hits


def count_events_by_type(events: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event_id in events:
        # get-or-default: dict как быстрый счётчик
        counts[event_id] = counts.get(event_id, 0) + 1
    return counts


def main() -> None:
    events = make_event_stream(size=20_000, unique_ratio=0.05)

    unique_events = dedup_with_set(events)
    print(f"Всего событий: {len(events)}, уникальных: {len(unique_events)}")

    lookups = [f"evt-{i}" for i in range(1000)]
    events_as_set = set(events)

    start = time.perf_counter()
    membership_check_list(events, lookups)
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    membership_check_set(events_as_set, lookups)
    set_time = time.perf_counter() - start

    print(f"\nПроверка принадлежности {len(lookups)} элементов среди {len(events)}:")
    print(f"  list:  {list_time * 1000:.3f} мс")
    print(f"  set:   {set_time * 1000:.3f} мс")
    print(f"  ускорение: {list_time / set_time:.1f}x" if set_time > 0 else "  set почти мгновенно")

    counters = count_events_by_type(events)
    top5 = sorted(counters.items(), key=lambda kv: kv[1], reverse=True)[:5]
    print("\nТоп-5 самых частых событий:")
    for event_id, count in top5:
        print(f"  {event_id}: {count}")


if __name__ == "__main__":
    main()

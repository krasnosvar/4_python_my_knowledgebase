"""Решение: проверка принадлежности list (O(n)) против set (O(1))."""

import time


def check_membership_list(data: list[int], lookups: list[int]) -> int:
    hits = 0
    for lookup in lookups:
        if lookup in data:
            hits += 1
    return hits


def check_membership_set(data: list[int], lookups: list[int]) -> int:
    data_set = set(data)
    hits = 0
    for lookup in lookups:
        if lookup in data_set:
            hits += 1
    return hits


def main() -> None:
    checks_passed = 0
    total_checks = 2

    data = list(range(200_000))
    lookups = list(range(0, 200_000, 37))

    list_hits = check_membership_list(data, lookups)
    set_hits = check_membership_set(data, lookups)

    assert list_hits == set_hits, (
        "Обе версии должны находить одинаковое количество совпадений"
    )
    assert list_hits == len(lookups), (
        "Все элементы lookups присутствуют в data по построению"
    )
    checks_passed += 1
    print(
        f"PASS: обе версии нашли одинаковое количество совпадений ({list_hits})"
    )

    start = time.perf_counter()
    check_membership_list(data, lookups)
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    check_membership_set(data, lookups)
    set_time = time.perf_counter() - start

    print(f"list: {list_time * 1000:.2f} мс, set: {set_time * 1000:.2f} мс")

    assert set_time < list_time / 3, (
        "Ожидалось, что set-версия будет в разы быстрее list-версии"
    )
    checks_passed += 1
    print(f"PASS: set-версия быстрее в {list_time / set_time:.1f} раз")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

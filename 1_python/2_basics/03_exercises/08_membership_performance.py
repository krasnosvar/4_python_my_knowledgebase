"""
Упражнение: проверка принадлежности list vs set — замер производительности.

TODO: реализуйте обе функции проверки принадлежности:
  - check_membership_list: линейный поиск `x in list_data` для каждого lookup
  - check_membership_set: поиск `x in set_data` для каждого lookup (сначала
    преобразуйте list_data в set один раз внутри функции)

Самопроверка засечёт время выполнения обеих версий на большом наборе данных
и убедится, что set-версия существенно быстрее.
"""

import time


def check_membership_list(data: list[int], lookups: list[int]) -> int:
    """Возвращает количество lookups, найденных в data (поиск по списку)."""
    raise NotImplementedError("Используйте `x in data` в цикле по lookups")


def check_membership_set(data: list[int], lookups: list[int]) -> int:
    """Возвращает количество lookups, найденных в data (поиск через множество)."""
    raise NotImplementedError("Преобразуйте data в set один раз, затем ищите через него")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 2

    data = list(range(200_000))
    lookups = list(range(0, 200_000, 37))   # разбросанные по всему диапазону значения

    list_hits = check_membership_list(data, lookups)
    set_hits = check_membership_set(data, lookups)

    assert list_hits == set_hits, "Обе версии должны находить одинаковое количество совпадений"
    assert list_hits == len(lookups), "Все lookups присутствуют в data по построению"
    checks_passed += 1
    print(f"PASS: обе версии нашли одинаковое количество совпадений ({list_hits})")

    start = time.perf_counter()
    check_membership_list(data, lookups)
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    check_membership_set(data, lookups)
    set_time = time.perf_counter() - start

    print(f"list: {list_time * 1000:.2f} мс, set: {set_time * 1000:.2f} мс")

    assert set_time < list_time / 3, (
        f"Ожидалось, что set-версия будет заметно (в разы) быстрее list-версии, "
        f"получено list={list_time:.4f}с, set={set_time:.4f}с. "
        "Проверьте, что check_membership_set преобразует data в set ОДИН раз."
    )
    checks_passed += 1
    print(f"PASS: set-версия быстрее в {list_time / set_time:.1f} раз")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

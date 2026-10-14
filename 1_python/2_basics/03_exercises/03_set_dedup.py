"""
Упражнение: дедупликация с сохранением порядка.

TODO: реализуйте dedup_preserve_order(items) — верните список без
      повторов, сохранив порядок первого появления каждого элемента.
      Реализация обязана использовать set для проверки "уже видели ли мы это"
      (а не lst.count(...) / x in list_accumulator — это свело бы решение к O(n^2)).
"""

import time


def dedup_preserve_order(items: list) -> list:
    raise NotImplementedError("Используйте set для отслеживания уже увиденных элементов")


def _self_check() -> None:
    checks_passed = 0
    total_checks = 4

    result = dedup_preserve_order([3, 1, 3, 2, 1, 4])
    assert result == [3, 1, 2, 4], f"Ожидалось [3, 1, 2, 4], получено {result}"
    checks_passed += 1
    print("PASS: базовая дедупликация с сохранением порядка")

    result_empty = dedup_preserve_order([])
    assert result_empty == [], "Пустой вход должен давать пустой выход"
    checks_passed += 1
    print("PASS: пустой список на входе")

    result_no_dups = dedup_preserve_order([1, 2, 3])
    assert result_no_dups == [1, 2, 3], "Список без повторов должен вернуться без изменений"
    checks_passed += 1
    print("PASS: список без повторов остаётся неизменным")

    # Проверка производительности: на большом входе с большим количеством повторов
    # set-based решение должно укладываться в разумное время (сотни мс, не секунды).
    # Наивное O(n^2) решение (через `if x in result`) на 200_000 элементах будет
    # заметно медленнее.
    big_input = list(range(2000)) * 100   # 200_000 элементов, 2000 уникальных
    start = time.perf_counter()
    big_result = dedup_preserve_order(big_input)
    elapsed = time.perf_counter() - start

    assert len(big_result) == 2000, f"Ожидалось 2000 уникальных элементов, получено {len(big_result)}"
    assert elapsed < 1.0, (
        f"Дедупликация заняла {elapsed:.2f} с — похоже на O(n^2) решение "
        "(например, `if x in result_list`), а не O(n) через set"
    )
    checks_passed += 1
    print(f"PASS: 200_000 элементов дедуплицировано за {elapsed * 1000:.1f} мс")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

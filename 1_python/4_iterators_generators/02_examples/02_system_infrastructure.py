"""
Сравнение памяти список vs генератор, и работа с itertools.chain/islice
на примере нескольких "источников" системных логов.
"""

from __future__ import annotations

import sys
import time
from itertools import chain, islice
from collections.abc import Iterator

N = 1_000_000


def compare_memory() -> None:
    list_of_ints = [x for x in range(N)]
    gen_of_ints = (x for x in range(N))

    list_size = sys.getsizeof(list_of_ints)
    gen_size = sys.getsizeof(gen_of_ints)

    print("Сравнение памяти для", N, "элементов:")
    print(f"  список:   {list_size:>10} байт")
    print(f"  генератор:{gen_size:>10} байт")
    print(f"  разница:  {list_size / gen_size:.0f}x")


def compare_time_to_first_result() -> None:
    """Генератор отдаёт первый элемент мгновенно, список - только после
    полного построения всех N элементов."""

    start = time.perf_counter()
    first_from_list = [x * x for x in range(N)][0]
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    first_from_gen = next(x * x for x in range(N))
    gen_time = time.perf_counter() - start

    print("\nВремя получения первого результата:")
    print(f"  список:    {list_time * 1000:.3f} мс (значение {first_from_list})")
    print(f"  генератор: {gen_time * 1000:.3f} мс (значение {first_from_gen})")


def host_metrics(host: str) -> Iterator[str]:
    """Имитация источника метрик одного хоста."""
    for i in range(3):
        yield f"{host}: metric_{i}=OK"


def demo_chain_and_islice() -> None:
    hosts = ["web-01", "web-02", "db-01"]

    all_metrics = chain.from_iterable(host_metrics(h) for h in hosts)

    print("\nВсе метрики через chain (постранично по 4 через islice):")
    page = list(islice(all_metrics, 4))
    for line in page:
        print(f"  {line}")

    print("  следующая страница:")
    next_page = list(islice(all_metrics, 4))
    for line in next_page:
        print(f"  {line}")


def main() -> None:
    compare_memory()
    compare_time_to_first_result()
    demo_chain_and_islice()


if __name__ == "__main__":
    main()

"""
Пример 03: consistent hashing против простого hash(key) % N.

Демонстрирует главную проблему шардирования по модулю числа узлов: при
добавлении нового узла результат hash(key) % N меняется почти для всех
ключей (нужна массовая перебалансировка). Consistent hashing размещает
узлы и ключи на одном кольце хэшей и переносит только небольшую долю
ключей при добавлении узла.

Запуск: python3 ./02_examples/03_consistent_hashing/main.py
"""

from __future__ import annotations

import hashlib
import bisect


def stable_hash(value: str) -> int:
    """Детерминированный хэш строки в целое число (не зависит от PYTHONHASHSEED,
    в отличие от встроенного hash())."""
    return int(hashlib.md5(value.encode("utf-8")).hexdigest(), 16)


def naive_mod_shard(key: str, n_shards: int) -> int:
    return stable_hash(key) % n_shards


class ConsistentHashRing:
    """Кольцо хэшей с виртуальными узлами (несколько точек на кольце на
    каждый физический шард - для более равномерного распределения)."""

    def __init__(self, shards: list[str], virtual_nodes: int = 100) -> None:
        self.virtual_nodes = virtual_nodes
        self.ring: dict[int, str] = {}
        self.sorted_points: list[int] = []
        for shard in shards:
            self.add_shard(shard)

    def add_shard(self, shard: str) -> None:
        for i in range(self.virtual_nodes):
            point = stable_hash(f"{shard}#{i}")
            self.ring[point] = shard
            bisect.insort(self.sorted_points, point)

    def remove_shard(self, shard: str) -> None:
        for i in range(self.virtual_nodes):
            point = stable_hash(f"{shard}#{i}")
            del self.ring[point]
            self.sorted_points.remove(point)

    def get_shard(self, key: str) -> str:
        point = stable_hash(key)
        idx = bisect.bisect(self.sorted_points, point)
        if idx == len(self.sorted_points):
            idx = 0  # кольцо замкнуто - переходим к первой точке
        return self.ring[self.sorted_points[idx]]


def main() -> None:
    print("--- Пример: consistent hashing vs hash(key) % N ---")

    keys = [f"user:{i}" for i in range(2000)]

    # --- Наивный подход: hash(key) % N ---
    shards_before = 4
    shards_after = 5  # добавили один шард

    mapping_before = {k: naive_mod_shard(k, shards_before) for k in keys}
    mapping_after = {k: naive_mod_shard(k, shards_after) for k in keys}

    moved_naive = sum(1 for k in keys if mapping_before[k] != mapping_after[k])
    moved_naive_pct = 100.0 * moved_naive / len(keys)
    print(f"Наивный hash % N: было {shards_before} шардов, стало {shards_after}.")
    print(f"  Переместилось ключей: {moved_naive} из {len(keys)} ({moved_naive_pct:.1f}%)")

    # --- Consistent hashing ---
    ring = ConsistentHashRing(shards=["shard-0", "shard-1", "shard-2", "shard-3"])
    mapping_ring_before = {k: ring.get_shard(k) for k in keys}

    ring.add_shard("shard-4")
    mapping_ring_after = {k: ring.get_shard(k) for k in keys}

    moved_ring = sum(1 for k in keys if mapping_ring_before[k] != mapping_ring_after[k])
    moved_ring_pct = 100.0 * moved_ring / len(keys)
    print(f"\nConsistent hashing: было 4 шарда, стало 5 (добавили shard-4).")
    print(f"  Переместилось ключей: {moved_ring} из {len(keys)} ({moved_ring_pct:.1f}%)")

    expected_fraction_pct = 100.0 / 5  # в идеале ~K/N = 1/5 ключей должно переехать
    print(f"  Ожидаемая доля при идеальном распределении: ~{expected_fraction_pct:.1f}%")

    assert moved_naive_pct > 70.0, "наивный подход должен перемешать почти все ключи"
    assert moved_ring_pct < 40.0, "consistent hashing должен переместить лишь часть ключей"
    assert moved_ring_pct < moved_naive_pct

    print(
        "\nВывод: наивный hash % N при добавлении шарда перемешивает "
        "практически весь датасет, требуя массовой перебалансировки. "
        "Consistent hashing переносит только те ключи, что попали в "
        "диапазон нового узла на кольце — в разы меньшую долю, близкую "
        "к теоретическому идеалу 1/N."
    )


if __name__ == "__main__":
    main()

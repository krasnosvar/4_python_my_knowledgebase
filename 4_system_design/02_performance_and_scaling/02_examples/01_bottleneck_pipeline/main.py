"""
Пример 01: поиск узкого места в конвейере обработки.

Три последовательные "стадии" обработки запроса с разной пропускной
способностью (стадия = сколько запросов в секунду она способна
обработать). Запросы поступают с фиксированной интенсивностью (arrival
rate). Симуляция считает, у какой стадии перед ней накапливается очередь,
если пропускать через конвейер N запросов подряд, и показывает, что
throughput всего конвейера ограничен самой медленной стадией, а не
средней по всем стадиям.

Запуск: python3 ./02_examples/01_bottleneck_pipeline/main.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Stage:
    name: str
    capacity_rps: float  # сколько запросов в секунду стадия может обработать

    def time_per_request(self) -> float:
        return 1.0 / self.capacity_rps


def simulate_pipeline(stages: list[Stage], arrival_rate_rps: float, n_requests: int) -> dict[str, float]:
    """Прогоняет n_requests через конвейер стадий и возвращает среднюю
    длину очереди перед каждой стадией (в запросах) — грубая оценка на
    основе Little's Law (L = lambda * W), где W - среднее время ожидания
    перед стадией при данной интенсивности поступления.
    """
    queue_lengths: dict[str, float] = {}
    for stage in stages:
        service_rate = stage.capacity_rps
        if arrival_rate_rps >= service_rate:
            # Стадия не успевает: очередь растёт неограниченно -> узкое место.
            queue_lengths[stage.name] = float("inf")
        else:
            # Простая M/M/1-подобная оценка средней очереди: rho / (1 - rho).
            rho = arrival_rate_rps / service_rate
            queue_lengths[stage.name] = rho / (1 - rho)
    return queue_lengths


def pipeline_throughput(stages: list[Stage]) -> float:
    """Throughput всего конвейера = throughput самой медленной стадии."""
    return min(stage.capacity_rps for stage in stages)


def main() -> None:
    print("--- Пример: поиск узкого места в конвейере из трёх стадий ---")

    stages = [
        Stage("app_handler", capacity_rps=1000.0),
        Stage("cache_lookup", capacity_rps=5000.0),
        Stage("db_query", capacity_rps=200.0),
    ]

    arrival_rate = 150.0  # запросов в секунду поступает в конвейер
    queues = simulate_pipeline(stages, arrival_rate, n_requests=10_000)

    print(f"Интенсивность поступления: {arrival_rate:.0f} req/s\n")
    for stage in stages:
        q = queues[stage.name]
        q_str = "растёт неограниченно (перегружена)" if q == float("inf") else f"~{q:.2f} запросов в очереди"
        print(f"  {stage.name:12s} capacity={stage.capacity_rps:7.0f} req/s  {q_str}")

    throughput = pipeline_throughput(stages)
    bottleneck = min(stages, key=lambda s: s.capacity_rps)
    print(f"\nThroughput всего конвейера: {throughput:.0f} req/s "
          f"(ограничен стадией '{bottleneck.name}')")

    assert bottleneck.name == "db_query"
    assert throughput == 200.0

    # Поднимем интенсивность выше пропускной способности узкого места:
    # его очередь должна уйти в бесконечность, даже если остальные стадии
    # справляются легко.
    overloaded_queues = simulate_pipeline(stages, arrival_rate_rps=250.0, n_requests=1)
    assert overloaded_queues["db_query"] == float("inf")
    assert overloaded_queues["app_handler"] != float("inf")

    print(
        "\nВывод: даже если 'app_handler' и 'cache_lookup' обрабатывают "
        "тысячи запросов в секунду, весь конвейер ограничен 'db_query' — "
        "добавление мощности другим стадиям throughput не увеличит."
    )


if __name__ == "__main__":
    main()

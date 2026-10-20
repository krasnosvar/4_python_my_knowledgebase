"""
Пример 01: алгоритмы балансировки нагрузки.

Реализует Round Robin и Least Connections поверх одного и того же набора
серверов и одной и той же последовательности запросов с разной
длительностью обработки, чтобы показать разницу в итоговом распределении
нагрузки между алгоритмами, когда время обработки запросов неоднородно.

Запуск: python3 ./02_examples/01_load_balancer_algorithms/main.py
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import cycle


@dataclass
class Server:
    name: str
    active_connections: int = 0
    total_requests: int = 0
    busy_time: float = 0.0  # суммарное время обработки, условные единицы


class RoundRobinBalancer:
    def __init__(self, servers: list[Server]) -> None:
        self._servers = servers
        self._cycle = cycle(servers)

    def pick(self) -> Server:
        return next(self._cycle)


class LeastConnectionsBalancer:
    def __init__(self, servers: list[Server]) -> None:
        self._servers = servers

    def pick(self) -> Server:
        return min(self._servers, key=lambda s: s.active_connections)


def simulate(balancer, requests: list[float]) -> list[Server]:
    """Прогоняет запросы через балансировщик. Каждый запрос характеризуется
    длительностью обработки (условные единицы). Для простоты обработка
    моделируется мгновенно с точки зрения времени симуляции, но
    active_connections используется как индикатор "занятости" сервера
    на момент выбора следующего запроса (эмулирует конкурентные запросы,
    которые ещё не завершились к моменту прихода следующего)."""
    servers = balancer._servers
    for duration in requests:
        server = balancer.pick()
        server.total_requests += 1
        server.busy_time += duration
        # active_connections растёт пропорционально "тяжести" уже принятых
        # запросов - грубая модель того, что тяжёлые запросы держат
        # соединение дольше, и балансировщик должен это видеть.
        server.active_connections += duration
    return servers


def main() -> None:
    print("--- Пример: Round Robin vs Least Connections ---")

    # Смешанная нагрузка: один очень тяжёлый запрос (10.0) в начале,
    # затем много лёгких (1.0) - эмулирует ситуацию, когда один запрос
    # надолго занимает сервер, а остальные запросы куда легче.
    requests = [10.0] + [1.0] * 9

    rr_servers = [Server("srv-1"), Server("srv-2"), Server("srv-3")]
    rr = RoundRobinBalancer(rr_servers)
    simulate(rr, requests)

    lc_servers = [Server("srv-1"), Server("srv-2"), Server("srv-3")]
    lc = LeastConnectionsBalancer(lc_servers)
    simulate(lc, requests)

    print("\nRound Robin:")
    for s in rr_servers:
        print(
            f"  {s.name}: requests={s.total_requests:2d}  "
            f"busy_time={s.busy_time:5.1f}"
        )

    print("\nLeast Connections:")
    for s in lc_servers:
        print(
            f"  {s.name}: requests={s.total_requests:2d}  "
            f"busy_time={s.busy_time:5.1f}"
        )

    rr_busy_spread = max(s.busy_time for s in rr_servers) - min(
        s.busy_time for s in rr_servers
    )
    lc_busy_spread = max(s.busy_time for s in lc_servers) - min(
        s.busy_time for s in lc_servers
    )

    print(
        f"\nРазброс busy_time (max-min) Round Robin:        "
        f"{rr_busy_spread:.1f}"
    )
    print(
        f"Разброс busy_time (max-min) Least Connections:  "
        f"{lc_busy_spread:.1f}"
    )

    assert lc_busy_spread <= rr_busy_spread, (
        "Least Connections должен давать не худший (обычно лучший) разброс "
        "занятости серверов, чем Round Robin, при неоднородных запросах"
    )

    print(
        "\nВывод: Round Robin отправил тяжёлый запрос на srv-1, а затем "
        "продолжил раздавать лёгкие запросы по кругу вслепую, не заметив, "
        "что srv-1 уже занят надолго - в итоге srv-1 получил больше "
        "суммарной нагрузки, чем остальные. Least Connections видел, что "
        "srv-1 занят, и направлял последующие лёгкие запросы на менее "
        "загруженные srv-2/srv-3, выравнивая итоговую нагрузку лучше."
    )


if __name__ == "__main__":
    main()

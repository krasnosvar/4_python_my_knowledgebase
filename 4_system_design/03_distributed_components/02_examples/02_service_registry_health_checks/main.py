"""
Пример 02: реестр сервисов с health checks (упрощённое server-side discovery).

Реестр хранит список зарегистрированных инстансов сервиса вместе с меткой
времени последнего "сердцебиения" (heartbeat). Инстанс считается здоровым,
если heartbeat пришёл не позже, чем N секунд назад. Реестр отдаёт клиенту
только здоровые инстансы - ровно то, что делает Service Discovery в связке
со health checks перед тем, как балансировщик выберет из них один.

Запуск: python3 ./02_examples/02_service_registry_health_checks/main.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Instance:
    address: str
    last_heartbeat: float  # условное "время" последнего heartbeat


class ServiceRegistry:
    """Реестр: имя сервиса -> список инстансов с их последним heartbeat."""

    def __init__(self, health_timeout: float = 10.0) -> None:
        self.health_timeout = health_timeout
        self._instances: dict[str, dict[str, Instance]] = {}

    def register(self, service: str, address: str, now: float) -> None:
        self._instances.setdefault(service, {})[address] = Instance(address, now)

    def heartbeat(self, service: str, address: str, now: float) -> None:
        instances = self._instances.get(service, {})
        if address in instances:
            instances[address].last_heartbeat = now

    def deregister(self, service: str, address: str) -> None:
        self._instances.get(service, {}).pop(address, None)

    def healthy_instances(self, service: str, now: float) -> list[str]:
        """Возвращает адреса инстансов, чей heartbeat не устарел."""
        instances = self._instances.get(service, {})
        return [
            inst.address
            for inst in instances.values()
            if now - inst.last_heartbeat <= self.health_timeout
        ]


def main() -> None:
    print("--- Пример: service registry с health checks ---")

    registry = ServiceRegistry(health_timeout=10.0)

    # t=0: три инстанса регистрируются и сразу шлют heartbeat.
    t = 0.0
    for addr in ["10.0.0.1:8080", "10.0.0.2:8080", "10.0.0.3:8080"]:
        registry.register("orders-service", addr, now=t)

    healthy_t0 = registry.healthy_instances("orders-service", now=t)
    print(f"t={t:5.1f}: здоровые инстансы: {healthy_t0}")
    assert len(healthy_t0) == 3

    # t=5: 10.0.0.1 и 10.0.0.2 продолжают слать heartbeat вовремя,
    # а 10.0.0.3 "завис" и перестал отвечать - heartbeat не обновляется.
    t = 5.0
    registry.heartbeat("orders-service", "10.0.0.1:8080", now=t)
    registry.heartbeat("orders-service", "10.0.0.2:8080", now=t)
    # 10.0.0.3:8080 heartbeat не шлём.

    healthy_t5 = registry.healthy_instances("orders-service", now=t)
    print(f"t={t:5.1f}: здоровые инстансы: {healthy_t5}")
    assert len(healthy_t5) == 3, "пока не прошло 10 секунд с последнего heartbeat, инстанс всё ещё здоров"

    # t=16: с момента последнего heartbeat 10.0.0.3 прошло 16 секунд > timeout 10.
    # Он должен выпасть из списка здоровых, даже если формально не был
    # дерегистрирован явно - это и есть readiness/liveness через heartbeat.
    t = 16.0
    registry.heartbeat("orders-service", "10.0.0.1:8080", now=t)
    registry.heartbeat("orders-service", "10.0.0.2:8080", now=t)

    healthy_t16 = registry.healthy_instances("orders-service", now=t)
    print(f"t={t:5.1f}: здоровые инстансы: {healthy_t16}")
    assert "10.0.0.3:8080" not in healthy_t16
    assert len(healthy_t16) == 2

    # t=20: 10.0.0.3 восстановился и снова начал слать heartbeat -
    # он должен автоматически вернуться в пул здоровых, без ручной регистрации.
    t = 20.0
    registry.heartbeat("orders-service", "10.0.0.1:8080", now=t)
    registry.heartbeat("orders-service", "10.0.0.2:8080", now=t)
    registry.heartbeat("orders-service", "10.0.0.3:8080", now=t)

    healthy_t20 = registry.healthy_instances("orders-service", now=t)
    print(f"t={t:5.1f}: здоровые инстансы: {healthy_t20}")
    assert "10.0.0.3:8080" in healthy_t20
    assert len(healthy_t20) == 3

    print(
        "\nВывод: реестр отдаёт клиенту/балансировщику только те инстансы, "
        "чей heartbeat не устарел - зависший инстанс автоматически "
        "исключается из пула без ручного вмешательства, а восстановившийся "
        "автоматически возвращается, как только снова начинает отвечать."
    )


if __name__ == "__main__":
    main()

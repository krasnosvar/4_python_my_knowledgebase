"""
Пример 03: минимальный API Gateway - маршрутизация + сквозные проверки.

Показывает три типовые задачи шлюза из теории: маршрутизацию запроса к
нужному внутреннему сервису по префиксу пути, простую проверку токена на
периметре (аутентификация один раз, до сервиса) и простой rate limiting
по клиенту. Внутренние "сервисы" - просто функции-заглушки.

Запуск: python3 ./02_examples/03_api_gateway_routing/main.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


class Unauthorized(Exception):
    pass


class RateLimited(Exception):
    pass


class NotFound(Exception):
    pass


def orders_service(path: str) -> str:
    return f"orders-service handled {path}"


def users_service(path: str) -> str:
    return f"users-service handled {path}"


@dataclass
class ApiGateway:
    """Тонкий шлюз: маршрутизация + cross-cutting concerns.
    НЕ содержит бизнес-логики сервисов - только периметр."""

    routes: dict[str, callable] = field(default_factory=dict)
    valid_tokens: set[str] = field(default_factory=set)
    rate_limit_per_client: int = 3
    _request_counts: dict[str, int] = field(default_factory=dict)

    def register_route(self, prefix: str, handler) -> None:
        self.routes[prefix] = handler

    def _authenticate(self, token: str) -> None:
        if token not in self.valid_tokens:
            raise Unauthorized(f"invalid token: {token!r}")

    def _check_rate_limit(self, client_id: str) -> None:
        count = self._request_counts.get(client_id, 0)
        if count >= self.rate_limit_per_client:
            raise RateLimited(f"client {client_id!r} exceeded rate limit")
        self._request_counts[client_id] = count + 1

    def _route(self, path: str):
        for prefix, handler in self.routes.items():
            if path.startswith(prefix):
                return handler
        raise NotFound(f"no route for path: {path!r}")

    def handle(self, client_id: str, token: str, path: str) -> str:
        # Порядок cross-cutting concerns: сначала auth (не тратить квоту
        # rate limit на неавторизованных), затем rate limit, затем routing.
        self._authenticate(token)
        self._check_rate_limit(client_id)
        handler = self._route(path)
        return handler(path)


def main() -> None:
    print("--- Пример: минимальный API Gateway ---")

    gateway = ApiGateway(rate_limit_per_client=3)
    gateway.valid_tokens = {"token-client-a", "token-client-b"}
    gateway.register_route("/orders", orders_service)
    gateway.register_route("/users", users_service)

    # 1. Успешная маршрутизация к разным сервисам.
    print(gateway.handle("client-a", "token-client-a", "/orders/1"))
    print(gateway.handle("client-a", "token-client-a", "/users/42"))

    # 2. Неверный токен - шлюз отклоняет запрос, не дав ему дойти до сервиса.
    try:
        gateway.handle("client-a", "wrong-token", "/orders/1")
        raised = False
    except Unauthorized as exc:
        raised = True
        print(f"Отклонено на периметре: {exc}")
    assert raised, "неверный токен должен быть отклонён шлюзом"

    # 3. Неизвестный путь - маршрут не найден (отдельный клиент, чтобы не
    # расходовать квоту rate limit client-a для следующей проверки).
    try:
        gateway.handle("client-probe", "token-client-a", "/billing/1")
        raised = False
    except NotFound as exc:
        raised = True
        print(f"Маршрут не найден: {exc}")
    assert raised

    # 4. Rate limit: client-b уже израсходовал 3 запроса (лимит), 4-й отклонён.
    for i in range(3):
        gateway.handle("client-b", "token-client-b", "/orders/99")
    try:
        gateway.handle("client-b", "token-client-b", "/orders/99")
        raised = False
    except RateLimited as exc:
        raised = True
        print(f"Rate limit сработал: {exc}")
    assert raised, "4-й запрос client-b должен быть отклонён по rate limit"

    # client-a при этом не пострадал от лимита client-b - лимиты независимы.
    result = gateway.handle("client-a", "token-client-a", "/orders/2")
    assert "orders-service" in result

    print(
        "\nВывод: шлюз проверяет аутентификацию и лимиты один раз на "
        "периметре и маршрутизирует к нужному сервису - сами сервисы "
        "orders_service/users_service ничего не знают ни про токены, "
        "ни про лимиты, ни про существование друг друга."
    )


if __name__ == "__main__":
    main()

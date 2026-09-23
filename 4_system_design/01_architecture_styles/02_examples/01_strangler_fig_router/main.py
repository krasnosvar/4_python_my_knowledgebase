"""
Пример 01: маршрутизатор в стиле strangler fig.

Идея: перед "монолитом" ставится роутер с таблицей маршрутов вида
{префикс пути -> обработчик}. Изначально все запросы уходят в монолит.
По мере миграции для отдельных префиксов регистрируется новый сервис,
и трафик по этому префиксу начинает идти туда, а остальное — по-прежнему
в монолит. Ни клиент, ни остальной код не знают, что часть путей уже
обслуживается новым сервисом.

Демонстрирует: три "этапа миграции" одного и того же набора запросов —
до выноса модуля, после выноса billing, после выноса billing и profile —
и то, как меняется распределение обработчиков без изменения клиента.

Запуск: python3 ./02_examples/01_strangler_fig_router/main.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Router:
    """Роутер strangler fig: префикс пути -> имя обработчика."""

    default_handler: str
    routes: dict[str, str] = field(default_factory=dict)

    def register(self, prefix: str, handler: str) -> None:
        """Выносит обработку путей с данным префиксом в новый сервис."""
        self.routes[prefix] = handler

    def route(self, path: str) -> str:
        """Возвращает имя обработчика для пути: самый длинный совпавший
        префикс, либо монолит по умолчанию."""
        best_prefix = ""
        best_handler = self.default_handler
        for prefix, handler in self.routes.items():
            if path.startswith(prefix) and len(prefix) > len(best_prefix):
                best_prefix = prefix
                best_handler = handler
        return best_handler


def run_requests(router: Router, paths: list[str]) -> dict[str, int]:
    """Прогоняет список путей через роутер, считает запросы на обработчик."""
    counts: dict[str, int] = {}
    for path in paths:
        handler = router.route(path)
        counts[handler] = counts.get(handler, 0) + 1
    return counts


def main() -> None:
    print("--- Пример strangler fig router ---")

    requests = [
        "/billing/invoice/1",
        "/billing/invoice/2",
        "/profile/42",
        "/orders/7",
        "/billing/refund/9",
        "/profile/43",
        "/orders/8",
    ]

    # Этап 1: монолит обслуживает всё.
    router = Router(default_handler="monolith")
    stage1 = run_requests(router, requests)
    print("Этап 1 (монолит целиком):        ", stage1)

    # Этап 2: вынесли billing в новый сервис.
    router.register("/billing", "billing_service")
    stage2 = run_requests(router, requests)
    print("Этап 2 (+ billing_service):      ", stage2)

    # Этап 3: вынесли ещё и profile; монолит обслуживает только orders.
    router.register("/profile", "profile_service")
    stage3 = run_requests(router, requests)
    print("Этап 3 (+ profile_service):      ", stage3)

    assert stage1["monolith"] == len(requests)
    assert stage3["monolith"] == 2  # остались только /orders/*
    assert stage3.get("billing_service") == 3
    assert stage3.get("profile_service") == 2

    print(
        "\nКлиент и остальной код ни разу не изменились — менялась только "
        "таблица маршрутов роутера. Монолит с каждым этапом обслуживает "
        "меньше путей, пока в итоге не останется пустым и его можно будет "
        "выключить."
    )


if __name__ == "__main__":
    main()

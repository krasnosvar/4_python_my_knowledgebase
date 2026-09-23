"""
Пример 02: синхронная цепочка вызовов A -> B -> C -> D без защиты.

Симулирует типичный признак распределённого монолита: сервис A синхронно
вызывает B, тот синхронно вызывает C, тот синхронно вызывает D. Каждый
"сервис" — просто функция с искусственной задержкой и шансом отказа.
Нет таймаутов и нет отдельной обработки отказа — вызывающий просто
пробрасывает исключение выше. Показывает: (1) суммарную задержку всей
цепочки = сумма задержек всех звеньев, (2) как единичный отказ в самом
нижнем звене (D) рушит весь запрос сверху донизу, хотя A, B и C были
полностью исправны.

Запуск: python3 ./02_examples/02_distributed_monolith_chain/main.py
"""

from __future__ import annotations

import time


class DownstreamError(Exception):
    """Ошибка нижестоящего сервиса в цепочке."""


def service_d(fail: bool) -> str:
    time.sleep(0.05)
    if fail:
        raise DownstreamError("service_d: база данных недоступна")
    return "d-ok"


def service_c(fail_d: bool) -> str:
    time.sleep(0.05)
    result = service_d(fail_d)  # синхронный вызов вниз по цепочке, без таймаута
    return f"c({result})"


def service_b(fail_d: bool) -> str:
    time.sleep(0.05)
    result = service_c(fail_d)  # тоже синхронно и без защиты
    return f"b({result})"


def service_a(fail_d: bool) -> str:
    time.sleep(0.05)
    result = service_b(fail_d)  # весь путь запроса — один синхронный стек
    return f"a({result})"


def main() -> None:
    print("--- Пример: синхронная цепочка A -> B -> C -> D ---")

    # Счастливый путь: все звенья исправны.
    start = time.monotonic()
    ok_result = service_a(fail_d=False)
    took_ok = time.monotonic() - start
    print(f"Успех: {ok_result}, суммарная задержка ~{took_ok*1000:.0f} мс "
          f"(4 звена по ~50 мс друг за другом)")

    # D отказал: A, B и C были полностью исправны, но весь запрос падает,
    # потому что вызовы синхронные и нет ни таймаута, ни деградации.
    start = time.monotonic()
    try:
        service_a(fail_d=True)
        crashed = False
    except DownstreamError as exc:
        crashed = True
        took_fail = time.monotonic() - start
        print(f"Отказ: {exc!r} после ~{took_fail*1000:.0f} мс — "
              f"A и B полностью исправны, но клиент получает ошибку")

    assert crashed, "ожидался DownstreamError из-за отказа service_d"

    print(
        "\nВывод: длинная синхронная цепочка без таймаутов и без "
        "деградации делает всю систему настолько же надёжной, насколько "
        "надёжно самое слабое звено, и настолько же медленной, насколько "
        "медленна сумма всех звеньев. Это одна из причин, почему такие "
        "цепочки — маркер распределённого монолита, а не здоровой "
        "микросервисной архитектуры."
    )


if __name__ == "__main__":
    main()

"""Декоратор retry с backoff + контекст-менеджер на классе для "соединения"."""

from __future__ import annotations

import random
import time
from functools import wraps


def retry(times: int, delay: float = 0.1, backoff: float = 2.0):
    """Фабрика декораторов: повторяет вызов до `times` раз с растущей паузой между попытками."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exc: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001 - демонстрационный retry
                    last_exc = exc
                    print(f"  попытка {attempt}/{times} не удалась: {exc}")
                    if attempt < times:
                        time.sleep(current_delay)
                        current_delay *= backoff
            raise last_exc

        return wrapper

    return decorator


_flaky_calls = 0


@retry(times=5, delay=0.01)
def flaky_operation() -> str:
    global _flaky_calls
    _flaky_calls += 1
    if _flaky_calls < 3:
        raise ConnectionError("сервис временно недоступен")
    return "успех"


class ManagedConnection:
    """Контекст-менеджер на классе: имитирует захват/освобождение соединения."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_open = False

    def __enter__(self) -> "ManagedConnection":
        self.is_open = True
        print(f"Соединение '{self.name}' открыто")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.is_open = False
        print(f"Соединение '{self.name}' закрыто (было исключение: {exc_type is not None})")
        return False  # исключение не подавляем, пусть летит дальше

    def query(self, sql: str) -> str:
        if not self.is_open:
            raise RuntimeError("соединение закрыто")
        return f"результат для: {sql}"


if __name__ == "__main__":
    print("--- retry ---")
    print("Результат:", flaky_operation())

    print("\n--- контекст-менеджер: штатное завершение ---")
    with ManagedConnection("primary-db") as conn:
        print(conn.query("SELECT 1"))

    print("\n--- контекст-менеджер: завершение с исключением ---")
    try:
        with ManagedConnection("primary-db") as conn:
            raise ValueError("что-то пошло не так внутри блока with")
    except ValueError as exc:
        print(f"Исключение поймано снаружи with: {exc}")

    random.seed(0)  # для воспроизводимости, если бы использовался random где-то ещё

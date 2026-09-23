"""Ручная мемоизация через замыкание, логирующий декоратор и compose-пайплайн."""

from __future__ import annotations

import time
from functools import reduce, wraps


def memoize(func):
    """Мемоизация вручную через замыкание, без functools.lru_cache — чтобы показать механизм."""
    cache: dict[tuple, object] = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"  [cache hit] {func.__name__}{args}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache  # доступ к внутреннему состоянию для отладки/тестов
    return wrapper


@memoize
def expensive_square(n: int) -> int:
    time.sleep(0.05)  # имитация дорогого вычисления
    return n * n


def log_calls(func):
    """Логирующий декоратор, сохраняющий метаданные оборачиваемой функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  вызов {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} -> {result!r}")
        return result

    return wrapper


@log_calls
def normalize_price(price: float, currency: str = "USD") -> str:
    """Форматирует цену с округлением до двух знаков."""
    return f"{price:.2f} {currency}"


def compose(*functions):
    """Собирает пайплайн: compose(f, g, h)(x) == f(g(h(x)))."""
    return reduce(lambda f, g: lambda x: f(g(x)), functions)


if __name__ == "__main__":
    print("--- мемоизация ---")
    print("Первый вызов:", expensive_square(5))
    print("Повторный вызов (из кэша):", expensive_square(5))
    print("Кэш содержит:", expensive_square.cache)

    print("\n--- логирующий декоратор ---")
    normalize_price(19.999, currency="EUR")
    print("Метаданные сохранены:", normalize_price.__name__, "-", normalize_price.__doc__)

    print("\n--- compose пайплайн ---")
    pipeline = compose(str.upper, str.strip, lambda s: s.replace("_", " "))
    print(pipeline("  hello_world  "))

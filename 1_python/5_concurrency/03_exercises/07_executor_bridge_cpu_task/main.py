"""
Задача: внутри asyncio-приложения выполнить тяжёлое CPU-вычисление, не
блокируя event loop, используя loop.run_in_executor с ProcessPoolExecutor.
Параллельно event loop должен продолжать "тикать" (доказательство, что он
не заблокирован).

Запусти: python main.py
"""
from __future__ import annotations

import asyncio
from concurrent.futures import ProcessPoolExecutor


def cpu_heavy(n: int) -> int:
    return sum(i * i for i in range(n))


async def run_cpu_task_without_blocking(n: int) -> tuple[int, int]:
    """
    TODO:
      1. Получить loop = asyncio.get_running_loop().
      2. Запустить cpu_heavy(n) в ProcessPoolExecutor через run_in_executor
         как одну задачу (не await сразу, а создать awaitable).
      3. Параллельно вести счётчик "тиков" event loop: в цикле 10 раз делать
         await asyncio.sleep(0.01) и увеличивать счётчик, пока cpu-задача
         считается.
      4. Дождаться результата cpu-задачи через gather с задачей-тикером.
      5. Вернуть (результат_cpu_heavy, число_тиков).

    Подсказка: используйте asyncio.gather(cpu_future, ticker_coro()).
    """
    raise NotImplementedError


async def main() -> None:
    checks_passed = 0
    total_checks = 2

    result, ticks = await run_cpu_task_without_blocking(3_000_000)

    expected = sum(i * i for i in range(3_000_000))
    assert result == expected
    checks_passed += 1
    assert ticks == 10, "event loop должен был успеть сделать все тики, пока считался CPU-таск"
    checks_passed += 1

    print(f"Результат: {result}, тиков event loop: {ticks}")
    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    asyncio.run(main())

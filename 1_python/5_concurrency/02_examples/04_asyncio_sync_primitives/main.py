"""
asyncio.Lock, Semaphore, Event, Queue на практике.

Запуск: python main.py
"""
from __future__ import annotations

import asyncio


async def demo_lock() -> None:
    print("--- Lock: защита shared state с гонкой check-then-act ---")
    balance = {"amount": 100}
    lock = asyncio.Lock()

    async def withdraw(who: str, amount: int) -> None:
        async with lock:
            if balance["amount"] >= amount:
                await asyncio.sleep(0.01)  # имитация похода в БД
                balance["amount"] -= amount
                print(f"{who}: списано {amount}, остаток {balance['amount']}")
            else:
                print(f"{who}: недостаточно средств")

    await asyncio.gather(withdraw("Alice", 80), withdraw("Bob", 80))
    assert balance["amount"] >= 0, "баланс не должен уходить в минус при защите Lock'ом"


async def demo_semaphore() -> None:
    print("\n--- Semaphore: не больше 2 одновременных 'подключений' ---")
    sem = asyncio.Semaphore(2)
    active = 0
    max_active = 0

    async def connect(n: int) -> None:
        nonlocal active, max_active
        async with sem:
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.1)
            active -= 1

    await asyncio.gather(*(connect(i) for i in range(6)))
    print(f"Максимум одновременных: {max_active}")
    assert max_active <= 2


async def demo_event() -> None:
    print("\n--- Event: разбудить всех ожидающих одним сигналом ---")
    ready = asyncio.Event()

    async def waiter(n: int) -> None:
        await ready.wait()
        print(f"waiter {n} проснулся")

    waiters = [asyncio.create_task(waiter(i)) for i in range(3)]
    await asyncio.sleep(0.1)
    ready.set()
    await asyncio.gather(*waiters)


async def demo_queue() -> None:
    print("\n--- Queue: producer/consumer ---")
    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=5)
    processed = []

    async def producer() -> None:
        for i in range(10):
            await queue.put(i)
        await queue.put(None)  # sentinel

    async def consumer() -> None:
        while (item := await queue.get()) is not None:
            processed.append(item)
            queue.task_done()

    await asyncio.gather(producer(), consumer())
    assert processed == list(range(10))
    print(f"Обработано: {processed}")


async def main() -> None:
    await demo_lock()
    await demo_semaphore()
    await demo_event()
    await demo_queue()


if __name__ == "__main__":
    asyncio.run(main())

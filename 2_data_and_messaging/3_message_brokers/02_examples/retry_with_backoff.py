"""Generic retry-with-exponential-backoff helper.

Используется в rabbitmq/consumer.py перед тем, как окончательно признать
сообщение необрабатываемым и отправить его в DLQ (см.
01_theory/07_dlq_and_retry.md - "Dead Letter Queue и retry с backoff").

Идея: вместо того, чтобы либо мгновенно ретраить в цикле (busy loop,
блокирует consumer и не решает проблему временной недоступности зависимости),
либо сразу сдаваться после первой ошибки, даём обработчику несколько попыток
с растущей паузой между ними. Если все попытки провалились - вызывающий код
сам решает, что делать дальше (в нашем случае - nack с requeue=False, что
при настроенном DLX отправит сообщение в DLQ).

Важно: backoff здесь - это sleep именно вокруг ОДНОЙ обработки одного
сообщения, а не блокировка всей очереди. Пока идёт backoff для одного
сообщения, другие сообщения из очереди/партиции не читаются этим consumer'ом -
поэтому в производственных системах retry с задержкой чаще выносят в отдельную
retry-очередь/топик (см. теорию), а не делают time.sleep() прямо в обработчике.
Здесь - простой вариант "sleep на месте" для наглядности внутри одного файла.
"""
from __future__ import annotations

import functools
import logging
import random
import time
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryExhaustedError(Exception):
    """Все попытки обработки исчерпаны без успеха."""

    def __init__(self, attempts: int, last_error: Exception):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            f"обработка не удалась после {attempts} попыток: {last_error!r}"
        )


def retry_with_backoff(
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: float = 0.3,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор: повторяет вызов функции с экспоненциальной задержкой.

    Задержка перед попыткой N (начиная с N=2): min(base_delay * 2**(N-2), max_delay),
    плюс случайный джиттер +-jitter*задержка - чтобы много упавших одновременно
    consumer'ов не били по внешней зависимости синхронной волной ровно
    в одно и то же время.

    Если после max_attempts попыток функция так и не выполнилась успешно -
    поднимается RetryExhaustedError с последней исходной ошибкой внутри.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_error: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as exc:
                    last_error = exc
                    if attempt == max_attempts:
                        break

                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    delay += random.uniform(-jitter, jitter) * delay
                    delay = max(delay, 0.0)

                    logger.warning(
                        "попытка %d/%d для %s провалилась (%s), retry через %.2fs",
                        attempt,
                        max_attempts,
                        func.__name__,
                        exc,
                        delay,
                    )
                    time.sleep(delay)

            assert last_error is not None
            raise RetryExhaustedError(max_attempts, last_error) from last_error

        return wrapper

    return decorator

import logging
import random

from celery_app import app

logger = logging.getLogger(__name__)


class ExternalServiceError(ConnectionError):
    """Имитация ошибки ненадёжного внешнего сервиса."""


# TODO: добавьте в декоратор @app.task параметры:
#   - bind=True (нужен доступ к self для логирования номера попытки)
#   - autoretry_for=(ExternalServiceError,)
#   - retry_backoff=True
#   - retry_backoff_max=<разумное значение в секундах>
#   - max_retries=5
@app.task
def unreliable_call(payload: str) -> str:
    if random.random() < 0.5:
        raise ExternalServiceError(f"внешний сервис недоступен для payload={payload!r}")
    return f"processed:{payload}"


# TODO: если задача так и не смогла выполниться после всех retry, Celery
# в итоге позволит исключению "провалиться" окончательно. Добавьте обработку
# финальной неудачи: либо через параметр on_failure у задачи (переопределив
# метод класса Task), либо оборачивая тело функции в try/except и вызывая
# self.retry(...) вручную в блоке except, а после исчерпания попыток —
# logger.error("unreliable_call окончательно провалилась для payload=%s", payload)

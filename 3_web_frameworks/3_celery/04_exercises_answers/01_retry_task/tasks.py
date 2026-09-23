import logging
import random

from celery_app import app

logger = logging.getLogger(__name__)


class ExternalServiceError(ConnectionError):
    """Имитация ошибки ненадёжного внешнего сервиса."""


@app.task(
    bind=True,
    autoretry_for=(ExternalServiceError,),
    retry_backoff=True,
    retry_backoff_max=30,
    max_retries=5,
)
def unreliable_call(self, payload: str) -> str:
    try:
        if random.random() < 0.5:
            raise ExternalServiceError(
                f"внешний сервис недоступен для payload={payload!r}"
            )
        return f"processed:{payload}"
    except ExternalServiceError:
        if self.request.retries >= self.max_retries:
            logger.error(
                "unreliable_call окончательно провалилась для payload=%s "
                "после %s попыток",
                payload,
                self.request.retries + 1,
            )
        raise

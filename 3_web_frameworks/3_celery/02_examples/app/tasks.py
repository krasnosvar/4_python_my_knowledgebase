import logging
import time

from app.celery_app import app

logger = logging.getLogger(__name__)


@app.task
def add(x: int, y: int) -> int:
    return x + y


@app.task
def send_report(user_id: int) -> str:
    # имитация тяжёлой работы: генерация отчёта, рендеринг, отправка письма
    logger.info("Начинаю генерацию отчёта для user_id=%s", user_id)
    time.sleep(5)
    logger.info("Отчёт для user_id=%s готов и отправлен", user_id)
    return f"report-for-user-{user_id}-sent"


@app.task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    retry_backoff_max=30,
    max_retries=3,
)
def flaky_external_call(self, payload: str) -> str:
    # демонстрация встроенного retry: Celery сам перехватит ConnectionError
    # и перепланирует задачу с экспоненциальной задержкой
    logger.info(
        "Попытка %s/%s вызвать внешний сервис с payload=%r",
        self.request.retries + 1,
        self.max_retries + 1,
        payload,
    )
    return f"processed:{payload}"

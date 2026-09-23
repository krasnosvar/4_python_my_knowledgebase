import logging

from celery_app import app

logger = logging.getLogger(__name__)


@app.task
def cleanup_tmp_files() -> None:
    logger.info("Очистка временных файлов выполнена")


@app.task
def daily_digest() -> None:
    logger.info("Ежедневный дайджест отправлен")

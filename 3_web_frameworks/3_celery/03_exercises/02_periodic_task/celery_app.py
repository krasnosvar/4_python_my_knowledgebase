import os

from celery import Celery

BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

app = Celery(
    "periodic_exercise",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["tasks"],
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# TODO: заполните app.conf.beat_schedule двумя записями:
#   1. "cleanup-every-15-seconds": запускает tasks.cleanup_tmp_files
#      каждые 15 секунд (schedule=15.0)
#   2. "daily-digest-at-9am": запускает tasks.daily_digest
#      каждый день в 09:00 (schedule=crontab(hour=9, minute=0))
# Не забудьте импортировать crontab: from celery.schedules import crontab

import os

from celery import Celery
from celery.schedules import crontab

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

app.conf.beat_schedule = {
    "cleanup-every-15-seconds": {
        "task": "tasks.cleanup_tmp_files",
        "schedule": 15.0,
    },
    "daily-digest-at-9am": {
        "task": "tasks.daily_digest",
        "schedule": crontab(hour=9, minute=0),
    },
}

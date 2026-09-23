См. `../../03_exercises/02_periodic_task/README.md` — шаги проверки те же
самые, здесь только код решения.

## Что сделано

`app.conf.beat_schedule` заполнен двумя записями:

- `cleanup-every-15-seconds` — запускает `tasks.cleanup_tmp_files` каждые
  15 секунд (`schedule=15.0`, простой числовой интервал);
- `daily-digest-at-9am` — запускает `tasks.daily_digest` ежедневно в 09:00
  через `crontab(hour=9, minute=0)`.

`crontab` импортирован из `celery.schedules`.

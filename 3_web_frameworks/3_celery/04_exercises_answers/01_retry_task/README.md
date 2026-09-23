См. `../../03_exercises/01_retry_task/README.md` — шаги проверки те же самые,
здесь только код решения.

## Что сделано

- `@app.task` дополнен `bind=True`, `autoretry_for=(ExternalServiceError,)`,
  `retry_backoff=True`, `retry_backoff_max=30`, `max_retries=5` — Celery сам
  перехватывает `ExternalServiceError` и планирует повтор с экспоненциальной
  задержкой (ограниченной 30 секундами), не более 5 раз.
- Внутри задачи добавлен `try/except`, который на последней исчерпанной
  попытке (`self.request.retries >= self.max_retries`) логирует финальную
  ошибку через `logger.error(...)` перед тем, как исключение уйдёт наружу
  окончательно (после `autoretry_for` Celery ре-рейзит исключение, если
  попытки закончились, — поэтому `raise` в конце обязателен).

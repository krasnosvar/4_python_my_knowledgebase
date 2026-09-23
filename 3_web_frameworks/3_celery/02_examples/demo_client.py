"""
Скрипт для отправки задач в брокер и получения результата.

Запускать с хоста, где Redis из docker-compose проброшен на localhost:6379
(порт "6379:6379" уже указан в docker-compose.yml), поэтому переменные
окружения можно не переопределять — celery_app.py по умолчанию использует
redis://localhost:6379/0.
"""

from app.tasks import add, send_report

if __name__ == "__main__":
    result = add.delay(2, 3)
    print("add task id:", result.id)
    print("add result:", result.get(timeout=10))

    report_result = send_report.delay(user_id=42)
    print("send_report task id:", report_result.id)
    print("статус сразу после отправки:", report_result.status)
    print("send_report result:", report_result.get(timeout=15))

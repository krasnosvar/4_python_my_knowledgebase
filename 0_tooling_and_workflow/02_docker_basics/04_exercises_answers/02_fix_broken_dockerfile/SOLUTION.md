# Решение: 02_fix_broken_dockerfile

Исходный (сломанный) Dockerfile:

```dockerfile
COPY app/app.py .      # неверно: файл называется main.py
...
EXPOSE 8000              # неверно: приложение слушает 5000
CMD ["python", "app.py"]  # неверно: тот же файл, что и выше
```

Исправленный вариант:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py .

EXPOSE 5000

CMD ["python", "main.py"]
```

Первая ошибка (`app.py` вместо `main.py`) ломала сам `docker build` — `COPY`
не может скопировать несуществующий файл, сборка падает с
`"app/app.py": not found`. Вторая (несоответствие `EXPOSE`) не ломает
работу приложения технически (это просто документация), но вводит в
заблуждение любого, кто запускает образ и пробрасывает порт по описанию из
Dockerfile.

# Минимальный однослойный (по стадиям) образ для FastAPI-приложения.
# Смотри Dockerfile.multistage для варианта с отдельной стадией сборки.

FROM python:3.12-slim

WORKDIR /app

# Сначала зависимости — этот слой пересоберётся только при изменении requirements.txt,
# а не при каждой правке кода приложения (см. 01_theory/02_dockerfile_basics.md).
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

# exec form: uvicorn становится PID 1 и корректно получает SIGTERM при docker stop.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

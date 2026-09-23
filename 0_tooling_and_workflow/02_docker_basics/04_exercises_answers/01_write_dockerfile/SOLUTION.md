# Решение: 01_write_dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/main.py .

EXPOSE 8080

CMD ["python", "main.py"]
```

Важно, что `CMD` записан в **exec-форме** (JSON-массивом), а не как строка
`CMD python main.py` — в exec-форме `python` становится процессом с PID 1 и
корректно получает `SIGTERM` при `docker stop` (см.
`../../01_theory/02_dockerfile_basics.md`, раздел про shell/exec form).

```bash
docker build -t exercise-01 .
docker run --rm -d -p 8080:8080 --name exercise-01 exercise-01
curl http://localhost:8080/
docker stop exercise-01
```

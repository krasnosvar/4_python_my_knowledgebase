# Решение: 03_compose_with_cache

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - CACHE_HOST=cache
      - CACHE_PORT=6379
    depends_on:
      - cache

  cache:
    image: redis:7-alpine
    volumes:
      - cache-data:/data

volumes:
  cache-data:
```

Ключевые моменты:

- Сервис называется именно `cache` — приложение по умолчанию обращается к
  хосту `cache` (переменная `CACHE_HOST`), а compose резолвит имена
  сервисов внутри общей сети автоматически, без ручной настройки DNS.
- У `cache` нет секции `ports` — порт `6379` доступен только внутри сети
  compose, что и требовалось: наружу светить Redis незачем.
- `depends_on: [cache]` гарантирует только порядок запуска контейнеров, не
  готовность Redis принимать соединения — в данном случае Redis поднимается
  быстро, и `app` начинает опрашивать `/health` уже после того, как Redis
  готов; для более медленных сервисов стоит добавлять `healthcheck`.
- `cache-data` — именованный volume для персистентности данных Redis между
  перезапусками контейнера (не обязателен для проверки `/health`, но
  правильная практика для реального кэша/БД).

```bash
docker compose up -d --build
curl http://localhost:8080/health   # "cache reachable"
docker compose down -v
```

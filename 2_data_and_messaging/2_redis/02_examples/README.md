# Примеры: Redis как кеш из Python (redis-py)

Рабочие скрипты поверх реального Redis, поднятого через Docker Compose.
Каждый скрипт самодостаточен, печатает происходящее в stdout и его можно
запускать многократно.

## Запуск

```bash
docker compose up -d
docker compose ps          # дождаться healthy у redis

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Дальше запускайте скрипты по одному:

```bash
python 01_data_structures.py
python 02_ttl_and_eviction.py
python 03_cache_aside_pattern.py
python 04_rate_limiting.py
```

Остановить и убрать контейнер (данные в volume сохранятся):

```bash
docker compose down
```

Полностью стереть данные вместе с volume:

```bash
docker compose down -v
```

## Что делает каждый скрипт

- **`01_data_structures.py`** — практика по всем пяти структурам из теории:
  string (счётчик просмотров, сессия с TTL), hash (объект пользователя),
  list (лента последних поисков + простая FIFO-очередь), set (теги статьи +
  пересечение множеств), sorted set (лидерборд с `ZREVRANGE`/`ZINCRBY`).
- **`02_ttl_and_eviction.py`** — базовые операции с TTL (`SET ... EX`,
  `TTL`, `PERSIST`, `EXPIRE`), а затем честная демонстрация вытеснения:
  скрипт временно выставляет маленький `maxmemory` и политику
  `allkeys-lru`, заливает больше данных, чем помещается, и показывает по
  `INFO stats`/`SCAN`, что часть ключей была вытеснена, а не привела к
  ошибке записи. В конце конфигурация сервера возвращается к исходной.
- **`03_cache_aside_pattern.py`** — cache-aside на функции `get_user()`:
  имитация медленной БД через `time.sleep`, замер времени холодного и
  тёплого вызова, и инвалидация кеша через `DEL` при обновлении данных
  (delete-on-write).
- **`04_rate_limiting.py`** — `fixed_window_allow` (INCR + EXPIRE) и
  `sliding_window_allow` (sorted set с timestamp'ами), плюс сценарий,
  воспроизводящий всплеск на границе fixed-window окна и показывающий,
  что sliding window от него не страдает.

## Примечание про `02_ttl_and_eviction.py`

Этот скрипт временно меняет `maxmemory`/`maxmemory-policy` **на уровне
всего Redis-сервера**, а не только для своих ключей. Для учебного
контейнера из этого раздела это безопасно, но если вы запускаете его
параллельно с другими скриптами на этом же инстансе — на несколько секунд
они тоже окажутся под ограничением памяти. Скрипт восстанавливает исходную
конфигурацию в блоке `finally`, даже если демонстрация упадёт с ошибкой.

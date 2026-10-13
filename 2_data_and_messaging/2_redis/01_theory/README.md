# Redis: in-memory кеш для ускорения ответов

Этот раздел рассматривает Redis узко и прагматично: как **in-memory кеш**,
который стоит перед медленным источником данных (обычно реляционной БД) и
ускоряет типичные операции чтения в веб-приложении на Python. Redis умеет
гораздо больше (pub/sub, streams, модули типа RediSearch/RedisJSON,
использование как основной БД в нишевых случаях), но это не тема данного
раздела — pub/sub и очереди сообщений затронуты только вскользь, потому что
полноценный разбор брокеров сообщений (Kafka/RabbitMQ) — отдельный модуль
базы знаний.

Уроки читаются по порядку:

1. [01_what_is_redis.md](./01_what_is_redis.md) — почему Redis быстрый
   (RAM, один поток, RDB/AOF) и когда его не использовать.
2. [02_data_structures.md](./02_data_structures.md) — String, Hash, List,
   Set, Sorted Set и типичные применения.
3. [03_ttl_expiration_eviction.md](./03_ttl_expiration_eviction.md) — как
   истекают ключи и что Redis вытесняет при нехватке памяти.
4. [04_caching_patterns.md](./04_caching_patterns.md) — cache-aside,
   write-through, write-behind.
5. [05_cache_invalidation.md](./05_cache_invalidation.md) — стратегии
   инвалидации и гонка между записью в БД и обновлением кеша.
6. [06_rate_limiting.md](./06_rate_limiting.md) — fixed window и sliding
   window.
7. [07_redis_as_queue.md](./07_redis_as_queue.md) — Redis как простая
   очередь.
8. [08_pubsub.md](./08_pubsub.md) — Pub/Sub коротко.

Как проходить всю тему (стенд, примеры, упражнения) — в
[README темы](../README.md).

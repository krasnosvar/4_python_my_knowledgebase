"""Упражнение 2 (Kafka) - решение: manual commit ТОЛЬКО после успешной обработки.

Почему именно так (а не auto-commit) - ответ на "главное" TODO упражнения:

Если бы был включён enable_auto_commit=True (коммит по таймеру, например
раз в 5 секунд, независимо от результата обработки), сценарий с падением на
number=5 выглядел бы так:
  1. Consumer читает number=0..4, успешно обрабатывает.
  2. Consumer читает number=5, process_message() бросает исключение.
  3. Но auto-commit не спрашивает, обработано ли сообщение - он коммитит
     ТЕКУЩУЮ ПОЗИЦИЮ (offset уже прочитанного, а не обработанного сообщения)
     по таймеру. Если этот таймер сработает после того, как number=5 был
     прочитан (а он читается consumer'ом даже при провале обработки), offset
     будет закоммичен ЗА number=5, хотя оно так и не было обработано успешно.
  4. При перезапуске consumer продолжит с number=6 - number=5 потерян
     БЕЗВОЗВРАТНО, и никакого следа этой потери в логах может не остаться.

Второй, менее очевидный нюанс (важно понять, а не просто выучить): committed
offset в Kafka - это ЕДИНЫЙ курсор-число на партицию ("всё, что до этой
позиции, обработано"), а НЕ отметка по каждому сообщению отдельно. Из этого
следует, что даже с manual commit нельзя просто "пропустить" провалившееся
сообщение и продолжить читать со следующего, коммитя успешные - коммит
следующего успешного сообщения молча сдвинет курсор и МИМО провалившегося
тоже. Поэтому при ошибке этот consumer не идёт дальше по циклу (не commit
и не continue), а полностью останавливается (return) - offset остаётся
на number=4, и следующий запуск consumer'а начнёт именно с number=5.

Это же само по себе иллюстрирует ту самую head-of-line-blocking проблему,
которая описана в 01_theory/README.md, раздел 4: "ядовитое" сообщение,
которое систематически не обрабатывается, останавливает весь дальнейший
прогресс по партиции. Решение - паттерн retry-топик + DLQ-топик (тоже раздел 4)
вместо простой остановки; для целей ЭТОГО упражнения (только про manual
commit) остановка - самая простая и честная демонстрация гарантии.
"""
from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ex2-consumer")

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "manual-commit-demo"
GROUP_ID = "ex2-manual-commit-group"


def process_message(payload: dict) -> None:
    if payload["number"] == 5:
        raise RuntimeError("временная ошибка обработки (например, БД недоступна)")
    logger.info("обработано сообщение number=%s", payload["number"])


async def consume_with_manual_commit() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=False,  # коммитим только вручную, см. docstring выше
    )
    await consumer.start()
    try:
        async for message in consumer:
            try:
                process_message(message.value)
            except Exception:
                logger.exception(
                    "ошибка обработки number=%s (offset=%d) - offset НЕ закоммичен, "
                    "останавливаемся, чтобы не закоммитить мимо этого сообщения",
                    message.value.get("number"),
                    message.offset,
                )
                # Не continue: если продолжить и позже закоммитить более
                # позднее сообщение, курсор сдвинется и мимо этого тоже.
                return

            await consumer.commit()
            logger.info(
                "offset закоммичен: number=%s (offset=%d)",
                message.value["number"],
                message.offset,
            )
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_with_manual_commit())

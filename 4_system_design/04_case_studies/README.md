# Тема 04. Разбор сквозных кейсов на Python (Case Studies)

## О чём эта тема (краткий контекст)

На System Design интервью и архитектурном ревью знания отдельных паттернов
складываются в сквозное проектирование реальной системы: от уточнения
функциональных и нефункциональных требований и расчётов нагрузки (QPS, трафик,
диски) до выбора модели данных, API-контрактов и устранения узких мест при
кратном росте. Два полярных эталонных кейса — система денежных переводов
(доминирует строгая ACID-согласованность, идемпотентность и защита от гонок) и
медиа-галерея (доминирует экстремальный перекос чтения к записи 1000:1,
терабайтные объёмы статики и CPU-bound обработка).

> **Базовая теория и инфраструктурный фундамент (DevOps / SRE):**
> Полный разбор концепции, базовые определения, схемы, алгоритмы и
> платформенные компромиссы вынесены в канонический раздел:
> - [Фреймворк System Design интервью и расчёты нагрузки](../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/01_theory/01_interview_framework_and_estimations.md)
> - [Сквозные кейсы: денежные переводы, медиа-галерея, URL Shortener и лента](../../../5_devops_sre_knowledgebase/14_system_design/07_case_studies_and_interview/01_theory/02_case_studies_transfers_and_media.md)
>
> **Фокус этого урока:** здесь мы не дублируем общую теорию, а разбираем
> исключительно особенности реализации и эксплуатации в экосистеме
> **Python** (рантайм CPython и GIL, память, WSGI/ASGI, стандартная
> библиотека и популярные фреймворки).

## Зачем этот раздел

Здесь мы собираем все темы раздела в код и архитектуру реальных Python-сервисов:
как провести денежный перевод на SQLAlchemy/Django без `float`, без гонок
TOCTOU и без взаимных блокировок (`with_for_update()` с сортировкой ID счетов +
`IdempotencyRecord` + `LedgerEntry` + `OutboxEvent`), и как построить
медиа-пайплайн на FastAPI/Celery/S3, не уронив воркеры по `OOMKilled` на
`await file.read()` и не заблокировав `asyncio` Event Loop ресайзом картинок в
`Pillow`.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — код и таблицы
ключевых решений для переводов и медиа-пайплайна в Python.

## Что нужно знать заранее

- Все три предыдущие темы раздела:
  [01_architecture_styles](../01_architecture_styles/),
  [02_performance_and_scaling](../02_performance_and_scaling/),
  [03_distributed_components](../03_distributed_components/).

## Структура раздела

- **[01_theory/](./01_theory/)** — реализация сквозных кейсов в Python:
  - [01_money_transfers_in_python.md (урок
    01)](./01_theory/01_money_transfers_in_python.md)
    — денежные переводы на Python: минорные единицы (`int`) и `Decimal` вместо
    `float`, защита от Deadlock через сортировку ID перед `with_for_update()`,
    обработка гонок по `Idempotency-Key`, Double-Entry Ledger и Transactional
    Outbox в одной транзакции `AsyncSession`.
  - [02_image_gallery_in_python.md](./01_theory/02_image_gallery_in_python.md)
    — галерея изображений на Python: почему `await file.read()` вызывает OOM в
    воркерах, генерация Presigned URL в `boto3`, потоковое чтение и SHA-256
    дедупликация чанками, вынос `Pillow` / `pyvips` в Celery с защитой от
    Decompression Bomb (`Image.MAX_IMAGE_PIXELS`) и фрагментации памяти
    (`--max-tasks-per-child`).
- **[02_examples/](./02_examples/)** — runnable-примеры на чистом Python:
  - [01_idempotent_transfer](./02_examples/01_idempotent_transfer/main.py) —
    идемпотентный перевод с журналом двойной записи (Double-Entry Bookkeeping).
  - [02_image_pipeline_dedup](./02_examples/02_image_pipeline_dedup/main.py) —
    пайплайн загрузки изображения с разделением метаданных и байтов и
    дедупликацией по SHA-256.
- **[03_exercises/](./03_exercises/)** — сценарии эволюции систем под новыми
  требованиями и кратным ростом нагрузки:
  - [01_transfer_growth](./03_exercises/01_transfer_growth.md) — эволюция
    системы переводов: регулярные платежи, два внешних провайдера и 50-кратный
    рост с эффектом локальности.
  - [02_gallery_growth](./03_exercises/02_gallery_growth.md) — эволюция
    галереи: приватные альбомы, живая лента, 10-кратный пиковый всплеск
    загрузок и счётчик просмотров.
- **[04_exercises_answers/](./04_exercises_answers/)** — разобранные
  рассуждения по тем же сценариям.

## Как проходить

1. Изучите базовую методологию интервью и сквозные кейсы в каноническом разделе
   DevOps (по ссылкам в начале уроков) и прочитайте оба урока в
   [01_theory/](./01_theory/).
2. Запустите и изучите примеры из `02_examples/`:
   ```bash
   python3 ./02_examples/01_idempotent_transfer/main.py
   python3 ./02_examples/02_image_pipeline_dedup/main.py
   ```
3. Проработайте сценарии роста в [03_exercises/](./03_exercises/) письменно,
   затем сверьтесь с [04_exercises_answers/](./04_exercises_answers/).

## Когда двигаться дальше

Когда вы можете самостоятельно провести новый кейс по шагам фреймворка и
написать ключевые узлы его реализации на Python без гонок, блокировок Event
Loop и утечек памяти — раздел пройден; вернитесь к
[оглавлению раздела](../README.md).

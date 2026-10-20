# Python Backend Knowledge Base

## Зачем этот раздел

Учебная база по Python backend-разработке: язык, стандартная библиотека,
конкурентность, базы данных, брокеры сообщений, веб-фреймворки, system design
и профессиональные коммуникативные навыки инженера.

Материалы собраны как практический roadmap: краткая теория, runnable-примеры,
упражнения и решения для самопроверки. Пройдя его, вы сможете писать на Python
backend-сервисы с базой данных, кэшем и очередями, тестировать их и рассуждать
об их архитектуре.

## Что нужно знать заранее

Ничего: база начинается с нуля. Первый шаг — урок
[00_setup](./1_python/1_python_fundamentals/00_setup/): установка Python 3.12+,
терминал, запуск первого скрипта.

> **`python3`, `python` или `py`?** В README и комментариях команды записаны как
> `python3` или `python` — это одна и та же программа, интерпретатор Python 3.
> На Linux и macOS обычно работает только `python3` (`python` может не быть
> или указывать на старый Python 2), на Windows — `python` или `py`. Используйте
> ту команду, которая на вашей системе показывает версию 3.12+ в ответ на
> `--version`; подробнее — в
> [00_setup](./1_python/1_python_fundamentals/00_setup/).
> Внутри активированного виртуального окружения (`.venv`) работают и `python`,
> и `python3`.

## Структура

- [0_tooling_and_workflow](./0_tooling_and_workflow/) — Git и Docker: минимум,
  без которого не обойтись в повседневной работе. Git нужен с самого начала,
  Docker можно отложить до `2_data_and_messaging`.
- [1_python](./1_python/) — Python с нуля: переменные, типы, `if`/`for`/`while`,
  функции — и дальше до идиом языка, ООП, итераторов и генераторов,
  конкурентности (GIL, threading, multiprocessing, asyncio), стандартной
  библиотеки, тестирования, алгоритмов и внутреннего устройства CPython.
- [2_data_and_messaging](./2_data_and_messaging/) — реляционные БД, транзакции
  и индексы, Redis как кэш, Kafka и RabbitMQ как брокеры сообщений.
- [3_web_frameworks](./3_web_frameworks/) — FastAPI, Django ORM, Celery и
  сравнение стеков между собой.
- [4_system_design](./4_system_design/) — архитектурные стили,
  производительность и масштабирование, компоненты распределённых систем,
  разбор кейсов целиком (с привязкой к CPython, ASGI/WSGI, SQLAlchemy и
  `asyncio`).
- [5_engineering_communication](./5_engineering_communication/) —
  профессиональные коммуникативные навыки: как документировать свою работу,
  объяснять сложные вещи разным аудиториям, вести диалог под давлением,
  договариваться об условиях и работать с конфликтами.
- [other](./other/) — окружение и упаковка (venv, зависимости), типизация
  и статический анализ.

## Формат разделов

Большинство тем устроены по одному шаблону:

- `01_theory/` — краткая теория без лишней воды;
- `02_examples/` — рабочие примеры, которые можно запускать;
- `03_exercises/` — упражнения от простого к сложному;
- `04_exercises_answers/` — решения для самопроверки;
- `README.md` — навигация по теме.

Раздел [5_engineering_communication](./5_engineering_communication/) устроен
иначе: вместо кода — `01_theory/` и `02_practice/` с чек-листами и сценариями
для практики.

## Шпаргалки

Уже знакомы с темой и нужен быстрый справочник? У каждой темы есть
`CHEATSHEET.md` — таблицы «задача → синтаксис/команда», «когда что
использовать», типичные ошибки. Подробности — по ссылкам на теорию внутри.

**0. Инструменты**
- [Git](./0_tooling_and_workflow/01_git_essentials/CHEATSHEET.md)
- [Docker и Compose](./0_tooling_and_workflow/02_docker_basics/CHEATSHEET.md)

**1. Python**
- [Основы языка (темы 1.0–1.8)](./1_python/1_python_fundamentals/CHEATSHEET.md)
- [Функции и декораторы](./1_python/2_functions_and_decorators/CHEATSHEET.md)
- [ООП](./1_python/3_oop/CHEATSHEET.md)
- [Итераторы и генераторы](./1_python/4_iterators_generators/CHEATSHEET.md)
- [Конкурентность](./1_python/5_concurrency/CHEATSHEET.md)
- [Стандартная библиотека](./1_python/6_standard_library/CHEATSHEET.md)
- [Тестирование](./1_python/7_testing/CHEATSHEET.md)
- [Алгоритмы и структуры данных](./1_python/8_algorithms_dsa/CHEATSHEET.md)
- [CPython изнутри](./1_python/9_under_the_hood/CHEATSHEET.md)

**2. Данные и сообщения**
- [SQL и реляционные
  БД](./2_data_and_messaging/1_sql_relational_databases/CHEATSHEET.md)
- [Redis](./2_data_and_messaging/2_redis/CHEATSHEET.md)
- [Брокеры сообщений (Kafka,
  RabbitMQ)](./2_data_and_messaging/3_message_brokers/CHEATSHEET.md)

**3. Веб-фреймворки**
- [FastAPI](./3_web_frameworks/1_fastapi/CHEATSHEET.md)
- [Django](./3_web_frameworks/2_django/CHEATSHEET.md)
- [Celery](./3_web_frameworks/3_celery/CHEATSHEET.md)
- [Сравнение стеков: FastAPI vs Django, место
  Celery](./3_web_frameworks/4_stack_comparison/CHEATSHEET.md)

**4. System design**
- [Архитектурные стили](./4_system_design/01_architecture_styles/CHEATSHEET.md)
- [Производительность и
  масштабирование](./4_system_design/02_performance_and_scaling/CHEATSHEET.md)
- [Компоненты распределённых
  систем](./4_system_design/03_distributed_components/CHEATSHEET.md)
- [Разбор кейсов](./4_system_design/04_case_studies/CHEATSHEET.md)

**5. Инженерная коммуникация**
- [Все темы 01–06](./5_engineering_communication/CHEATSHEET.md)

**Дополнительно**
- [Окружения и упаковка (venv, pip,
  Poetry)](./other/01_environments_and_packaging/CHEATSHEET.md)
- [Типизация и статический
  анализ](./other/02_typing_and_static_analysis/CHEATSHEET.md)

## Как проходить

1. Установить Python и освоиться в терминале:
   [00_setup](./1_python/1_python_fundamentals/00_setup/).
2. Пройти Git из [0_tooling_and_workflow](./0_tooling_and_workflow/) — он нужен
   с самого начала, чтобы сохранять свои решения. Docker из того же раздела
   можно отложить до шага 5.
3. Пройти [1_python](./1_python/): основы языка, ООП, конкурентность,
   стандартная библиотека, тестирование и алгоритмы. Docker здесь не нужен.
4. До первого `pip install` (на практике он впервые понадобится в
   `1_python/7_testing`) создать виртуальное окружение по
   [01_environments_and_packaging](./other/01_environments_and_packaging/),
   иначе библиотеки встанут в системный Python.
5. Пройти Docker из [0_tooling_and_workflow](./0_tooling_and_workflow/), затем
   перейти к [2_data_and_messaging](./2_data_and_messaging/) и
   [3_web_frameworks](./3_web_frameworks/), чтобы связать язык с реальными
   backend-сервисами (PostgreSQL, Redis, брокеры поднимаются через
   `docker compose up`).
6. Параллельно читать [4_system_design](./4_system_design/), чтобы видеть, как
   отдельные решения складываются в архитектуру целиком.
7. [5_engineering_communication](./5_engineering_communication/) — проходить в
   любой момент, эти навыки не привязаны к техническому прогрессу.
8. Использовать [other](./other/) как справочник по окружению разработки.

## Проверка примеров

Большинство упражнений — самостоятельные Python-скрипты с `TODO`: это стартовое
состояние задачи, а готовые решения лежат рядом в `04_exercises_answers/`.

```bash
python3 \
  1_python/1_python_fundamentals/01_variables_and_types/03_exercises/01_convert_and_sum.py
```

Пока задача не решена, скрипт падает с `NotImplementedError` — это нормально.

Часть тем (SQL, Redis, брокеры сообщений) поднимают локальное окружение через
Docker Compose — команда для запуска указана в README соответствующей темы.

## Когда двигаться дальше

Внутри каждого раздела и темы в README есть свой блок «Когда двигаться
дальше» с конкретным критерием готовности. На уровне всей базы порядок
задан в «Как проходить» выше.

## Полезные ресурсы

- [Python.org Docs](https://docs.python.org/3/) — официальная документация
  Python.
- [Real Python](https://realpython.com) — практические статьи и туториалы.
- [PEP 8](https://peps.python.org/pep-0008/) — руководство по стилю кода.
- [Fluent
  Python](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)
  — книга Лучано Рамальо о том, как устроен Python «под капотом».
- [Exercism Python Track](https://exercism.org/tracks/python) — практические
  упражнения.

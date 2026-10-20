# logging: базовая настройка

## Почему не print

`print` не умеет уровней важности, не пишет в файл/syslog одновременно с
консолью, не добавляет автоматически время/модуль/номер строки, не
управляется конфигурацией на уровне всего приложения. `logging` решает всё
это через единую иерархию логгеров.

## Быстрый старт

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)
logger.info("сервис запущен")
logger.warning("конфиг не найден, использую дефолт")
logger.error("не удалось подключиться к БД")
```

`logging.getLogger(__name__)` — стандартная идиома: имя логгера = путь
модуля (`myapp.services.user`), что позволяет включать/выключать
логирование по конкретному модулю без изменения кода.

## Уровни важности

От менее к более серьёзному: `DEBUG` < `INFO` < `WARNING` < `ERROR` <
`CRITICAL`. `logger.setLevel(logging.WARNING)` — логгер отбрасывает
сообщения ниже установленного уровня **до** передачи их handler'ам (это
дешевле, чем форматировать и никуда не выводить).

```python
logger.debug("детали для отладки, %s", expensive_repr())
```

Ленивое форматирование через `%s` + позиционные аргументы (а не f-string
внутри вызова) важно: если уровень `DEBUG` отключён, `expensive_repr()`
всё равно вызовется при f-string (`f"...{expensive_repr()}"`), а
`%`-форматирование `logging` выполнит только если сообщение реально
пойдёт в вывод.

## Handlers и formatters

Логгер решает, **что** логировать; handler — **куда** это идёт; formatter —
**как** это выглядит.

```python
import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()          # вывод в stderr
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log")      # вывод в файл
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

Один логгер может писать сразу в несколько мест с разными уровнями и
форматами: например, в консоль — только `INFO`+, в файл — всё, включая
`DEBUG`.

## Иерархия логгеров и propagation

```python
root_logger = logging.getLogger()          # корневой логгер, имя ""
app_logger = logging.getLogger("myapp")    # дочерний
service_logger = logging.getLogger("myapp.service")  # внук
```

По умолчанию сообщения «всплывают» от дочернего логгера к родительским
(`propagate=True`) — если у `myapp.service` нет собственных handler'ов,
сообщение обработают handler'ы `myapp`, а затем корневого логгера.
`basicConfig()` настраивает именно корневой логгер — поэтому в маленьких
скриптах достаточно одного вызова `basicConfig`, а библиотеки/большие
приложения настраивают handler'ы на своих логгерах и оставляют
`propagate` управлять доставкой наверх.

## RotatingFileHandler — логи, которые не растут бесконечно

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=10_000_000, backupCount=5)
```

Ротация по размеру: при достижении `maxBytes` текущий файл переименовывается
(`app.log.1`, `app.log.2`, ...), создаётся новый `app.log`, старые файлы
сверх `backupCount` удаляются. `TimedRotatingFileHandler` — то же самое, но
по времени (по дням/часам).

## Частые ошибки

- Логировать через `print` в библиотечном коде — библиотека не должна
  решать, куда и в каком формате выводить логи, это дело приложения.
  Библиотеки настраивают только `logging.getLogger(__name__)` без
  handler'ов и без `basicConfig`.
- Вызывать `logging.basicConfig()` несколько раз в разных модулях —
  срабатывает только первый вызов (если у корневого логгера уже есть
  handler'ы, повторный `basicConfig` без `force=True` ничего не меняет).
- Логировать секреты (пароли, токены, PII) на уровне `INFO`/`DEBUG` без
  маскирования — типичная утечка данных через агрегаторы логов.

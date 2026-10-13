# datetime, time и часовые пояса

## time vs datetime

- `time` — работа с «системным» временем как числом секунд (`time.time()`,
  `time.monotonic()`, `time.perf_counter()`) и низкоуровневым `time.sleep`.
- `datetime` — работа с календарными датами/временем как структурированными
  объектами: год, месяц, день, час и т.д., арифметика между датами.

```python
import time

time.time()          # unix-время (секунды с эпохи), может скакать при NTP-корректировке
time.monotonic()     # монотонные часы — только для измерения интервалов, не абсолютного времени
time.perf_counter()  # похож на monotonic, максимальная точность — для бенчмарков
```

**Правило**: для измерения длительности («сколько прошло времени») всегда
`time.monotonic()`/`time.perf_counter()`, никогда `time.time()` — системные
часы могут переводиться назад (NTP, ручная правка), и разница `end - start`
может стать отрицательной.

## Наивные и осведомлённые (aware) datetime

```python
from datetime import datetime, timezone

naive = datetime.now()                 # без информации о часовом поясе — двусмысленно
aware = datetime.now(timezone.utc)     # с явным UTC — однозначно
```

- **Naive** datetime не знает, в каком часовом поясе он выражен — сравнение
  и арифметика между naive-датами из разных источников (сервер в UTC,
  пользователь в MSK) — источник тонких багов.
- **Aware** datetime хранит `tzinfo` — сравнения и конвертации корректны.
- Практика для бэкенда: хранить и передавать между сервисами только aware
  datetime в UTC, конвертировать в локальный часовой пояс только на границе
  отображения пользователю.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # стандартная библиотека с 3.9+

utc_now = datetime.now(timezone.utc)
moscow_time = utc_now.astimezone(ZoneInfo("Europe/Moscow"))
print(moscow_time.isoformat())
```

`zoneinfo` (3.9+) заменил сторонний `pytz` как стандартный способ работы с
именованными часовыми поясами (учитывает переходы на летнее время и
исторические изменения правил — то, чего не делает голый `timezone(timedelta(...))`).

## Разбор и форматирование

```python
from datetime import datetime

dt = datetime.strptime("2026-08-21 14:30", "%Y-%m-%d %H:%M")  # строка -> datetime
s = dt.strftime("%d.%m.%Y %H:%M")                              # datetime -> строка

dt2 = datetime.fromisoformat("2026-08-21T14:30:00+00:00")       # ISO 8601, быстрее strptime
```

`fromisoformat`/`isoformat` — предпочтительный способ работы с датами в
JSON/логах/API: однозначный формат, нет неоднозначности между
день/месяц (в отличие от `%d/%m/%Y` против `%m/%d/%Y`).

## Арифметика: timedelta

```python
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
in_a_week = now + timedelta(days=7)
diff = in_a_week - now  # timedelta(days=7)
print(diff.total_seconds())  # 604800.0
```

`timedelta` не понимает «месяцы» и «годы» напрямую (их длительность
непостоянна) — для «через месяц» с учётом календаря используют сторонний
`dateutil.relativedelta` или ручную арифметику по компонентам.

## Частые ошибки

- Сравнение naive и aware datetime бросает `TypeError: can't compare
  offset-naive and offset-aware datetimes`.
- `datetime.utcnow()` (устаревший с 3.12, deprecated) возвращает **naive**
  datetime со значением UTC — легко перепутать с aware UTC. Используйте
  `datetime.now(timezone.utc)`.
- Хранение времени в БД без часового пояса и без документированного
  соглашения «всё в UTC» — жёсткий источник багов при масштабировании на
  несколько регионов.

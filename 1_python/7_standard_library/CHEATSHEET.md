# Стандартная библиотека — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.
Версии указаны там, где поведение зависит от Python.

## collections

Подробно: [01_collections_module.md](./01_theory/01_collections_module.md).

| Задача | Инструмент |
| :--- | :--- |
| Посчитать частоты | `Counter(words).most_common(2)` |
| Сложить / вычесть счётчики | `c1 + c2`, `c1 - c2` (≤ 0 отбрасываются), `c1 & c2` (min), `c1 \| c2` (max) |
| Сгруппировать по ключу | `groups = defaultdict(list); groups[k].append(v)` |
| Очередь / стек с O(1) с обоих концов | `deque`: `append`/`appendleft`/`pop`/`popleft` |
| Последние N событий (кольцевой буфер) | `deque(maxlen=N)` |
| Неизменяемая запись с полями | `class Point(NamedTuple): x: int; y: int` |
| Слои конфига без копирования | `ChainMap(cli_args, env_vars, defaults)` — поиск слева направо |

- ⚠️ `defaultdict`: чтение `d["missing"]` создаёт ключ; `d.get(k)` — не создаёт.
- ⚠️ `Counter` на отсутствующий ключ возвращает `0`, `KeyError` нет.
- ⚠️ `deque[i]` в середине — O(n); `list.pop(0)` / `insert(0, x)` — O(n).

## functools / itertools

Подробно: [02_functools_itertools_extra.md](./01_theory/02_functools_itertools_extra.md).

| Задача | Инструмент |
| :--- | :--- |
| Мемоизация чистой функции | `@lru_cache(maxsize=128)`; без лимита — `@cache` (3.9+) |
| Статистика / сброс кэша | `f.cache_info()` / `f.cache_clear()` (в тестах) |
| Вычислить атрибут один раз | `@cached_property` (нужен `__dict__`, без `__slots__`) |
| Зафиксировать часть аргументов | `square = partial(power, exponent=2)` |
| Нестандартная свёртка | `reduce(lambda acc, x: ..., items, init)`; для `+`/`*`/`max` — `sum`/`math.prod`/`max` |
| Склеить итерируемые без копии | `chain(a, b)` |
| Группы подряд идущих | `groupby(sorted(xs, key=k), key=k)` |
| Декартово произведение | `product([1, 2], ["a", "b"])` |
| Сочетания / перестановки | `combinations(xs, 2)` / `permutations(xs, 2)` |
| Срез бесконечного итератора | `islice(count(10), 5)` → `10..14` |

- ⚠️ `groupby` без предварительной сортировки по тому же ключу дробит группы.
- ⚠️ `lru_cache` на методе держит `self` в ключе — объекты живут дольше.
- ⚠️ Аргументы `lru_cache`-функции должны быть хешируемыми (`list`/`dict` — `TypeError`).

## Время и даты

Подробно: [03_datetime_time_timezones.md](./01_theory/03_datetime_time_timezones.md).

| Задача | Код |
| :--- | :--- |
| Измерить длительность | `time.monotonic()` / `time.perf_counter()` (бенчмарк) |
| Unix-время | `time.time()` (может прыгать при NTP) |
| Сейчас в UTC (aware) | `datetime.now(timezone.utc)` (или `datetime.UTC`, 3.11+) |
| В локальный пояс | `dt.astimezone(ZoneInfo("Europe/Moscow"))` (`zoneinfo`, 3.9+) |
| Строка → datetime | `datetime.strptime(s, "%Y-%m-%d %H:%M")` |
| datetime → строка | `dt.strftime("%d.%m.%Y %H:%M")` |
| ISO 8601 туда / обратно | `dt.isoformat()` / `datetime.fromisoformat(s)` |
| Сдвиг / разница | `dt + timedelta(days=7)`; `(b - a).total_seconds()` |

- ⚠️ `datetime.utcnow()` — naive, устарел с 3.12 (`DeprecationWarning`); пишите `datetime.now(timezone.utc)`.
- ⚠️ Сравнение naive и aware → `TypeError: can't compare offset-naive and offset-aware datetimes`.
- ⚠️ `end - start` по `time.time()` может стать отрицательным.
- ⚠️ `timedelta` не знает «месяц» и «год».
- Правило: храним и передаём aware UTC, в локальный пояс переводим только при показе пользователю.

## re

Подробно: [04_re_regular_expressions.md](./01_theory/04_re_regular_expressions.md) (там же полная таблица синтаксиса).

| Задача | Функция |
| :--- | :--- |
| Первое совпадение где угодно | `re.search(r"\d+", s)` → `Match` или `None` |
| Совпадение с начала строки | `re.match(...)` (не всей строки!) |
| Вся строка целиком | `re.fullmatch(r"\d+", s)` |
| Все совпадения списком / лениво | `re.findall(...)` / `re.finditer(...)` |
| Замена / разбиение | `re.sub(r"\d+", "#", s)` / `re.split(r"\s*,\s*", s)` |
| Шаблон в цикле, именованные группы | `p = re.compile(r"(?P<user>\w+)@(?P<domain>[\w.]+)")`; `m.group("user")`, `m.groupdict()` |
| Нежадный квантификатор | `<.+?>` вместо `<.+>` |

| Флаг | Эффект |
| :--- | :--- |
| `re.I` (`IGNORECASE`) | без учёта регистра |
| `re.M` (`MULTILINE`) | `^`/`$` — на каждой строке |
| `re.S` (`DOTALL`) | `.` совпадает и с `\n` |
| `re.X` (`VERBOSE`) | многострочный шаблон с комментариями |

- ⚠️ Шаблоны всегда `r"..."`: `"\b"` без `r` — это backspace.
- ⚠️ Вложенные квантификаторы `(a+)+b` → catastrophic backtracking.
- ⚠️ HTML/JSON — парсером, а не regex; «начинается с» — `str.startswith`.

## json / csv

Подробно: [05_json_csv_serialization.md](./01_theory/05_json_csv_serialization.md).

| Задача | Код |
| :--- | :--- |
| dict ↔ строка | `json.dumps(obj)` / `json.loads(s)` |
| Читаемо и с кириллицей | `json.dumps(obj, indent=2, ensure_ascii=False)` |
| В файл / из файла | `json.dump(obj, f)` / `json.load(f)` |
| Нестандартный тип (`datetime`) | `json.dumps(obj, default=fn)`, где `fn` возвращает `obj.isoformat()` |
| Строки CSV списками | `csv.reader(f)`, первая строка: `next(reader)` |
| Строки CSV словарями | `csv.DictReader(f)` → `row["name"]` |
| Записать CSV | `w = csv.writer(f); w.writerow([...])` |
| Другой разделитель | `csv.reader(f, delimiter=";")` |

- ⚠️ CSV открывать с `newline=""` и `encoding="utf-8"`.
- ⚠️ CSV всё читает строками: `int(row["age"])` вручную.
- ⚠️ Деньги в JSON — `float`: храните строкой или в копейках.
- ⚠️ `json.load` грузит документ целиком; `csv.reader` — построчно.

## pathlib / os / tempfile

Подробно: [06_pathlib_os_filesystem.md](./01_theory/06_pathlib_os_filesystem.md).

| Задача | Код |
| :--- | :--- |
| Собрать путь | `Path("data") / "raw" / "file.csv"` |
| Части пути | `.parent`, `.name`, `.stem`, `.suffix`, `.with_suffix(".json")` |
| Проверки | `.exists()`, `.is_file()`, `.is_dir()` |
| Создать каталоги | `p.mkdir(parents=True, exist_ok=True)` |
| Прочитать / записать целиком | `p.read_text(encoding="utf-8")` / `p.write_text(s, encoding="utf-8")` |
| Построчно | `with p.open(encoding="utf-8") as f: for line in f: ...` |
| Содержимое каталога / по маске / рекурсивно | `.iterdir()` / `.glob("*.log")` / `.rglob("*.log")` |
| Обход с отсечением подкаталогов | `for root, dirs, files in os.walk(top)` (менять `dirs` на месте) |
| Переменные окружения | `os.environ["X"]` (`KeyError`) / `os.getenv("X", "default")` |
| Временный каталог | `with tempfile.TemporaryDirectory() as tmp:` — удаляется сам |

- ⚠️ `base + "/" + name` — ломается между ОС; используйте `Path`.
- ⚠️ Без `encoding="utf-8"` кодировка зависит от ОС → `UnicodeDecodeError`.

## logging

Подробно: [07_logging_basics.md](./01_theory/07_logging_basics.md).

| Задача | Код |
| :--- | :--- |
| Быстрая настройка (скрипт) | `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")` |
| Логгер модуля | `logger = logging.getLogger(__name__)` |
| Ленивое форматирование | `logger.debug("x=%s", x)` — не f-string |
| Отсечь уровень | `logger.setLevel(logging.WARNING)` (`DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`) |
| Куда писать | `StreamHandler()` (stderr), `FileHandler("app.log")` |
| Ротация по размеру / времени | `RotatingFileHandler(path, maxBytes=..., backupCount=5)` / `TimedRotatingFileHandler` |
| Формат | `handler.setFormatter(logging.Formatter("..."))` |
| Перенастроить root | `logging.basicConfig(..., force=True)` (3.8+) |

- ⚠️ Повторный `basicConfig` без `force=True` ничего не меняет.
- ⚠️ Библиотека не вызывает `basicConfig` и не вешает handler'ы — только `getLogger(__name__)`.
- ⚠️ Не логируйте пароли, токены, PII.

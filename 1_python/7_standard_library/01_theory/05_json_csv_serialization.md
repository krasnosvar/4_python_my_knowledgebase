# json и csv: сериализация данных

**Сериализация** — превращение объекта Python (словаря, списка) в текст
или байты, которые можно сохранить в файл или отправить по сети, и
обратное восстановление (десериализация).

Работа с файлами в примерах ниже — в двух словах (подробно — в
[06_pathlib_os_filesystem.md](./06_pathlib_os_filesystem.md)):
`with open(путь, режим, encoding="utf-8") as f:` открывает файл, а `with`
гарантирует, что файл закроется после выхода из блока, даже при ошибке.
Режим `"r"` (по умолчанию) — чтение, `"w"` — запись с перезаписью файла,
`"a"` — дописывание в конец. `encoding="utf-8"` нужен, чтобы кириллица
читалась и писалась одинаково на любой ОС.

## json

```python
import json

data = {"name": "den", "age": 30, "active": True, "tags": ["a", "b"]}

s = json.dumps(data)                     # dict -> строка JSON
s_pretty = json.dumps(data, indent=2, ensure_ascii=False)  # читаемо + кириллица без \uXXXX

parsed = json.loads(s)                   # строка JSON -> dict

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)   # прямо в файл

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

- `ensure_ascii=False` — иначе кириллица и другие не-ASCII символы
  экранируются в `\uXXXX`, что затрудняет чтение файла человеком (данные
  при этом корректны, просто менее читаемы).
- `json.dumps` не умеет сериализовать произвольные объекты (`datetime`,
  кастомные классы, `Decimal`) без помощи — либо привести к строке/числу
  заранее, либо передать `default=`:

```python
from datetime import datetime

def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"не могу сериализовать {type(obj)}")

json.dumps({"created": datetime.now()}, default=default)
```

- Для объектной десериализации в кастомные типы (например, dataclass) есть
  параметр `object_hook` у `json.loads`, но чаще проще десериализовать в
  `dict`/`list` и явно сконструировать нужный объект (`MyClass(**data)`),
  либо использовать сторонние библиотеки валидации данных (pydantic и
  подобные — вне stdlib).
- Числа с плавающей точкой в JSON — это `float`, не `Decimal`: денежные
  суммы через `json` без дополнительной обработки теряют точность —
  хранить как строку или целое число (копейки/центы).

## csv

```python
import csv

with open("users.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print(row)  # список строк: ['1', 'den', '30']

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "age"])
    writer.writerow([1, "den", 30])
```

- `newline=""` при открытии файла для csv — обязательная идиома в stdlib
  (иначе на Windows возможны лишние пустые строки из-за двойной обработки
  `\r\n`).
- `csv.DictReader`/`csv.DictWriter` — работа со строками как со словарями
  по заголовку, а не по позиции — надёжнее при изменении порядка колонок:

```python
with open("users.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["age"])  # row — dict {'id': ..., 'name': ..., 'age': ...}
```

- `csv.writer`/`DictWriter` сами не приводят типы: все значения записываются
  как строки через `str()`. При чтении также всё возвращается строками —
  числа нужно приводить вручную (`int(row["age"])`).
- Диалекты (`csv.excel`, `csv.excel_tab`) и параметр `delimiter=";"` —
  разные системы используют разные разделители (запятая vs точка с
  запятой в локалях с десятичной запятой).

## Когда что

| Формат | Когда |
|---|---|
| `json` | вложенные структуры, API, конфиги, обмен между сервисами |
| `csv` | табличные плоские данные, экспорт для Excel/аналитиков, построчная обработка больших файлов |

`csv` можно читать построчно без загрузки всего файла в память (`csv.reader`
— генератор поверх файлового объекта) — важно для больших файлов. `json`
по умолчанию требует загрузки всего документа в память для `json.load`;
для потокового разбора очень больших JSON нужны сторонние библиотеки
(`ijson` и подобные, вне стандартной библиотеки).

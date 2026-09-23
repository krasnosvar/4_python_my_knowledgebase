# pathlib и os: работа с файловой системой

## pathlib — предпочтительный способ работы с путями

```python
from pathlib import Path

p = Path("data") / "raw" / "file.csv"   # соединение путей через / — кроссплатформенно
print(p)                                 # data/raw/file.csv (или data\raw\file.csv на Windows)

p.exists()        # существует ли путь
p.is_file()
p.is_dir()
p.parent          # data/raw
p.name            # file.csv
p.stem            # file (без расширения)
p.suffix          # .csv
p.with_suffix(".json")  # data/raw/file.json

p.parent.mkdir(parents=True, exist_ok=True)  # создать все недостающие директории
```

`pathlib.Path` — объектный API поверх путей, заменяет ручную конкатенацию
строк (`os.path.join`) и большинство функций `os.path`. Оператор `/`
работает независимо от ОС (сам выбирает `/` или `\`), в отличие от
ручного `"data" + "/" + "raw"`.

## Чтение и запись файлов через Path

```python
text = Path("config.txt").read_text(encoding="utf-8")
Path("output.txt").write_text("result", encoding="utf-8")

data = Path("data.bin").read_bytes()
Path("data.bin").write_bytes(data)
```

Короче, чем `open(...)`/`with`, для простых случаев «прочитать/записать
весь файл целиком». Для построчной обработки больших файлов всё равно
нужен `with path.open() as f: for line in f`.

## Обход директорий

```python
for path in Path("logs").iterdir():        # только непосредственные элементы директории
    print(path)

for path in Path("logs").glob("*.log"):     # по маске, без рекурсии
    print(path)

for path in Path("logs").rglob("*.log"):    # рекурсивно, включая поддиректории
    print(path)
```

`rglob("*.log")` эквивалентен `glob("**/*.log", recursive=True)` из `glob`
и делает то же самое, что `os.walk`, но в одну строку для типичного случая
«найти все файлы с расширением».

## os и os.path — когда всё ещё нужны

`pathlib` не заменяет `os` полностью:

```python
import os

os.environ["MY_VAR"]              # переменные окружения
os.getenv("MY_VAR", "default")
os.cpu_count()                    # число ядер CPU
os.getpid()                       # PID процесса
os.walk("logs")                   # рекурсивный обход с контролем над поддиректориями/файлами раздельно

for root, dirs, files in os.walk("logs"):
    for name in files:
        print(os.path.join(root, name))
```

`os.walk` даёт больше контроля, чем `rglob`, когда нужно, например,
пропускать некоторые поддиректории на лету (модифицировать `dirs` внутри
цикла — стандартная идиома для этого).

## Временные файлы и директории

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    (tmp_path / "scratch.txt").write_text("data")
    # директория и всё её содержимое удаляются автоматически при выходе из with
```

`tempfile.TemporaryDirectory`/`NamedTemporaryFile` — стандартный способ
работать с временными файлами в тестах и скриптах без ручной очистки.

## Частые ошибки

- Конкатенация путей строками (`base + "/" + name`) вместо `Path`/`os.path.join`
  — ломается на другой ОС и при отсутствующих/лишних слэшах.
- Забыть `encoding="utf-8"` при открытии текстовых файлов — на разных ОС
  дефолтная кодировка может отличаться (`locale.getpreferredencoding()`),
  что даёт `UnicodeDecodeError` при переносе кода между машинами.
- Сравнение путей как строк (`str(p1) == str(p2)`) вместо `Path`-объектов
  — `Path` умеет нормализовать (`resolve()`) и сравнивать корректно с учётом ОС.

# Типизация и статический анализ — шпаргалка

Подробности — в [01_theory/](./01_theory/): аннотации и mypy —
[01_type_hints_and_mypy.md](./01_theory/01_type_hints_and_mypy.md), ruff,
black, pre-commit — [02_linters_formatters.md](./01_theory/02_linters_formatters.md).
Аннотации в рантайме **не проверяются**: `add("2", "3")` при `a: int` вернёт `"23"`.

## Синтаксис аннотаций

| Что выразить | Запись | С какой версии |
| :--- | :--- | :--- |
| Может быть `None` | `X \| None` (старое: `Optional[X]`) | `\|` — 3.10+ |
| Один из типов | `int \| str` (старое: `Union[int, str]`) | 3.10+ |
| Коллекции | `list[str]`, `dict[str, int]`, `set[int]` | 3.9+ (раньше `typing.List`) |
| Кортеж фиксированный / любой длины | `tuple[int, str]` / `tuple[int, ...]` | 3.9+ |
| Функция `(int, str) -> bool` | `Callable[[int, str], bool]` (из `collections.abc` или `typing`) | — |
| Generic-функция | `T = TypeVar("T")`; `def first(items: list[T]) -> T` | — |
| Generic без `TypeVar` (PEP 695) | `class Stack[T]: ...`, функция — см. `first` ниже | 3.12+ |
| Псевдоним типа | `type UserId = int` (старое: `UserId = int`) | `type` — 3.12+ |
| Структурный интерфейс | `class SupportsClose(Protocol): def close(self) -> None: ...` | — |
| Словарь с фиксированными ключами | `class User(TypedDict): id: int; name: str` | — |
| Выключить проверку точечно | `Any` | — |

```python
from typing import Protocol, TypedDict

def parse(value: str | int) -> float:
    return float(value)

def first[T](items: list[T]) -> T:      # 3.12+
    return items[0]

type UserId = int                        # 3.12+

class SupportsClose(Protocol):
    def close(self) -> None: ...

class User(TypedDict):
    id: UserId
    name: str

def cleanup(resource: SupportsClose) -> None:   # подходит любой объект с close()
    resource.close()

print(parse("2.5"), first([1, 2]), User(id=1, name="Аня"))
# 2.5 1 {'id': 1, 'name': 'Аня'}
```

## mypy

| Задача | Команда / настройка |
| :--- | :--- |
| Проверить код | `mypy src/` |
| Строгий режим (обязательные аннотации, без неявного `Any`) | `mypy --strict src/` |
| То же в `pyproject.toml` | `[tool.mypy]` → `strict = true`, `python_version = "3.12"` |
| Строгость по модулям при постепенном внедрении | `[[tool.mypy.overrides]]` в `pyproject.toml` |
| Подавить одну ошибку в строке | `# type: ignore[код]` (не голый `# type: ignore`) |

Что ловит: не тот тип аргумента, несуществующий атрибут, `X | None` без
проверки на `None`, несовместимое переопределение метода в наследнике.

## Ruff и Black

| Задача | Команда |
| :--- | :--- |
| Линт | `ruff check .` |
| Линт с безопасными автоисправлениями | `ruff check . --fix` |
| Форматирование (совместимо с Black) | `ruff format .` |
| Black: переформатировать / только проверить (CI) / показать diff | `black .` / `black --check .` / `black --diff .` |
| Поставить git hook | `pre-commit install` |
| Прогнать хуки по всем файлам | `pre-commit run --all-files` |

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]   # pycodestyle, pyflakes, isort, pyupgrade, bugbear, simplify
```

## Когда что использовать

| Инструмент | Задача |
| :--- | :--- |
| mypy / pyright | Ошибки **типов** до запуска |
| `ruff check` | Баги и стиль без запуска: неиспользуемые импорты, `def f(x=[])`, `is` с литералом |
| `ruff format` / black | Единое форматирование; в новых проектах обычно только ruff |
| pydantic / typeguard | Проверка типов **в рантайме** на границах (HTTP-запрос, JSON) |
| pre-commit | Чтобы проверки запускались на каждом `git commit` |

## Частые ошибки

- ⚠️ `Any` заразен: всё, что вычислено из `Any`, тоже `Any` — проверки молча выключаются по цепочке.
- Аннотации не валидируют данные в рантайме — для входных данных нужен pydantic или аналог.
- Голый `# type: ignore` скроет и будущие, несвязанные ошибки в той же строке.
- `--strict` на старом проекте сразу — сотни ошибок; начинать с дефолтного режима по модулям.

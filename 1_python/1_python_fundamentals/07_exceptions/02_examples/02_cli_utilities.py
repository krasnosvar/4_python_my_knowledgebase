"""
Пример: разбор CLI-подобных параметров конфигурации с проверкой ошибок.

Демонстрирует:
- приведение типов через try/except ValueError;
- проверку допустимых флагов за O(1) через set и выброс raise ValueError;
- использование кортежа как составного ключа словаря.

Запуск:
    python3 02_examples/02_cli_utilities.py
"""

ALLOWED_FLAGS = {"verbose", "debug", "dry-run", "force"}

RAW_ARGS = [
    "--verbose",
    "--timeout=30",
    "--retries=3",
    "--ratio=0.5",
    "--dry-run",
]


def coerce(value: str) -> int | float | str:
    """Пытается привести строку к int, затем к float, иначе оставляет str."""
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def parse_args(raw_args: list[str]) -> dict[str, object]:
    config: dict[str, object] = {}
    for arg in raw_args:
        name = arg.lstrip("-")
        if "=" in name:
            key, value = name.split("=", 1)
            config[key] = coerce(value)
        else:
            if name not in ALLOWED_FLAGS:
                raise ValueError(f"Неизвестный флаг: --{name}")
            config[name] = True
    return config


config = parse_args(RAW_ARGS)
print("Разобранная конфигурация:")
for key, value in config.items():
    print(f"  {key!r}: {value!r} (тип {type(value).__name__})")

registry: dict[tuple[str, int], str] = {}
registry[("server-1", 8080)] = "primary"
registry[("server-2", 8081)] = "replica"
print("\nРеестр серверов (ключ — кортеж (host, port)):")
for key, role in registry.items():
    print(f"  {key} -> {role}")

try:
    parse_args(["--unknown-flag"])
except ValueError as exc:
    print(f"\nОжидаемая ошибка валидации: {exc}")

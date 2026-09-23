"""
Пример: разбор CLI-подобных параметров конфигурации.

Демонстрирует:
- приведение типов (type coercion) значений, пришедших в виде строк;
- множество (set) для валидации допустимых флагов, O(1) проверка принадлежности;
- хешируемость кортежа как составного ключа конфигурации.
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
    """Пытается привести строку к int, затем к float, иначе возвращает как есть."""
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
            # это флаг: проверяем принадлежность множеству допустимых флагов за O(1)
            if name not in ALLOWED_FLAGS:
                raise ValueError(f"Неизвестный флаг: --{name}")
            config[name] = True
    return config


def main() -> None:
    config = parse_args(RAW_ARGS)
    print("Разобранная конфигурация:")
    for key, value in config.items():
        print(f"  {key!r}: {value!r} (тип {type(value).__name__})")

    # Кортеж хешируем -> можно использовать как составной ключ кэша/реестра
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


if __name__ == "__main__":
    main()

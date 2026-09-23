"""Система CLI-команд на Protocol (утиная типизация) и dataclass для конфигурации."""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class CliConfig:
    verbose: bool = False
    aliases: dict[str, str] = field(default_factory=dict)


class Command(Protocol):
    """Любой объект с такой сигнатурой run() подходит — без явного наследования."""

    name: str

    def run(self, args: list[str]) -> str: ...


class GreetCommand:
    name = "greet"

    def run(self, args: list[str]) -> str:
        who = args[0] if args else "мир"
        return f"Привет, {who}!"


class SumCommand:
    name = "sum"

    def run(self, args: list[str]) -> str:
        total = sum(int(a) for a in args)
        return f"Сумма: {total}"


class CommandRegistry:
    def __init__(self, config: CliConfig) -> None:
        self._config = config
        self._commands: dict[str, Command] = {}

    def register(self, command: Command) -> None:
        self._commands[command.name] = command

    def dispatch(self, name: str, args: list[str]) -> str:
        resolved = self._config.aliases.get(name, name)
        command = self._commands.get(resolved)
        if command is None:
            return f"Неизвестная команда: {name}"
        result = command.run(args)
        if self._config.verbose:
            result = f"[{resolved}] {result}"
        return result


if __name__ == "__main__":
    config = CliConfig(verbose=True, aliases={"hi": "greet"})
    registry = CommandRegistry(config)
    registry.register(GreetCommand())
    registry.register(SumCommand())

    print(registry.dispatch("hi", ["Аня"]))
    print(registry.dispatch("sum", ["1", "2", "3"]))
    print(registry.dispatch("unknown", []))

"""Задача: определите typing.Protocol с методом render() -> str, и напишите
функцию, принимающую любой объект, структурно совместимый с этим протоколом.
Два класса ниже НЕ должны наследоваться ни от чего — только совпадать по форме."""

from typing import Protocol


# TODO: определите Renderable(Protocol) с методом render(self) -> str.
class Renderable(Protocol):
    pass


def render_all(items: list[Renderable]) -> list[str]:
    # TODO: верните список результатов item.render() для каждого item.
    raise NotImplementedError


class HtmlButton:
    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"<button>{self.label}</button>"


class PlainTextLine:
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self) -> str:
        return f"- {self.text}"


def main() -> None:
    items: list[Renderable] = [HtmlButton("OK"), PlainTextLine("пункт списка")]
    rendered = render_all(items)

    no_shared_base = HtmlButton.__mro__[1] is object and PlainTextLine.__mro__[1] is object

    checks = [
        (rendered == ["<button>OK</button>", "- пункт списка"], "render_all вызывает render() у обоих объектов"),
        (no_shared_base, "HtmlButton и PlainTextLine не связаны наследованием, только формой"),
        (hasattr(Renderable, "__protocol_attrs__") or hasattr(Renderable, "_is_protocol"), "Renderable объявлен как Protocol"),
    ]

    checks_passed = 0
    total_checks = len(checks)
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if ok:
            checks_passed += 1
        print(f"[{status}] {description}")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

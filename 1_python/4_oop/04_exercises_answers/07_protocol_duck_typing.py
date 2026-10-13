"""Решение: Protocol Renderable и структурно совместимые классы без наследования."""

from typing import Protocol


class Renderable(Protocol):
    def render(self) -> str: ...


def render_all(items: list[Renderable]) -> list[str]:
    return [item.render() for item in items]


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

    all_ok = True
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"[{status}] {description}")

    print("PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()

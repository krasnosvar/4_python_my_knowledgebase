"""
pathlib: соединение путей, чтение/запись, обход директорий.

Запуск: python main.py
"""
from __future__ import annotations

import tempfile
from pathlib import Path


def demo_path_basics() -> None:
    print("--- базовые операции Path ---")
    p = Path("data") / "raw" / "file.csv"
    print(p, p.parent, p.name, p.stem, p.suffix)
    print(p.with_suffix(".json"))


def demo_read_write_and_walk() -> None:
    print("\n--- запись/чтение и обход директорий ---")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "logs").mkdir(parents=True, exist_ok=True)

        for i in range(3):
            (root / "logs" / f"app_{i}.log").write_text(f"line {i}\n", encoding="utf-8")
        (root / "logs" / "readme.txt").write_text("not a log", encoding="utf-8")

        print("iterdir:")
        for path in sorted((root / "logs").iterdir()):
            print(" ", path.name)

        print("glob *.log:")
        log_files = sorted((root / "logs").glob("*.log"))
        for path in log_files:
            print(" ", path.name, "->", path.read_text(encoding="utf-8").strip())

        assert len(log_files) == 3

        print("rglob **/*.log:")
        for path in sorted(root.rglob("*.log")):
            print(" ", path.relative_to(root))


def main() -> None:
    demo_path_basics()
    demo_read_write_and_walk()


if __name__ == "__main__":
    main()

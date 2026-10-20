"""
json и csv: сериализация, round-trip через временный файл.

Запуск: python main.py
"""
from __future__ import annotations

import csv
import json
import tempfile
from datetime import datetime
from pathlib import Path


def demo_json() -> None:
    print("--- json ---")
    data = {"name": "den", "age": 30, "active": True, "tags": ["a", "b"]}

    s = json.dumps(data, ensure_ascii=False, indent=2)
    print(s)

    parsed = json.loads(s)
    assert parsed == data

    def default(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"не могу сериализовать {type(obj)}")

    with_date = json.dumps({"created": datetime(2026, 8, 21)}, default=default)
    print(with_date)


def demo_csv() -> None:
    print("\n--- csv ---")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "users.csv"

        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age"])
            writer.writerow([1, "den", 30])
            writer.writerow([2, "anna", 25])

        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        for row in rows:
            print(row)

        assert rows[0]["name"] == "den"
        assert int(rows[0]["age"]) == 30


def main() -> None:
    demo_json()
    demo_csv()


if __name__ == "__main__":
    main()

"""Решение: 05_json_csv_roundtrip"""
from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path


USERS = [
    {"id": 1, "name": "den", "age": 30, "active": True},
    {"id": 2, "name": "anna", "age": 25, "active": False},
]


def csv_json_roundtrip(users: list[dict], tmp_dir: Path) -> list[dict]:
    csv_path = tmp_dir / "users.csv"
    json_path = tmp_dir / "users.json"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "active"])
        writer.writeheader()
        writer.writerows(users)

    with csv_path.open(newline="", encoding="utf-8") as f:
        restored = []
        for row in csv.DictReader(f):
            restored.append({
                "id": int(row["id"]),
                "name": row["name"],
                "age": int(row["age"]),
                "active": row["active"] == "True",
            })

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(restored, f, indent=2, ensure_ascii=False)

    with json_path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        result = csv_json_roundtrip(USERS, Path(tmp))

    assert result == USERS, f"данные должны совпасть после round-trip, получили {result}"
    print("Round-trip успешен:", result)


if __name__ == "__main__":
    main()

"""
Задача: дан список словарей (пользователи). Нужно:
  1. Сохранить их в CSV-файл.
  2. Прочитать CSV обратно и привести типы (age -> int, active -> bool).
  3. Сохранить восстановленные данные в JSON-файл с indent=2.
  4. Прочитать JSON обратно и вернуть список словарей.

Запусти: python main.py
"""
from __future__ import annotations

import tempfile
from pathlib import Path


USERS = [
    {"id": 1, "name": "den", "age": 30, "active": True},
    {"id": 2, "name": "anna", "age": 25, "active": False},
]


def csv_json_roundtrip(users: list[dict], tmp_dir: Path) -> list[dict]:
    """
    TODO:
      1. Записать users в tmp_dir / "users.csv" через csv.DictWriter
         (не забыть newline="" при открытии файла).
      2. Прочитать users.csv обратно через csv.DictReader, привести
         id/age к int, active к bool (строка "True"/"False" -> bool).
      3. Записать восстановленный список в tmp_dir / "users.json" через
         json.dump(..., indent=2, ensure_ascii=False).
      4. Прочитать users.json обратно через json.load и вернуть результат.
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 1
    with tempfile.TemporaryDirectory() as tmp:
        result = csv_json_roundtrip(USERS, Path(tmp))

    assert result == USERS, f"данные должны совпасть после round-trip, получили {result}"
    checks_passed += 1
    print("Round-trip успешен:", result)
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()

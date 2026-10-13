"""
Упражнение: dict comprehension для построения lookup-таблицы.

TODO: реализуйте index_records(records) — верните словарь
      {record["id"]: record for record in records} ОДНОЙ dict comprehension.
"""

RECORDS = [
    {"id": 101, "name": "Алиса", "role": "engineer"},
    {"id": 102, "name": "Борис", "role": "designer"},
    {"id": 103, "name": "Вера", "role": "manager"},
]


def index_records(records: list[dict]) -> dict[int, dict]:
    raise NotImplementedError("Постройте словарь id -> record через dict comprehension")


def _self_check() -> None:
    indexed = index_records(RECORDS)

    assert isinstance(indexed, dict), "Результат должен быть словарём"
    print("PASS: результат — словарь")

    assert len(indexed) == 3, f"Ожидалось 3 записи, получено {len(indexed)}"
    print("PASS: количество записей совпадает с исходным списком")

    assert indexed[102]["name"] == "Борис", "Доступ по id=102 должен вернуть запись Бориса"
    print("PASS: быстрый доступ по id=102 работает")

    assert indexed[101] is RECORDS[0], "Значение в словаре должно быть той же записью (той же ссылкой), без копирования"
    print("PASS: значения в словаре — те же объекты, что и в исходном списке")

    print("\nВсе проверки пройдены")


if __name__ == "__main__":
    _self_check()

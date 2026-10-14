"""Решение: dict comprehension для построения lookup-таблицы."""

RECORDS = [
    {"id": 101, "name": "Алиса", "role": "engineer"},
    {"id": 102, "name": "Борис", "role": "designer"},
    {"id": 103, "name": "Вера", "role": "manager"},
]


def index_records(records: list[dict]) -> dict[int, dict]:
    return {record["id"]: record for record in records}


def _self_check() -> None:
    checks_passed = 0
    total_checks = 4

    indexed = index_records(RECORDS)

    assert isinstance(indexed, dict), "Результат должен быть словарём"
    checks_passed += 1
    print("PASS: результат — словарь")

    assert len(indexed) == 3, f"Ожидалось 3 записи, получено {len(indexed)}"
    checks_passed += 1
    print("PASS: количество записей совпадает с исходным списком")

    assert indexed[102]["name"] == "Борис", "Доступ по id=102 должен вернуть запись Бориса"
    checks_passed += 1
    print("PASS: быстрый доступ по id=102 работает")

    assert indexed[101] is RECORDS[0], "Значение в словаре должно быть той же записью (той же ссылкой)"
    checks_passed += 1
    print("PASS: значения в словаре — те же объекты, что и в исходном списке")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    _self_check()

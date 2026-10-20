"""Упражнение: сортировка структурированных записей через lambda в key=."""


records = [
    {"name": "Иван", "department": "IT", "salary": 90000},
    {"name": "Мария", "department": "HR", "salary": 70000},
    {"name": "Пётр", "department": "IT", "salary": 85000},
    {"name": "Анна", "department": "HR", "salary": 75000},
]


def sort_by_salary_desc(items):
    # TODO: верните новый список записей, отсортированный по salary по убыванию,
    # используя lambda в качестве key= для sorted().
    raise NotImplementedError


def sort_by_department_then_name(items):
    # TODO: верните новый список записей, отсортированный сначала по department (по возрастанию),
    # затем по name (по возрастанию) - составной ключ через lambda, возвращающую кортеж.
    raise NotImplementedError


if __name__ == "__main__":
    checks_passed = 0
    total_checks = 2

    by_salary = sort_by_salary_desc(records)
    assert [r["name"] for r in by_salary] == ["Иван", "Пётр", "Анна", "Мария"], (
        f"FAIL: {[r['name'] for r in by_salary]}"
    )
    checks_passed += 1

    by_dept = sort_by_department_then_name(records)
    assert [r["name"] for r in by_dept] == ["Анна", "Мария", "Иван", "Пётр"], (
        f"FAIL: {[r['name'] for r in by_dept]}"
    )
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")

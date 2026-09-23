"""Решение: сортировка записей через lambda в key=."""


records = [
    {"name": "Иван", "department": "IT", "salary": 90000},
    {"name": "Мария", "department": "HR", "salary": 70000},
    {"name": "Пётр", "department": "IT", "salary": 85000},
    {"name": "Анна", "department": "HR", "salary": 75000},
]


def sort_by_salary_desc(items):
    return sorted(items, key=lambda r: r["salary"], reverse=True)


def sort_by_department_then_name(items):
    return sorted(items, key=lambda r: (r["department"], r["name"]))


if __name__ == "__main__":
    by_salary = sort_by_salary_desc(records)
    assert [r["name"] for r in by_salary] == ["Иван", "Пётр", "Анна", "Мария"], (
        f"FAIL: {[r['name'] for r in by_salary]}"
    )

    by_dept = sort_by_department_then_name(records)
    assert [r["name"] for r in by_dept] == ["Анна", "Мария", "Иван", "Пётр"], (
        f"FAIL: {[r['name'] for r in by_dept]}"
    )

    print("PASS")

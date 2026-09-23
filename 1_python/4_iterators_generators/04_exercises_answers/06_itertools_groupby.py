"""Решение: группировка через itertools.groupby."""

from __future__ import annotations

from itertools import groupby
from operator import itemgetter
from typing import TypedDict


class Employee(TypedDict):
    name: str
    department: str


EMPLOYEES: list[Employee] = [
    {"name": "Алиса", "department": "Engineering"},
    {"name": "Борис", "department": "Sales"},
    {"name": "Виктор", "department": "Engineering"},
    {"name": "Галина", "department": "Marketing"},
    {"name": "Дмитрий", "department": "Sales"},
    {"name": "Елена", "department": "Engineering"},
]


def group_by_department(employees: list[Employee]) -> dict[str, list[str]]:
    sorted_employees = sorted(employees, key=itemgetter("department"))

    result: dict[str, list[str]] = {}
    for department, group in groupby(sorted_employees, key=itemgetter("department")):
        result[department] = [employee["name"] for employee in group]
    return result


def main() -> None:
    result = group_by_department(EMPLOYEES)

    assert set(result.keys()) == {"Engineering", "Sales", "Marketing"}, result.keys()
    assert sorted(result["Engineering"]) == ["Алиса", "Виктор", "Елена"], result["Engineering"]
    assert sorted(result["Sales"]) == ["Борис", "Дмитрий"], result["Sales"]
    assert sorted(result["Marketing"]) == ["Галина"], result["Marketing"]

    print("PASS")


if __name__ == "__main__":
    main()

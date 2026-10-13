"""
Задача: сгруппировать записи по полю department, используя itertools.groupby.
Помните: groupby группирует только соседние элементы с одинаковым ключом,
поэтому вход нужно предварительно отсортировать по тому же ключу.
"""

from __future__ import annotations

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
    """Возвращает словарь {отдел: [имена сотрудников]}, где для каждого
    отдела собраны имена ВСЕХ сотрудников этого отдела (порядок внутри
    списка неважен, порядок отделов в словаре не важен)."""
    # TODO: отсортируйте employees по 'department', затем используйте
    # itertools.groupby для группировки. Не забудьте материализовать
    # каждую группу (list(group)) прежде чем перейти к следующей.
    raise NotImplementedError


def main() -> None:
    result = group_by_department(EMPLOYEES)

    assert set(result.keys()) == {"Engineering", "Sales", "Marketing"}, result.keys()
    assert sorted(result["Engineering"]) == ["Алиса", "Виктор", "Елена"], result["Engineering"]
    assert sorted(result["Sales"]) == ["Борис", "Дмитрий"], result["Sales"]
    assert sorted(result["Marketing"]) == ["Галина"], result["Marketing"]

    print("PASS")


if __name__ == "__main__":
    main()

"""
Coverage: показывает разницу между line coverage и branch coverage.

Запуск:
  pytest 02_examples/06_coverage_demo --cov=discount --cov-report=term-missing
  pytest 02_examples/06_coverage_demo --cov=discount --cov-branch --cov-report=term-missing

Требует: pip install pytest-cov

С этим единственным тестом line coverage будет 100% (обе строки функции
выполняются хотя бы в одном из веток if/else суммарно), но branch coverage
покажет, что ветка `else` (is_vip=False) не была протестирована — тест
ниже специально проверяет только is_vip=True.
"""
from __future__ import annotations

from discount import apply_discount


def test_vip_gets_discount():
    assert apply_discount(100, is_vip=True) == 80

# Намеренно нет теста для is_vip=False — чтобы --cov-branch показал непокрытую ветку.
# Полное решение (для сравнения) добавило бы:
# def test_regular_customer_no_discount():
#     assert apply_discount(100, is_vip=False) == 100

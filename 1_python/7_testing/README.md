# Testing

pytest как стандарт де-факто: структура тестов, fixtures, parametrize,
mocks (`unittest.mock`, `monkeypatch`), маркеры, покрытие тестами
(`coverage`), сравнение с `unittest` из стандартной библиотеки.

## Структура

- `01_theory/` — семь тем: основы и структура pytest; fixtures; parametrize;
  mocking (`unittest.mock` + `monkeypatch`); маркеры и конфигурация;
  coverage; сравнение unittest vs pytest.
- `02_examples/` — 7 runnable-примеров (модуль + тесты pytest на каждую тему).
- `03_exercises/` — 6 упражнений: готовый исходный модуль + тест с `TODO`
  внутри тестовых функций (задача — написать тесты, а не имплементацию).
- `04_exercises_answers/` — готовые решения.

## Как проходить

1. `01_pytest_basics_and_structure` → `02_fixtures` → `03_parametrize` —
   базовая механика pytest.
2. `04_mocking...` — как изолировать тест от внешнего мира.
3. `05_markers_and_config`, `06_coverage` — организация большого набора
   тестов и метрика покрытия.
4. `07_unittest_vs_pytest` — для понимания легаси-кода на `unittest`.

## Запуск

```bash
pytest 02_examples/01_pytest_basic_tests -v
pytest 03_exercises/01_write_unit_tests_for_calculator -v

# покрытие (требует pip install pytest-cov)
pytest 02_examples/06_coverage_demo --cov=discount --cov-report=term-missing
```

# Тема 7. Тестирование (Testing)

pytest как стандарт де-факто: структура тестов, fixtures, parametrize,
mocks (`unittest.mock`, `monkeypatch`), маркеры, покрытие тестами
(`coverage`), сравнение с `unittest` из стандартной библиотеки.

## Зачем этот раздел

До сих пор правильность кода проверялась запуском и чтением вывода
глазами — и в упражнениях этой базы встроенной функцией `_self_check()`.
Автотесты делают то же самое систематически: одна команда за секунды
проверяет сотни сценариев после каждой правки. Без них любой рефакторинг
рискован, а баги находят пользователи. В командной разработке код без
тестов обычно просто не принимают на ревью. После раздела вы сможете
писать тесты на pytest, изолировать код от БД/сети через моки, проверять
много входных данных одним тестом и понимать, что на самом деле значит
процент покрытия.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — команды pytest, fixtures, parametrize, моки, маркеры, coverage, соответствие unittest ↔ pytest.

## Что нужно знать заранее

- [1_python_fundamentals](../1_python_fundamentals/) — функции, исключения,
  `import`.
- [2_functions_and_decorators](../2_functions_and_decorators/) — декораторы
  (`@pytest.fixture`, `@pytest.mark...`) и `with` (`pytest.raises`,
  `patch`).
- [3_oop](../3_oop/) — классы и методы: моки подменяют объекты и их
  методы.
- [6_standard_library](../6_standard_library/) — `pathlib` и `datetime`
  встречаются в упражнениях.
- Виртуальное окружение и `pip` —
  [other/01_environments_and_packaging](../../other/01_environments_and_packaging/):
  pytest не входит в стандартную библиотеку, его нужно установить.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_pytest_basics_and_structure.md](./01_theory/01_pytest_basics_and_structure.md)
    — что такое автотест, установка pytest, правила обнаружения тестов.
  - [02_fixtures.md](./01_theory/02_fixtures.md) — подготовка и очистка
    состояния для тестов.
  - [03_parametrize.md](./01_theory/03_parametrize.md) — один тест на много
    наборов входных данных.
  - [04_mocking_unittest_mock_monkeypatch.md](./01_theory/04_mocking_unittest_mock_monkeypatch.md)
    — изоляция от внешнего мира через `unittest.mock` и `monkeypatch`.
  - [05_markers_and_config.md](./01_theory/05_markers_and_config.md) —
    маркеры (`skip`, `xfail`, свои) и конфигурация pytest.
  - [06_coverage.md](./01_theory/06_coverage.md) — line vs branch
    coverage и как читать отчёт.
  - [07_unittest_vs_pytest.md](./01_theory/07_unittest_vs_pytest.md) —
    для понимания легаси-кода на `unittest`.
- **[02_examples/](./02_examples/)** — 7 runnable-примеров (модуль + тесты
  pytest на каждую тему).
- **[03_exercises/](./03_exercises/)** — 6 упражнений: готовый исходный
  модуль + тест с `TODO` внутри тестовых функций (задача — написать
  тесты, а не имплементацию).
- **[04_exercises_answers/](./04_exercises_answers/)** — готовые решения.

## Как проходить

1. `01_pytest_basics_and_structure` → `02_fixtures` → `03_parametrize` —
   базовая механика pytest.
2. `04_mocking...` — как изолировать тест от внешнего мира.
3. `05_markers_and_config`, `06_coverage` — организация большого набора
   тестов и метрика покрытия.
4. `07_unittest_vs_pytest` — для понимания легаси-кода на `unittest`.

## Запуск

pytest и pytest-cov — сторонние пакеты. Ставьте их в виртуальное окружение,
а не в системный Python: как создать и активировать venv, описано в
[other/01_environments_and_packaging](../../other/01_environments_and_packaging/).

```bash
python3 -m venv .venv && source .venv/bin/activate   # один раз, см. ссылку выше
pip install pytest pytest-cov

pytest 02_examples/01_pytest_basic_tests -v
pytest 03_exercises/01_write_unit_tests_for_calculator -v

# покрытие (требует pytest-cov)
pytest 02_examples/06_coverage_demo --cov=discount --cov-report=term-missing
```

## Когда двигаться дальше

Когда можете написать тест с fixture и `parametrize`, проверить
исключение через `pytest.raises`, подменить внешний вызов через
`unittest.mock.patch` или `monkeypatch` и прочитать отчёт покрытия —
переходите к [8_algorithms_dsa](../8_algorithms_dsa/). Навык писать тесты
пригодится во всех следующих разделах.

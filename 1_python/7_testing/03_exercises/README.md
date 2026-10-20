# Упражнения: testing

Каждое упражнение содержит готовый исходный модуль и файл теста с `TODO`
внутри тестовых функций — задача написать содержимое теста (assert'ы,
моки, параметризацию), а не имплементацию исходного кода.

Запуск задания: `pytest 03_exercises/01_write_unit_tests_for_calculator`

Ответы: `pytest 04_exercises_answers/01_write_unit_tests_for_calculator`

1. `01_write_unit_tests_for_calculator` — базовые unit-тесты и pytest.raises.
2. `02_fixtures_for_temp_files` — fixture с yield-teardown для временных файлов.
3. `03_parametrize_validation_rules` — parametrize для валидатора паролей.
4. `04_mock_external_api_call` — patch внешнего HTTP-вызова.
5. `05_monkeypatch_env_and_time` — monkeypatch переменных окружения и времени.
6. `06_custom_markers_slow_tests` — кастомные маркеры и условный skip.

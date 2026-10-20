# Моки: unittest.mock и monkeypatch

## Зачем нужны моки

Заменить реальную зависимость (сеть, БД, время, файловая система, внешний
API) на управляемую подделку — тест становится быстрым, детерминированным
и не зависит от внешнего мира.

## Mock и MagicMock

```python
from unittest.mock import Mock, MagicMock

mock_repo = Mock()
mock_repo.get_user.return_value = {"id": 1, "name": "den"}

result = mock_repo.get_user(1)
assert result == {"id": 1, "name": "den"}
mock_repo.get_user.assert_called_once_with(1)
```

- Любой атрибут/метод на `Mock` создаётся «на лету» и тоже является `Mock`
  — не нужно заранее описывать интерфейс.
- `MagicMock` дополнительно поддерживает магические методы (`__len__`,
  `__iter__`, `__enter__` и т.д.) — нужен, если код использует объект как
  context manager, итератор и т.п.
- `assert_called_once_with(...)`, `assert_not_called()`, `call_count`,
  `call_args_list` — проверка того, **как** был вызван мок, а не только
  что он вернул.

## side_effect — динамическое поведение

```python
mock_repo.get_user.side_effect = [
    {"id": 1, "name": "den"},
    ConnectionError("timeout"),
]

mock_repo.get_user(1)          # первый вызов -> словарь
mock_repo.get_user(2)          # второй вызов -> бросает ConnectionError
```

`side_effect` как список — разные результаты на последовательные вызовы;
как функция — вычисляемый результат в зависимости от аргументов; как
исключение — мок бросает его вместо возврата значения.

## patch — подмена зависимости на время теста

```python
from unittest.mock import patch

def test_send_notification():
    with patch("myapp.services.notifier.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        send_notification("hello")
        mock_post.assert_called_once()
```

Ключевое правило `patch`: **патчить нужно там, где имя используется, а не
там, где оно определено**. Если `myapp/services/notifier.py` делает
`import requests` и вызывает `requests.post`, патчить нужно
`"myapp.services.notifier.requests.post"`, а не `"requests.post"` —
иначе патч не подействует на уже импортированную в модуль ссылку.

```python
@patch("myapp.services.notifier.requests.post")
def test_send_notification(mock_post):
    mock_post.return_value.status_code = 200
    send_notification("hello")
```

`patch` как декоратор передаёт мок первым аргументом теста (порядок —
снизу вверх при нескольких декораторах `@patch`).

## monkeypatch — pytest-нативная альтернатива patch

```python
def test_uses_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert get_api_key() == "test-key"

def test_uses_current_time(monkeypatch):
    monkeypatch.setattr("myapp.utils.time.time", lambda: 1_700_000_000.0)
    assert get_timestamp() == 1_700_000_000.0
```

`monkeypatch` — встроенная fixture pytest: `setattr`, `delattr`, `setenv`,
`delenv`, `syspath_prepend`, `chdir`. Главное преимущество перед ручным
`patch`: **автоматический откат** после теста (даже при падении) — не
нужен `with`/декоратор, pytest сам восстанавливает исходное состояние в
teardown fixture.

## patch vs monkeypatch

| | `unittest.mock.patch` | `monkeypatch` (pytest) |
|---|---|---|
| Откат | автоматический, но нужен `with`/decorator | автоматический через fixture teardown |
| Возможности | подмена атрибутов, вызовы-проверки (`assert_called_*`) | подмена атрибутов, env, sys.path, cwd — без встроенных проверок вызовов |
| Стиль | явный контекст/декоратор | естественная fixture pytest |

На практике часто комбинируют: `monkeypatch.setattr` для подмены + обычный
`Mock()`/`MagicMock()` как заменяемое значение, чтобы получить и удобный
откат, и проверки вызовов.

## Частые ошибки

- Патчить объект в неправильном месте (по определению, а не по
  использованию) — патч «не срабатывает», тест ошибочно проходит на
  реальном вызове.
- Мокать слишком много — если тест мокает 5 из 6 зависимостей, вероятно,
  тестируемая единица слишком большая или тест лучше писать как
  интеграционный.
- Не проверять `assert_called_with` там, где важен сам факт и параметры
  вызова — тест проверяет только возвращаемое значение и не ловит баг
  «вызвали не с теми аргументами».

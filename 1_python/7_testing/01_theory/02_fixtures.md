# Fixtures

Fixture — переиспользуемая функция подготовки/очистки состояния для тестов,
объявленная через `@pytest.fixture`. Заменяет `setUp`/`tearDown` из
`unittest` более гибким и композируемым механизмом.

## Базовое использование

```python
import pytest

@pytest.fixture
def account():
    return Account(balance=100)

def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70

def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150
```

Имя параметра теста должно совпадать с именем fixture — pytest сам находит
и вызывает нужную функцию и передаёт её результат в тест. Такой подход
называется **dependency injection** (внедрение зависимостей): функция не
создаёт нужные ей объекты сама, а получает их готовыми «снаружи» — здесь
от pytest. Тест не знает и не заботится, как именно создаётся `account`,
и не требует явного импорта fixture в каждом файле.

## Setup + teardown через yield

```python
@pytest.fixture
def temp_database():
    db = create_test_database()   # setup
    yield db                       # то, что получает тест
    db.close()                     # teardown — выполнится всегда, даже при падении теста
```

Код после `yield` выполняется в `finally`-подобном порядке: гарантированно
после теста, независимо от того, прошёл он или упал.

## Области видимости (scope)

```python
@pytest.fixture(scope="function")  # по умолчанию: новый экземпляр на каждый тест
def account(): ...

@pytest.fixture(scope="module")    # один экземпляр на все тесты файла
def db_connection(): ...

@pytest.fixture(scope="session")   # один экземпляр на весь прогон pytest
def docker_container(): ...
```

- `function` (по умолчанию) — самая безопасная изоляция: тесты не влияют
  друг на друга через shared state.
- `module`/`session` — для дорогих ресурсов (поднятие БД, Docker-контейнера)
  — но требует аккуратности: shared state между тестами может привести к
  «тестам, которые проходят только в определённом порядке».

## conftest.py — общие fixtures без импорта

Fixtures, объявленные в `conftest.py`, доступны всем тестам в той же
директории и поддиректориях **без явного импорта** — pytest подключает их
автоматически:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def api_client():
    return TestClient(app)
```

```python
# tests/test_users.py
def test_get_user(api_client):  # fixture доступна без import
    response = api_client.get("/users/1")
    assert response.status_code == 200
```

## Композиция fixtures

Fixture может зависеть от другой fixture — pytest сам строит граф
зависимостей и вызывает их в правильном порядке:

```python
@pytest.fixture
def db_connection():
    return connect_to_test_db()

@pytest.fixture
def user_repo(db_connection):
    return UserRepository(db_connection)

def test_find_user(user_repo):
    assert user_repo.find(1) is not None
```

## autouse — fixture без явного параметра

```python
@pytest.fixture(autouse=True)
def reset_global_state():
    yield
    global_cache.clear()
```

Применяется ко **всем** тестам в области видимости без явного упоминания
в сигнатуре — удобно для сквозной очистки состояния, но злоупотребление
`autouse` делает неочевидным, что именно происходит вокруг теста —
используйте только для действительно сквозных вещей (сброс глобального
кэша, случайного seed, логирования).

## Фабрики через fixture

Когда тесту нужно несколько экземпляров с разными параметрами — fixture
возвращает функцию-фабрику, а не готовый объект:

```python
@pytest.fixture
def make_account():
    def _make(balance: int = 0) -> Account:
        return Account(balance=balance)
    return _make

def test_multiple_accounts(make_account):
    rich = make_account(balance=1000)
    poor = make_account(balance=0)
    assert rich.balance > poor.balance
```

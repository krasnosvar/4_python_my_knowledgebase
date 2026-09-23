# Упражнение 2. Ветка и merge

## Стартовое состояние

```bash
bash setup.sh
cd sandbox
```

Репозиторий с одним коммитом: `calculator.py` содержит функцию `add()`.

## TODO

- [ ] Создать и переключиться на ветку `feature/subtract`.
- [ ] В этой ветке добавить в `calculator.py` функцию:
      ```python
      def subtract(a: int, b: int) -> int:
          return a - b
      ```
- [ ] Закоммитить изменение в ветке `feature/subtract`.
- [ ] Вернуться на `main`.
- [ ] Смёржить `feature/subtract` в `main`.
- [ ] Убедиться, что merge прошёл **fast-forward** (в этой задаче на `main`
      не было отдельных новых коммитов, поэтому Git не должен создавать
      merge-коммит).

## Подсказки

- `git switch -c <name>` создаёт ветку и сразу переключается на неё.
- Fast-forward merge не создаёт коммит с двумя родителями — история
  остаётся линейной.

## Проверка

```bash
bash check.sh
```

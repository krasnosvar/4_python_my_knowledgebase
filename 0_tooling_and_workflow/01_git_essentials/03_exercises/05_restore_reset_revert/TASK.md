# Упражнение 5. restore vs reset vs revert

## Стартовое состояние

```bash
bash setup.sh
cd sandbox
```

История из 4 коммитов на `main`:

1. `chore: initial report module`
2. `feat: report v2`
3. `feat: report v3 (bug: broke report output)` — считайте, что этот коммит
   уже запушен и виден остальной команде.
4. `chore: add scratch module`

Плюс есть незакоммиченная правка в `scratch.py` — в файл случайно дописали
лишнюю строку `ACCIDENTAL_LINE = True`.

## TODO

- [ ] **restore**: отменить незакоммиченную правку в `scratch.py`, вернув
      файл к состоянию последнего коммита (уберите
      `ACCIDENTAL_LINE = True`, не трогая остальное вручную).
- [ ] **restore --staged**: создать новый файл `draft.py` с любым
      содержимым, добавить его в staging (`git add`), затем убрать из
      staging через `git restore --staged`, не удаляя сам файл с диска.
- [ ] **revert**: коммит `feat: report v3 (bug: broke report output)` уже
      считается опубликованным — отменить его эффект через `git revert`
      (не через `reset`!), не удаляя сам коммит из истории.
- [ ] После revert функция `build_report()` в `report.py` должна снова
      возвращать `"report v2"`.
- [ ] Убедиться, что коммит `feat: report v3 ...` по-прежнему присутствует
      в `git log` — revert не переписывает историю, а дополняет её.

## Подсказки

- Если бы "плохой" коммит был чисто локальным и никуда не запушенным,
  корректнее было бы использовать `git reset`. Но здесь мы моделируем
  ситуацию с уже опубликованной историей — поэтому только `revert`.
- `draft.py` в конце задания должен остаться на диске как untracked-файл.

## Проверка

```bash
bash check.sh
```

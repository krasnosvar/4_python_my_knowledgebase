# Упражнение 3. Разрешение конфликта слияния

Теория: [03_conflicts_and_hygiene.md](../01_theory/03_conflicts_and_hygiene.md).
Пошаговый пример конфликта: [02_examples/02_conflict_walkthrough.md](../02_examples/02_conflict_walkthrough.md).

## Подготовка

Две ветки по-разному меняют `settings.py`: в `feature/prod-settings`
выключен `DEBUG`, а на `main` увеличен `MAX_CONNECTIONS`.

```bash
mkdir -p ~/git-practice/ex03
cd ~/git-practice/ex03
git init -b main

printf 'DEBUG = True\nMAX_CONNECTIONS = 10\n' > settings.py
git add settings.py
git commit -m "chore: initial settings"

git switch -c feature/prod-settings
printf 'DEBUG = False\nMAX_CONNECTIONS = 10\n' > settings.py
git add settings.py
git commit -m "feat: disable debug mode for production"

git switch main
printf 'DEBUG = True\nMAX_CONNECTIONS = 50\n' > settings.py
git add settings.py
git commit -m "feat: raise max connections to 50"
```

`printf 'строка1\nстрока2\n' > файл` записывает в файл две строки (`\n` —
перевод строки).

## Задание

1. Находясь на `main`, слейте ветку `feature/prod-settings`. Будет
   конфликт: ветки изменили **соседние** строки, а такие правки Git
   считает одним куском и не объединяет сам.
2. Откройте `settings.py` в редакторе и разрешите конфликт так, чтобы
   файл стал таким:
   ```python
   DEBUG = False
   MAX_CONNECTIONS = 50
   ```
   Все строки-маркеры (`<<<<<<<`, `=======`, `>>>>>>>`) должны быть
   удалены.
3. Отметьте конфликт как разрешённый и завершите merge коммитом.

## Проверь себя

```bash
cat settings.py
```

```
DEBUG = False
MAX_CONNECTIONS = 50
```

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

Если вместо этого видно `You have unmerged paths` или
`you are still merging` — merge не завершён.

```bash
git log --oneline --graph --all
```

```
*   224ae9e merge: resolve settings conflict
|\
| * d8cf124 feat: disable debug mode for production
* | a0cddf0 feat: raise max connections to 50
|/
* e8597de chore: initial settings
```

Верхний коммит — merge-коммит с двумя родителями (`|\`).

## Подсказки

- `git status` во время конфликта показывает файлы с конфликтом
  (`both modified`).
- Запутались — `git merge --abort` вернёт всё как было до `git merge`.

Решение: [../04_exercises_answers/03_resolve_merge_conflict.md](../04_exercises_answers/03_resolve_merge_conflict.md).

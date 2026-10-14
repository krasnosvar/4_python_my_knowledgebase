# Пример 2. Как возникает и решается конфликт слияния

Повторяйте команды по порядку и сверяйте вывод (хеши у вас будут другими).
Теория: [03_conflicts_and_hygiene.md](../01_theory/03_conflicts_and_hygiene.md).

## 1. Общая начальная точка

```bash
mkdir -p ~/git-practice/example-02
cd ~/git-practice/example-02
git init -b main

cat > config.py <<'EOF'
DEBUG = False
TIMEOUT = 10
EOF

git add config.py
git commit -m "chore: initial config"
```

## 2. Две ветки меняют одну и ту же строку

В ветке `feature/longer-timeout` ставим `TIMEOUT = 30`:

```bash
git switch -c feature/longer-timeout

cat > config.py <<'EOF'
DEBUG = False
TIMEOUT = 30
EOF

git add config.py
git commit -m "feat: increase timeout to 30s"
```

А на `main` тем временем кто-то поставил `TIMEOUT = 60`:

```bash
git switch main

cat > config.py <<'EOF'
DEBUG = False
TIMEOUT = 60
EOF

git add config.py
git commit -m "feat: increase timeout to 60s"

git log --oneline --graph --all
```

```
* b7b048b feat: increase timeout to 30s
| * dec86cb feat: increase timeout to 60s
|/
* d61c3a5 chore: initial config
```

История разошлась: у каждой ветки свой коммит после общего предка.

## 3. Пытаемся слить — конфликт

```bash
git merge feature/longer-timeout
```

```
Auto-merging config.py
CONFLICT (content): Merge conflict in config.py
Automatic merge failed; fix conflicts and then commit the result.
```

Git не знает, какое значение правильное — 30 или 60 — и останавливается.

```bash
git status
```

```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   config.py
```

```bash
cat config.py
```

```
DEBUG = False
<<<<<<< HEAD
TIMEOUT = 60
=======
TIMEOUT = 30
>>>>>>> feature/longer-timeout
```

- между `<<<<<<< HEAD` и `=======` — версия текущей ветки (`main`);
- между `=======` и `>>>>>>>` — версия сливаемой ветки.

## 4. Разрешаем конфликт

Откройте `config.py` в редакторе, оставьте нужное значение и **удалите все
три строки-маркера**. Должно получиться:

```python
DEBUG = False
TIMEOUT = 60
```

Затем сообщаем Git, что конфликт разрешён, и завершаем merge:

```bash
git add config.py
git status
```

```
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
```

```bash
git commit -m "merge: resolve timeout conflict, keep 60s"
git log --oneline --graph --all
```

```
*   1d5c645 merge: resolve timeout conflict, keep 60s
|\
| * b7b048b feat: increase timeout to 30s
* | dec86cb feat: increase timeout to 60s
|/
* d61c3a5 chore: initial config
```

Верхний коммит — **merge-коммит с двумя родителями** (видно по `|\`).

Если в середине конфликта хочется всё отменить и начать сначала —
`git merge --abort` вернёт состояние до `git merge`.

## Убрать за собой

```bash
cd ~
rm -rf ~/git-practice/example-02
```

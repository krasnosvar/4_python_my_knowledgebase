# Пример 1. Базовый workflow: init → commit → ветка → merge

Повторяйте команды по порядку в терминале и сверяйте вывод. Хеши коммитов
(`0d1b020` и т.п.) у вас будут другими — это нормально, остальное должно
совпадать.

Работаем в отдельной папке вне этого репозитория, чтобы ничего здесь не
задеть. Перед началом один раз выполните первичную настройку Git (имя и
email) — см.
[01_basic_workflow.md → Установка и первая настройка](../01_theory/01_basic_workflow.md#установка-и-первая-настройка).

## 1. Создаём репозиторий

```bash
mkdir -p ~/git-practice/example-01
cd ~/git-practice/example-01
git init -b main
```

```
Initialized empty Git repository in /home/you/git-practice/example-01/.git/
```

`-b main` сразу называет первую ветку `main`.

## 2. Создаём файлы и смотрим статус

```bash
cat > app.py <<'EOF'
def greet(name):
    return f"Hello, {name}!"
EOF

cat > .gitignore <<'EOF'
__pycache__/
*.pyc
.venv/
EOF

git status
```

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	app.py

nothing added to commit but untracked files present (use "git add" to track)
```

`cat > файл <<'EOF' ... EOF` — просто способ создать файл с этим текстом
прямо из терминала. Можно вместо этого создать файл в редакторе.

Оба файла **untracked** — Git их видит, но пока не отслеживает.

## 3. Добавляем в staging area и коммитим

```bash
git add app.py .gitignore
git status
```

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   .gitignore
	new file:   app.py
```

Теперь файлы в staging area — «черновике» коммита.

```bash
git commit -m "feat: add greet() function"
```

```
[main (root-commit) 0d1b020] feat: add greet() function
 2 files changed, 5 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 app.py
```

## 4. Ветка для новой функции

```bash
git switch -c feature/farewell

cat >> app.py <<'EOF'

def farewell(name):
    return f"Goodbye, {name}!"
EOF

git diff
```

```
Switched to a new branch 'feature/farewell'
diff --git a/app.py b/app.py
index 097a41c..b366fe3 100644
--- a/app.py
+++ b/app.py
@@ -1,2 +1,5 @@
 def greet(name):
     return f"Hello, {name}!"
+
+def farewell(name):
+    return f"Goodbye, {name}!"
```

`cat >> файл` (два `>`) дописывает в конец файла. `git diff` показывает,
что изменилось, но ещё не добавлено в staging: строки с `+` — новые.

```bash
git add app.py
git commit -m "feat: add farewell() function"
```

```
[feature/farewell 974ff19] feat: add farewell() function
 1 file changed, 3 insertions(+)
```

## 5. Возвращаемся на main и сливаем ветку

```bash
git switch main
git merge feature/farewell
```

```
Switched to branch 'main'
Updating 0d1b020..974ff19
Fast-forward
 app.py | 3 +++
 1 file changed, 3 insertions(+)
```

**Fast-forward**: на `main` не было своих новых коммитов, поэтому Git
просто передвинул указатель `main` вперёд, на коммит ветки. Merge-коммит
не создаётся.

## 6. Смотрим историю и удаляем ветку

```bash
git log --oneline --graph --all
git branch -d feature/farewell
```

```
* 974ff19 feat: add farewell() function
* 0d1b020 feat: add greet() function
Deleted branch feature/farewell (was 974ff19).
```

История линейная — признак fast-forward. Ветка больше не нужна: её коммит
уже в `main`.

## Убрать за собой

```bash
cd ~
rm -rf ~/git-practice/example-01
```

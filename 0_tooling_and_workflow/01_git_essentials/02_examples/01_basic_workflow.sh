#!/usr/bin/env bash
# Аннотированный проход по базовому workflow: init -> add -> commit -> branch -> merge.
#
# Запуск:
#   bash 01_basic_workflow.sh
#
# Скрипт создаёт временный репозиторий в ./sandbox рядом с собой,
# полностью себя изолируя от вашего реального git-конфига (локальные user.name/email).
# Можно запускать многократно — каждый раз sandbox пересоздаётся с нуля.

set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

echo "=== 1. git init ==="
git init -q
git checkout -q -b main
# Локальный, а не глобальный конфиг: не трогаем настройки пользователя на машине.
git config user.name "KB Learner"
git config user.email "learner@example.com"

echo "=== 2. Первый коммит ==="
cat > app.py <<'EOF'
def greet(name: str) -> str:
    return f"Hello, {name}!"
EOF

cat > .gitignore <<'EOF'
__pycache__/
*.pyc
.venv/
EOF

git add app.py .gitignore
git status
git commit -m "feat: add greet() function"

echo "=== 3. Ветка feature/farewell ==="
git switch -c feature/farewell

cat >> app.py <<'EOF'

def farewell(name: str) -> str:
    return f"Goodbye, {name}!"
EOF

git add app.py
git commit -m "feat: add farewell() function"

echo "=== 4. Возврат на main и fast-forward merge ==="
git switch main
git merge feature/farewell    # fast-forward: main просто "догоняет" feature

echo "=== 5. Итоговая история ==="
git log --oneline --graph --all --decorate

echo
echo "sandbox готов в $(pwd) — можно исследовать 'git log', 'git show' и т.д."

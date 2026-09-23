#!/usr/bin/env bash
# Аннотированный проход по конфликту слияния: как он возникает и как его решить.
#
# Запуск:
#   bash 02_conflict_walkthrough.sh

set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

cat > config.py <<'EOF'
DEBUG = False
TIMEOUT = 10
EOF
git add config.py
git commit -m "chore: initial config"

echo "=== Ветка A меняет TIMEOUT ==="
git switch -c feature/longer-timeout
sed -i 's/TIMEOUT = 10/TIMEOUT = 30/' config.py
git add config.py
git commit -m "feat: increase timeout to 30s"

echo "=== main тем временем тоже меняет TIMEOUT (другое значение) ==="
git switch main
sed -i 's/TIMEOUT = 10/TIMEOUT = 60/' config.py
git add config.py
git commit -m "feat: increase timeout to 60s"

echo "=== Пытаемся смержить feature/longer-timeout в main ==="
set +e
git merge feature/longer-timeout
MERGE_STATUS=$?
set -e

echo
echo "--- git status ---"
git status
echo
echo "--- содержимое config.py с конфликтными маркерами ---"
cat config.py

if [ "$MERGE_STATUS" -ne 0 ]; then
  echo
  echo "=== Разрешаем конфликт: оставляем более консервативное значение 60 ==="
  cat > config.py <<'EOF'
DEBUG = False
TIMEOUT = 60
EOF
  git add config.py
  git commit -m "merge: resolve timeout conflict, keep 60s"
fi

echo
echo "=== Итоговая история (виден merge-коммит с двумя родителями) ==="
git log --oneline --graph --all --decorate
git show --stat HEAD

#!/usr/bin/env bash
# Готовит стартовое состояние для упражнения 03_resolve_merge_conflict.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

cat > settings.py <<'EOF'
DEBUG = True
MAX_CONNECTIONS = 10
EOF
git add settings.py
git commit -q -m "chore: initial settings"

git checkout -q -b feature/prod-settings
sed -i 's/DEBUG = True/DEBUG = False/' settings.py
git add settings.py
git commit -q -m "feat: disable debug mode for production"

git checkout -q main
sed -i 's/MAX_CONNECTIONS = 10/MAX_CONNECTIONS = 50/' settings.py
git add settings.py
git commit -q -m "feat: raise max connections to 50"

echo "Sandbox готов: $(pwd)"
echo
echo "git log --oneline --graph --all:"
git log --oneline --graph --all

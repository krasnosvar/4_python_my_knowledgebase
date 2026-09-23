#!/usr/bin/env bash
# Полный прогон: setup -> решение -> check. Демонстрирует эталонное решение.
set -euo pipefail
cd "$(dirname "$0")"

bash setup.sh
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

printf '*.log\n__pycache__/\n' > .gitignore
git add app.py .gitignore
git commit -q -m "chore: initial project setup"

cd ..
bash check.sh

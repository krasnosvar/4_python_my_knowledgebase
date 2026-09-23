#!/usr/bin/env bash
# Полный прогон: setup -> решение -> check.
set -euo pipefail
cd "$(dirname "$0")"

bash setup.sh
cd sandbox

git switch -c feature/subtract -q
cat >> calculator.py <<'EOF'


def subtract(a: int, b: int) -> int:
    return a - b
EOF
git add calculator.py
git commit -q -m "feat: add subtract()"
git switch -q main
git merge -q feature/subtract

cd ..
bash check.sh

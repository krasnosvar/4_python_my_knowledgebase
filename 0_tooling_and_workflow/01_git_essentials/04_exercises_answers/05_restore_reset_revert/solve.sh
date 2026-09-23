#!/usr/bin/env bash
# Полный прогон: setup -> решение -> check.
set -euo pipefail
cd "$(dirname "$0")"

bash setup.sh
cd sandbox

git restore scratch.py

echo "TEMP = 1" > draft.py
git add draft.py
git restore --staged draft.py

git revert --no-edit HEAD~1

cd ..
bash check.sh

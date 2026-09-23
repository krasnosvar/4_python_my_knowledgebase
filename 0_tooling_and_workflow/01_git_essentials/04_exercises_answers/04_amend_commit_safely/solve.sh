#!/usr/bin/env bash
# Полный прогон: setup -> решение -> check.
set -euo pipefail
cd "$(dirname "$0")"

bash setup.sh
cd sandbox

git add parser_test_notes.py
git commit -q --amend -m "fix: raise ValueError on empty line in parse_line()"

cd ..
bash check.sh

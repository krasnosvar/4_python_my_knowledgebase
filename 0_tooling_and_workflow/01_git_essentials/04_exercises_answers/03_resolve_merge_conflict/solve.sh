#!/usr/bin/env bash
# Полный прогон: setup -> решение -> check.
set -euo pipefail
cd "$(dirname "$0")"

bash setup.sh
cd sandbox

set +e
git merge feature/prod-settings
set -e

printf 'DEBUG = False\nMAX_CONNECTIONS = 50\n' > settings.py
git add settings.py
git commit -q -m "merge: resolve settings conflict"

cd ..
bash check.sh

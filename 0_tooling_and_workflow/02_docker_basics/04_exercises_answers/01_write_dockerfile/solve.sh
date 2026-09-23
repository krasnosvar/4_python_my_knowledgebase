#!/usr/bin/env bash
# Копирует эталонный Dockerfile в это же место и прогоняет check.sh.
set -euo pipefail
cd "$(dirname "$0")"
bash check.sh

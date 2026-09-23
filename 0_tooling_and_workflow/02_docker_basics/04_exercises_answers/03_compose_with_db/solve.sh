#!/usr/bin/env bash
# Прогоняет check.sh с уже готовым docker-compose.yml из этой папки.
set -euo pipefail
cd "$(dirname "$0")"
bash check.sh

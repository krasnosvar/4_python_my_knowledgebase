#!/usr/bin/env bash
# Прогоняет check.sh с уже исправленным Dockerfile из этой папки.
set -euo pipefail
cd "$(dirname "$0")"
bash check.sh

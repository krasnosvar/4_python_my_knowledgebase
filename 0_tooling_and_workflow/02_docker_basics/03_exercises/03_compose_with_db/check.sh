#!/usr/bin/env bash
# Проверяет решение упражнения 03_compose_with_db.
# Требует установленный и запущенный Docker (docker compose plugin).
set -uo pipefail
cd "$(dirname "$0")"

PASS=0
FAIL=0

check() {
  local desc="$1"
  local cond="$2"
  if eval "$cond"; then
    echo "PASS: $desc"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $desc"
    FAIL=$((FAIL + 1))
  fi
}

cleanup() {
  docker compose down -v >/dev/null 2>&1
}
trap cleanup EXIT

if [ ! -f docker-compose.yml ]; then
  echo "FAIL: docker-compose.yml не найден рядом с check.sh"
  exit 1
fi

check "docker-compose.yml валиден (docker compose config)" \
  "docker compose config >/dev/null 2>&1"

check "объявлен сервис cache на образе redis" \
  "docker compose config | grep -qi 'redis'"

check "порт cache не опубликован наружу (нет ports: у сервиса cache)" \
  "! docker compose config | awk '/^  cache:/,/^  [a-zA-Z]/' | grep -q 'published:'"

if docker compose up -d --build >/tmp/kb-ex03-up.log 2>&1; then
  echo "PASS: docker compose up завершился успешно"
  PASS=$((PASS + 1))
else
  echo "FAIL: docker compose up завершился с ошибкой (см. /tmp/kb-ex03-up.log)"
  FAIL=$((FAIL + 1))
  echo; echo "Итого: $PASS PASS, $FAIL FAIL"
  exit 1
fi

sleep 3

APP_PORT=$(docker compose port app 8080 2>/dev/null | cut -d: -f2)
APP_PORT="${APP_PORT:-8080}"

RESPONSE=$(curl -s --max-time 3 "http://localhost:${APP_PORT}/health" || true)
check "app видит cache по имени сервиса (health вернул cache reachable)" \
  "echo '$RESPONSE' | grep -q 'cache reachable'"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]

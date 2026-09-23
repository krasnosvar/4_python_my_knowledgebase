#!/usr/bin/env bash
# Проверяет решение упражнения 01_write_dockerfile.
# Требует установленный и запущенный Docker.
set -uo pipefail
cd "$(dirname "$0")"

IMAGE="kb-exercise-01-write-dockerfile"
CONTAINER="kb-exercise-01-write-dockerfile-run"
HOST_PORT=18080

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
  docker rm -f "$CONTAINER" >/dev/null 2>&1
  docker rmi "$IMAGE" >/dev/null 2>&1
}
trap cleanup EXIT

if [ ! -f Dockerfile ]; then
  echo "FAIL: Dockerfile не найден рядом с check.sh"
  exit 1
fi

check "Dockerfile использует CMD в exec-форме (список, не строка)" \
  "grep -qE '^CMD \[' Dockerfile"

if docker build -t "$IMAGE" . >/tmp/kb-ex01-build.log 2>&1; then
  echo "PASS: docker build завершился успешно"
  PASS=$((PASS + 1))
else
  echo "FAIL: docker build завершился с ошибкой (см. /tmp/kb-ex01-build.log)"
  FAIL=$((FAIL + 1))
  echo; echo "Итого: $PASS PASS, $FAIL FAIL"
  exit 1
fi

docker run --rm -d -p "${HOST_PORT}:8080" --name "$CONTAINER" "$IMAGE" >/dev/null 2>&1
sleep 2

RESPONSE=$(curl -s --max-time 3 "http://localhost:${HOST_PORT}/" || true)
check "контейнер отвечает на / ожидаемым текстом" \
  "echo '$RESPONSE' | grep -q 'hello from exercise app'"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]

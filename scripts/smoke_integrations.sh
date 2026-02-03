#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-https://execalc-api-1052039536917.us-east1.run.app}"
TENANT_ID="${TENANT_ID:-tenant_test_001}"
ROLE="${ROLE:-operator}"

echo "[1/4] list integrations (tenant-scoped)"
curl -s -H "X-Tenant-Id: ${TENANT_ID}" -H "X-Role: ${ROLE}" "${BASE_URL}/integrations" | python3 -m json.tool

echo "[2/4] echo healthcheck WITHOUT X-Scopes (expect ok:false and missing scope error)"
curl -s -X POST -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${TENANT_ID}" -H "X-Role: ${ROLE}" \
  "${BASE_URL}/integrations/echo/healthcheck" \
  -d '{"actor_id":"u1"}' | python3 -m json.tool

echo "[3/4] echo healthcheck WITH X-Scopes (expect ok:true)"
curl -s -X POST -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${TENANT_ID}" -H "X-Role: ${ROLE}" \
  -H "X-Scopes: echo.readonly" \
  "${BASE_URL}/integrations/echo/healthcheck" \
  -d '{"actor_id":"u1"}' | python3 -m json.tool

echo "[4/4] echo fetch WITH X-Scopes (expect query echoed)"
curl -s -X POST -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${TENANT_ID}" -H "X-Role: ${ROLE}" \
  -H "X-Scopes: echo.readonly" \
  "${BASE_URL}/integrations/echo/fetch" \
  -d '{"actor_id":"u1","query":{"ping":"pong","n":1}}' | python3 -m json.tool

echo "smoke_ok"

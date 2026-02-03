#!/usr/bin/env bash
set -euo pipefail

SERVICE_URL="${SERVICE_URL:-https://execalc-api-1052039536917.us-east1.run.app}"
TENANT_ID="${TENANT_ID:-tenant_demo_999}"
ROLE="${ROLE:-operator}"

endpoint="$SERVICE_URL/integrations/null/healthcheck"
tmp_body="$(mktemp /tmp/execalc_smoke_body.XXXXXX.json)"

cleanup() { rm -f "$tmp_body"; }
trap cleanup EXIT

require() {
  local name="$1" got="$2" want="$3"
  if [[ "$got" != "$want" ]]; then
    echo "FAIL: $name (expected $want, got $got)"
    exit 1
  fi
  echo "PASS: $name"
}

http_status() {
  curl -s -o "$tmp_body" -w "%{http_code}" "$@"
}

body_contains() {
  local needle="$1"
  if ! grep -q "$needle" "$tmp_body"; then
    echo "FAIL: response body missing: $needle"
    echo "---- body ----"
    cat "$tmp_body"
    echo "--------------"
    exit 1
  fi
}

body_matches() {
  local regex="$1"
  if ! grep -Eq "$regex" "$tmp_body"; then
    echo "FAIL: response body did not match regex: $regex"
    echo "---- body ----"
    cat "$tmp_body"
    echo "--------------"
    exit 1
  fi
}

# 1) Missing scope -> 403
code="$(http_status -X POST "$endpoint" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d '{}')"
require "missing scope returns 403" "$code" "403"
body_contains "Missing required scopes"

# 2) Wrong scope -> 403
code="$(http_status -X POST "$endpoint" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d '{"scopes":["wrong.scope"]}')"
require "wrong scope returns 403" "$code" "403"
body_contains "Missing required scopes"

# 3) Correct scope -> 200 and ok true
code="$(http_status -X POST "$endpoint" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d '{"scopes":["null.readonly"]}')"
require "correct scope returns 200" "$code" "200"
body_matches '"ok"[[:space:]]*:[[:space:]]*true'

echo "ALL PASS: integrations scope gate is enforced."

# --- allowlist/unknown connector negative test ---
bad_endpoint="$SERVICE_URL/integrations/not-a-connector/healthcheck"
code="$(http_status -X POST "$bad_endpoint" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d '{"scopes":["null.readonly"]}')"
require "unknown connector returns 404" "$code" "404"

# --- list + fetch route gates ---
list_endpoint="$SERVICE_URL/integrations"

code="$(http_status "$list_endpoint")"
require "list without headers returns 403" "$code" "403"
body_contains "\"forbidden\""

code="$(http_status "$list_endpoint" -H "X-Role: admin")"
require "list with admin returns 200" "$code" "200"
body_contains "\"null\""

code="$(http_status "$list_endpoint" -H "X-Tenant-Id: $TENANT_ID" -H "X-Role: $ROLE")"
require "list with tenant+role returns 200" "$code" "200"
body_contains "\"null\""

fetch_endpoint="$SERVICE_URL/integrations/null/fetch"

code="$(http_status -X POST "$fetch_endpoint" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d '{"query":{"ping":true}}')"
require "fetch missing scope returns 403" "$code" "403"
body_contains "Missing required scopes"

code="$(http_status -X POST "$fetch_endpoint" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d '{"scopes":["null.readonly"],"query":{"ping":true}}')"
require "fetch with correct scope returns 200" "$code" "200"
body_contains "\"ping\""

echo "ALL PASS: integrations list+fetch gates are enforced."

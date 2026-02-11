#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:?BASE_URL is required}"
TENANT_ID="${TENANT_ID:-tenant_test_001}"
ROLE="${ROLE:-operator}"
USER_ID="${USER_ID:-u1}"

echo "[1/4] list integrations (tenant-scoped)"
LIST="$(curl -sS \
  -H "X-User-Id: $USER_ID" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  "$BASE_URL/integrations")"
echo "$LIST" | python3 -m json.tool
LIST="$LIST" python3 - <<'PY'
import json, os
o = json.loads(os.environ["LIST"])
assert o.get("ok") is True, o
assert isinstance(o.get("connectors"), list), o
PY

echo "[2/4] echo healthcheck WITHOUT X-Scopes (expect ok:false and missing scope error)"
NO_SCOPE="$(curl -sS \
  -H "Content-Type: application/json" \
  -H "X-User-Id: $USER_ID" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -d "{\"actor_id\":\"$USER_ID\"}" \
  "$BASE_URL/integrations/echo/healthcheck")"
echo "$NO_SCOPE" | python3 -m json.tool
NO_SCOPE="$NO_SCOPE" python3 - <<'PY'
import json, os
o = json.loads(os.environ["NO_SCOPE"])
assert o.get("ok") is False, o
err = o.get("error") or ""
assert "Missing required scopes" in err, o
PY

echo "[3/4] echo healthcheck WITH X-Scopes (expect ok:true)"
YES_SCOPE="$(curl -sS \
  -H "Content-Type: application/json" \
  -H "X-User-Id: $USER_ID" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -H "X-Scopes: echo.readonly" \
  -d "{\"actor_id\":\"$USER_ID\"}" \
  "$BASE_URL/integrations/echo/healthcheck")"
echo "$YES_SCOPE" | python3 -m json.tool
YES_SCOPE="$YES_SCOPE" python3 - <<'PY'
import json, os
o = json.loads(os.environ["YES_SCOPE"])
assert o.get("ok") is True, o
PY

echo "[4/4] echo fetch WITH X-Scopes (expect query echoed)"
FETCH="$(curl -sS \
  -H "Content-Type: application/json" \
  -H "X-User-Id: $USER_ID" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Role: $ROLE" \
  -H "X-Scopes: echo.readonly" \
  -d '{"actor_id":"'"$USER_ID"'","query":{"n":1,"ping":"pong"}}' \
  "$BASE_URL/integrations/echo/fetch")"
echo "$FETCH" | python3 -m json.tool
FETCH="$FETCH" python3 - <<'PY'
import json, os
o = json.loads(os.environ["FETCH"])
assert o.get("ok") is True, o
d = o.get("data") or {}
q = d.get("query") or {}
assert q.get("n") == 1, o
assert q.get("ping") == "pong", o
PY

echo "smoke_ok"

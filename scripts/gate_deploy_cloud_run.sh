#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

SERVICE="${SERVICE:-execalc-api}"
REGION="${REGION:-us-east1}"
PROJECT="${PROJECT:-execalc-core}"

INTEGRATION_TENANT_ID="${INTEGRATION_TENANT_ID:-tenant_test_001}"
INTEGRATION_ROLE="${INTEGRATION_ROLE:-operator}"

die() { echo "ERROR: $*" 1>&2; exit 1; }

curl_json() { curl -sSf "$@"; }

# Dev harness is deny-by-default in production. The deploy gate temporarily enables it
# to exercise /status, /db-info, /executions, and integrations endpoints, then restores it.
DEV_HARNESS_CHANGED=0

restore_dev_harness() {
  if [[ "${DEV_HARNESS_CHANGED}" == "1" ]]; then
    echo "[gate cleanup] restore EXECALC_DEV_HARNESS=0"
    gcloud run services update "$SERVICE" --region "$REGION" --project "$PROJECT"       --update-env-vars EXECALC_DEV_HARNESS=0 --quiet >/dev/null 2>&1 || true
  fi
}
trap restore_dev_harness EXIT

echo "[gate 1/5] predeploy (compile + tests)"
./scripts/gate_predeploy.sh

echo "[gate 2/5] deploy Cloud Run"
gcloud run deploy "$SERVICE" --source . --region "$REGION" --project "$PROJECT" --update-env-vars EXECALC_DEV_HARNESS=1 --quiet
  DEV_HARNESS_CHANGED=1

BASE_URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)')"
[[ -n "$BASE_URL" ]] || die "could not resolve service URL after deploy"
echo "BASE_URL=$BASE_URL"

echo "[gate 3/5] db-info (admin)"
DBINFO="$(curl_json -H "X-Role: admin" "$BASE_URL/db-info")"
echo "$DBINFO" | python3 -m json.tool
DBINFO="$DBINFO" python3 - <<'PY'
import json, os
s = os.environ.get("DBINFO", "")
if not s.strip():
    raise SystemExit("DBINFO was empty (curl returned nothing)")
o = json.loads(s)
assert o.get("ok") is True, o
assert o.get("db_module_available") is True, o
PY

echo "[gate 4/5] status -> persisted -> executions fetch (tenant autocreate path)"
TID="tenant_gate_$(date +%s)"
STATUS="$(curl_json "$BASE_URL/status?tenant_id=$TID")"
echo "$STATUS" | python3 -m json.tool

EID="$(STATUS="$STATUS" python3 - <<'PY'
import json, os
s = os.environ.get("STATUS", "")
if not s.strip():
    raise SystemExit("STATUS was empty (curl returned nothing)")
o = json.loads(s)
assert o.get("ok") is True, o
assert o.get("persisted") is True, o
assert o.get("envelope_id"), o
print(o["envelope_id"])
PY
)"

EXEC="$(curl_json -H "X-Tenant-Id: $TID" -H "X-Role: operator" "$BASE_URL/executions/$EID")"
echo "$EXEC" | python3 -m json.tool
EXEC="$EXEC" python3 - <<'PY'
import json, os
s = os.environ.get("EXEC", "")
if not s.strip():
    raise SystemExit("EXEC was empty (curl returned nothing)")
o = json.loads(s)
assert o.get("ok") is True, o
d = o.get("data") or {}
assert d.get("tenant_id"), o
assert d.get("envelope_id"), o
assert d.get("ok") is True, o
PY

echo "[gate 5/5] integrations smoke (uses configured integration tenant)"
BASE_URL="$BASE_URL" TENANT_ID="$INTEGRATION_TENANT_ID" ROLE="$INTEGRATION_ROLE" bash scripts/smoke_integrations.sh

echo "gate_deploy_ok"

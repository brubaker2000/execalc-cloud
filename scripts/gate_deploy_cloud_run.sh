#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

SERVICE="${SERVICE:-execalc-api}"
REGION="${REGION:-us-east1}"
PROJECT="${PROJECT:-execalc-core}"

INTEGRATION_TENANT_ID="${INTEGRATION_TENANT_ID:-tenant_test_001}"
INTEGRATION_ROLE="${INTEGRATION_ROLE:-operator}"

GATE_USER_ID="${GATE_USER_ID:-gate}"

die() { echo "ERROR: $*" 1>&2; exit 1; }

curl_json() { curl -sSf "$@"; }


curl_json_retry() {
  local tries="${CURL_TRIES:-10}"
  local delay="${CURL_DELAY_SECONDS:-2}"
  local i
  local out
  local rc
  for ((i=1; i<=tries; i++)); do
    set +e
    out="$(curl -sSf "$@")"
    rc="$?"
    set -e
    if [[ "$rc" == "0" ]]; then
      echo "$out"
      return 0
    fi
    echo "[gate] retry ${i}/${tries} (curl rc=${rc})" 1>&2
    sleep "$delay"
  done
  return 1
}


echo "[gate 1/6] predeploy (compile + tests)"
./scripts/gate_predeploy.sh

echo "[gate 2/6] deploy Cloud Run"
gcloud run deploy "$SERVICE" --source . --region "$REGION" --project "$PROJECT" --quiet

BASE_URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)')"
[[ -n "$BASE_URL" ]] || die "could not resolve service URL after deploy"
echo "BASE_URL=$BASE_URL"

echo "[gate 3/6] livez + readyz"
curl_json_retry "$BASE_URL/livez" | python3 -m json.tool >/dev/null
READY="$(curl_json_retry "$BASE_URL/readyz")"
echo "$READY" | python3 -m json.tool >/dev/null
READY="$READY" python3 - <<'PY'
import json, os
o = json.loads(os.environ["READY"])
assert o.get("ok") is True, o
assert o.get("ready") is True, o
PY


echo "[gate 4/6] verify EXECALC_API_KEY configured"
ENVLIST="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(spec.template.spec.containers[0].env)')"
echo "$ENVLIST" | grep -q "EXECALC_API_KEY" || die "EXECALC_API_KEY not configured on Cloud Run service"

echo "[gate 5/6] production ingress (API key path)"
API_KEY="$(gcloud secrets versions access latest --secret=execalc-api-key --project "$PROJECT")"
[[ -n "$API_KEY" ]] || die "could not read execalc-api-key secret"
TID="tenant_test_001"
ING="$(curl_json_retry -H "X-Api-Key: $API_KEY" -H "Content-Type: application/json" -d "{\"tenant_id\":\"$TID\",\"message\":\"ping\"}" "$BASE_URL/ingress")"
echo "$ING" | python3 -m json.tool
ING="$ING" python3 - <<'PY'
import json, os
o = json.loads(os.environ["ING"])
assert o.get("ok") is True, o
assert (o.get("data") or {}).get("received") is True, o
assert o.get("tenant_id"), o
assert o.get("envelope_id"), o
PY
echo "[gate 6/6] verify /status forbidden (dev harness off)"
code="$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/status?tenant_id=tenant_test_001" || true)"
[[ "$code" == "403" ]] || die "dev harness should be closed (expected 403, got $code)"

echo "gate_deploy_ok"

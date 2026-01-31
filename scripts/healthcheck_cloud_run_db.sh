#!/usr/bin/env bash
set -euo pipefail

# End-to-end healthcheck:
# Cloud Run ingress → Cloud SQL persistence → local read via cloud-sql-proxy
#
# Shell A must be running:
#   cloud-sql-proxy execalc-core:us-east1:execalc-db --port 5432
#
# Shell B runs this script from the repo root.

PROJECT="${PROJECT:-execalc-core}"
REGION="${REGION:-us-east1}"
SERVICE="${SERVICE:-execalc-api}"
TENANT_ID="${TENANT_ID:-tenant_demo_999}"

DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-execalc}"
DB_USER="${DB_USER:-execalc_app}"
DB_SECRET="${DB_SECRET:-execalc-db-password}"

# Confirm proxy is listening locally
if ! ss -ltn 2>/dev/null | awk '{print $4}' | grep -Eq "(^${DB_HOST}:${DB_PORT}$|^\\[::1\\]:${DB_PORT}$)"; then
  echo "ERROR: cloud-sql-proxy is not listening on ${DB_HOST}:${DB_PORT}."
  echo "Start it in Shell A: cloud-sql-proxy execalc-core:us-east1:execalc-db --port 5432"
  exit 1
fi

# Resolve Cloud Run service URL (or accept override)
if [[ -z "${SERVICE_URL:-}" ]]; then
  SERVICE_URL="$(gcloud run services describe "$SERVICE" \
    --region "$REGION" --project "$PROJECT" \
    --format='value(status.url)')"
fi

# Call /ingress and extract envelope_id
ENVELOPE_ID="$(
  curl -fsS -X POST "$SERVICE_URL/ingress" \
    -H "Content-Type: application/json" \
    -d "{\"tenant_id\":\"$TENANT_ID\",\"payload\":{\"hello\":\"cloud-run-healthcheck\"}}" \
  | python3 -c 'import sys, json; print(json.load(sys.stdin).get("envelope_id",""))'
)"

if [[ -z "$ENVELOPE_ID" ]]; then
  echo "ERROR: Did not receive envelope_id from ${SERVICE_URL}/ingress"
  exit 1
fi

# Resolve DB password (or accept override)
if [[ -z "${DB_PASSWORD:-}" ]]; then
  DB_PASSWORD="$(gcloud secrets versions access latest \
    --secret="$DB_SECRET" --project "$PROJECT")"
fi

# Query Cloud SQL via local proxy
RESULT="$(
  PGPASSWORD="$DB_PASSWORD" \
  psql "host=${DB_HOST} port=${DB_PORT} dbname=${DB_NAME} user=${DB_USER} sslmode=disable" \
    -t -A \
    -c "SELECT tenant_id||'|'||envelope_id||'|'||ok||'|'||created_at
        FROM execution_records
        WHERE envelope_id='${ENVELOPE_ID}';"
)"

if [[ -z "$RESULT" ]]; then
  echo "ERROR: No DB row found for envelope_id=${ENVELOPE_ID}"
  exit 1
fi

echo "SERVICE_URL=$SERVICE_URL"
echo "ENVELOPE_ID=$ENVELOPE_ID"
echo "DB_ROW=$RESULT"

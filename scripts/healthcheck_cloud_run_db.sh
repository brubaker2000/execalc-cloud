#!/usr/bin/env bash
set -euo pipefail

# Requirements:
# - gcloud authenticated with project execalc-core
# - cloud-sql-proxy running in Shell A on 127.0.0.1:5432
# - psql installed in Cloud Shell

PROJECT="execalc-core"
REGION="us-east1"
SERVICE="execalc-api"
TENANT_ID="tenant_demo_999"

SERVICE_URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)')"

ENVELOPE_ID="$(
  curl -s -X POST "$SERVICE_URL/ingress" \
    -H "Content-Type: application/json" \
    -d "{\"tenant_id\":\"$TENANT_ID\",\"payload\":{\"hello\":\"cloud-run-healthcheck\"}}" \
  | python3 -c 'import sys, json; print(json.load(sys.stdin)["envelope_id"])'
)"

DB_PASSWORD="$(gcloud secrets versions access latest --secret=execalc-db-password --project "$PROJECT")"

RESULT="$(
  PGPASSWORD="$DB_PASSWORD" \
  psql "host=127.0.0.1 port=5432 dbname=execalc user=execalc_app sslmode=disable" \
    -t -A \
    -c "SELECT tenant_id||'|'||envelope_id||'|'||ok||'|'||created_at FROM execution_records WHERE envelope_id='$ENVELOPE_ID';"
)"

echo "SERVICE_URL=$SERVICE_URL"
echo "ENVELOPE_ID=$ENVELOPE_ID"
echo "DB_ROW=$RESULT"

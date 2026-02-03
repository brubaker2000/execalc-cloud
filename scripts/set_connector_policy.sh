#!/usr/bin/env bash
set -euo pipefail

SERVICE="${SERVICE:-execalc-api}"
PROJECT="${PROJECT:-execalc-core}"
REGION="${REGION:-us-east1}"

# JSON values (no spaces). Edit deliberately.
ALLOWLIST_JSON='{"*":["null","echo"]}'
SCOPES_JSON='{"null":["null.readonly"],"echo":["echo.readonly"]}'

echo "Updating Cloud Run env vars for ${SERVICE} in ${PROJECT}/${REGION}..."
gcloud run services update "${SERVICE}" \
  --region "${REGION}" \
  --project "${PROJECT}" \
  --update-env-vars "^@^EXECALC_CONNECTOR_ALLOWLIST=${ALLOWLIST_JSON}@EXECALC_CONNECTOR_REQUIRED_SCOPES=${SCOPES_JSON}"

echo "done"

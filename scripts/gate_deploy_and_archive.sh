#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

SERVICE="${SERVICE:-execalc-api}"
REGION="${REGION:-us-east1}"
PROJECT="${PROJECT:-execalc-core}"

BUCKET="${BUCKET:-gs://execalc-core-build-logs-1052039536917}"

command -v gsutil >/dev/null || { echo "ERROR: gsutil not found" 1>&2; exit 1; }
mkdir -p logs

gsutil ls -b "$BUCKET" >/dev/null 2>&1 || gsutil mb -p "$PROJECT" -l "$REGION" "$BUCKET"

STAMP="$(date +%Y%m%d_%H%M%S)"
SHA="$(git rev-parse --short HEAD 2>/dev/null || echo "no_git")"

LOG_FILE="logs/gate_deploy_${STAMP}_${SHA}.log"
META_FILE="logs/gate_deploy_${STAMP}_${SHA}.meta.json"

set +e
./scripts/gate_deploy_cloud_run.sh 2>&1 | tee "$LOG_FILE"
RC=${PIPESTATUS[0]}
set -e

BASE_URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)' 2>/dev/null || true)"
REVISION="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.latestReadyRevisionName)' 2>/dev/null || true)"

IMAGE=""
if [[ -n "${REVISION:-}" ]]; then
  IMAGE="$(gcloud run revisions describe "$REVISION" --region "$REGION" --project "$PROJECT" --format='value(spec.containers[0].image)' 2>/dev/null || true)"
fi

PROJECT="$PROJECT" REGION="$REGION" SERVICE="$SERVICE" SHA="$SHA" BASE_URL="$BASE_URL" REVISION="$REVISION" IMAGE="$IMAGE" RC="$RC" META_FILE="$META_FILE" \
python3 - <<'PY'
import json, datetime, os

meta = {
  "timestamp_utc": datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z'),
  "project": os.environ.get("PROJECT", ""),
  "region": os.environ.get("REGION", ""),
  "service": os.environ.get("SERVICE", ""),
  "git_sha_short": os.environ.get("SHA", ""),
  "base_url": os.environ.get("BASE_URL", ""),
  "latest_ready_revision": os.environ.get("REVISION", ""),
  "image": os.environ.get("IMAGE", ""),
  "gate_exit_code": int(os.environ.get("RC", "1")),
}

with open(os.environ["META_FILE"], "w", encoding="utf-8") as f:
  json.dump(meta, f, indent=2, sort_keys=True)
  f.write("\n")
PY

ARCHIVE_PATH="${BUCKET}/gates/${SERVICE}/${STAMP}_${SHA}/"
gsutil -q cp "$LOG_FILE" "$META_FILE" "$ARCHIVE_PATH"

echo "archive_path=${ARCHIVE_PATH}"
if [[ "$RC" -ne 0 ]]; then
  exit "$RC"
fi
echo "gate_deploy_and_archive_ok"

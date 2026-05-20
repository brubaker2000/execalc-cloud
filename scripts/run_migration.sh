#!/usr/bin/env bash
set -euo pipefail

# Run a SQL migration file against Cloud SQL via local proxy.
#
# Usage:
#   ./scripts/run_migration.sh infra/migrations/003_memory_objects.sql
#
# Prerequisites (same as healthcheck_cloud_run_db.sh):
#   Shell A must be running:
#     cloud-sql-proxy execalc-core:us-east1:execalc-db --port 5432
#   Then run this script in Shell B from the repo root.

MIGRATION_FILE="${1:-}"
if [[ -z "$MIGRATION_FILE" ]]; then
  echo "Usage: ./scripts/run_migration.sh <path/to/migration.sql>"
  exit 1
fi

if [[ ! -f "$MIGRATION_FILE" ]]; then
  echo "ERROR: File not found: $MIGRATION_FILE"
  exit 1
fi

PROJECT="${PROJECT:-execalc-core}"
DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-execalc}"
DB_USER="${DB_USER:-execalc_app}"
DB_SECRET="${DB_SECRET:-execalc-db-password}"

# Confirm proxy is listening
if ! nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; then
  echo "ERROR: cloud-sql-proxy is not listening on ${DB_HOST}:${DB_PORT}."
  echo "Start it in another terminal:"
  echo "  cloud-sql-proxy execalc-core:us-east1:execalc-db --port 5432"
  exit 1
fi

# Resolve DB password from Secret Manager
if [[ -z "${DB_PASSWORD:-}" ]]; then
  echo "Fetching DB password from Secret Manager..."
  DB_PASSWORD="$(gcloud secrets versions access latest \
    --secret="$DB_SECRET" --project "$PROJECT")"
fi

echo "Running migration: $MIGRATION_FILE"
PGPASSWORD="$DB_PASSWORD" \
psql "host=${DB_HOST} port=${DB_PORT} dbname=${DB_NAME} user=${DB_USER} sslmode=disable" \
  -f "$MIGRATION_FILE" \
  -v ON_ERROR_STOP=1

echo "Migration complete: $MIGRATION_FILE"

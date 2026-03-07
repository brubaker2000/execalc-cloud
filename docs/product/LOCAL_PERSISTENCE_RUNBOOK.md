# Local Persistence Runbook (Dev Only)

This runbook enables local Postgres-backed persistence for the current Decision Journal retrieval flow.

## What this enables
- `POST /decision/run` persists to Postgres and returns `audit.envelope_id`
- `GET /decision/<envelope_id>` retrieves the stored payload
- `GET /decision/recent?limit=N` returns a tenant-scoped timeline

## 1) Start local Postgres (Docker)

```bash
docker rm -f execalc-pg || true

docker run -d --name execalc-pg \
  -e POSTGRES_USER=execalc \
  -e POSTGRES_PASSWORD=execalc_pw \
  -e POSTGRES_DB=execalc \
  -p 5432:5432 \
  postgres:16
```

## 2) Apply schema

From the repo root:

```bash
cat docs/db/schema.sql | docker exec -i execalc-pg psql -U execalc -d execalc
```

## 3) Enable persistence (current shell)

```bash
export EXECALC_PERSIST_EXECUTIONS=1
export EXECALC_DB_HOST=127.0.0.1
export EXECALC_DB_PORT=5432
export EXECALC_DB_NAME=execalc
export EXECALC_DB_USER=execalc
export EXECALC_DB_PASSWORD=execalc_pw
```

## 4) Start the API locally

```bash
EXECALC_DEV_HARNESS=1 FLASK_APP=src/service/api.py flask run --host=127.0.0.1 --port=5000
```

## 5) Create a persisted decision

In a second shell:

```bash
curl -sS -X POST "http://127.0.0.1:5000/decision/run" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: t1" \
  -H "X-Role: operator" \
  -H "X-User-Id: u1" \
  -d '{
    "situation": "Evaluate a vendor renewal under time pressure.",
    "options": [
      {"label": "renew", "description": "Renew the current vendor for one year."},
      {"label": "rebid", "description": "Run a fast competitive rebid."}
    ]
  }'
```

Confirm the response includes:
- `ok: true`
- `audit.envelope_id`
- `audit.persist.persisted: true`

## 6) Retrieve the stored decision

Replace `<ENVELOPE_ID>` with the returned value:

```bash
curl -sS "http://127.0.0.1:5000/decision/<ENVELOPE_ID>" \
  -H "X-Tenant-Id: t1" \
  -H "X-Role: operator" \
  -H "X-User-Id: u1"
```

## 7) List recent decisions

```bash
curl -sS "http://127.0.0.1:5000/decision/recent?limit=5" \
  -H "X-Tenant-Id: t1" \
  -H "X-Role: operator" \
  -H "X-User-Id: u1"
```

Expected result:
- `persist_enabled: true`
- tenant-scoped records from `execution_records`

## Notes
- Persistence is enabled only when both of these are true:
  1. `EXECALC_PERSIST_EXECUTIONS=1`
  2. required DB env vars are present
- The canonical local schema lives in `docs/db/schema.sql`
- Current persistence table: `execution_records`
- Current tenant table: `tenants`

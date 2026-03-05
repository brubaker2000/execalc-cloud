# Local Persistence Runbook (Dev Only)

This runbook enables local Postgres-backed persistence for the Decision Journal endpoints.

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

## 2) Enable persistence (current shell)

```bash
export EXECALC_PERSIST_ENABLED=1
export EXECALC_PG_DSN="postgresql://execalc:execalc_pw@127.0.0.1:5432/execalc"
```

## 3) Quick endpoint check (example)

```bash
curl -sS "http://127.0.0.1:5000/decision/recent?limit=5" \n  -H "X-Tenant-Id: t1" \n  -H "X-Role: operator" \n  -H "X-User-Id: u1"
```

# Build State Snapshot — 2026-02-11

## Repo State
- Repo: execalc-cloud
- Branch: main
- HEAD: 1e87d55
- Working tree: clean

## Completed Tranche
### Tranche 1 — Hardened Execution Spine (Completed and gated)
- Tenant + actor context enforced per request with guaranteed cleanup.
- Dev harness is deny-by-default and explicitly gated.
- Persistence path proven end-to-end (execution_records).
- Connector framework proven with scope enforcement (echo/null).
- Cloud Run deploy gate is the definition of “done” and runs end-to-end.

## Last Verified Gate Run
- Gate: scripts/gate_deploy_cloud_run.sh → PASS (gate_deploy_ok)
- Tests: 20 passed
- Cloud Run:
  - Service: execalc-api
  - Project: execalc-core
  - Region: us-east1
  - Revision deployed: execalc-api-00076-tsl
- DB:
  - persist_enabled: true
  - tables: execution_records, tenants
- Integrations:
  - connectors: echo, null
  - scope enforcement: echo.readonly required (fails closed without X-Scopes; succeeds with X-Scopes)
- Safety:
  - dev harness closure verified: /status returns 403 after close

## Next Planned Work (choose and execute in order)
1) Tranche 2: Tenant Persistence Service (full lifecycle + fail-closed tenant validation)
2) Ship Track: Login boundary for Cloud Run (IAP or equivalent) without weakening tenant isolation
3) Repo Truth Kit expansion: ADRs + TRUE_NORTH page + one-command Makefile targets

## Deploy Record — 2026-02-15 (America/New_York)
- Service: execalc-api
- Region: us-east1
- Project: execalc-core
- Latest ready revision: execalc-api-00076-tsl
- Traffic: 100% -> execalc-api-00076-tsl
- URL: https://execalc-api-7f42ijydqa-ue.a.run.app

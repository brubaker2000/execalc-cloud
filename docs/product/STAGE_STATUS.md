# Execalc Stage Status

Last updated: 2026-03-07
Last verified state: Stage 7A local Postgres happy path proven on workstation

## Stage 4A–4C: Decision Loop Engine (COMPLETE)
- Spec: docs/product/DECISION_LOOP_ENGINE_SPEC.md
- Engine module:
  - src/service/decision_loop/engine.py
  - src/service/decision_loop/models.py
- Unit test: src/service/decision_loop/test_decision_loop.py
- Endpoint: POST /decision/run
- Endpoint test: tests/test_decision_run_endpoint.py
- Persistence metadata (response audit):
  - audit.envelope_id
  - audit.persist

## Stage 5A: Decision Journal Retrieval (COMPLETE)
- Endpoint: GET /decision/<envelope_id>
- Test: tests/test_decision_get_endpoint.py

## Stage 5B: Decision Journal Timeline (COMPLETE)
- Endpoint: GET /decision/recent?limit=N
- Test: tests/test_decision_recent_endpoint.py
- DB helper: list_execution_records (tenant-scoped) [see src/service/db/postgres.py]

## Stage 5C: Smoke Harness Coverage (COMPLETE)
- /decision/recent accessible via smoke harness when enabled
- Test: tests/test_decision_recent_smoke_harness.py

## Stage 6: Persistence Hardening + Operational Defaults (COMPLETE)
- Persistence requested vs enabled semantics separated
- Strict persistence gating for readiness and enabled-state reporting
- Best-effort execution persistence preserved for request paths
- Unit tests do not require DB env vars
- Tenant-scoped persistence behavior preserved
- Main branch verification:
  - python -m compileall -q src/service
  - pytest -q
  - local /decision/run check with persistence off

## Next
### Stage 7A status (live verified on 2026-03-07)
- Lazy-loaded Postgres driver so unit tests no longer fail on eager import
- Persistence-enabled paths covered for:
  - GET /decision/<envelope_id>
  - GET /decision/recent?limit=N
- Local persistence runbook aligned to current env contract
- Local Postgres happy path proven:
  - Docker container started locally
  - Canonical schema applied
  - OS-level `libpq5` dependency installed so `psycopg2` can load
  - `/decision/run` persists successfully to `execution_records`
  - `/decision/<envelope_id>` successfully reads back the stored record
  - `/decision/recent?limit=N` returns tenant-scoped recent records
- Workstation posture note:
  - Shell has `noclobber` behavior; `rm -f` may be needed before redirecting to existing files
  - Long heredocs and long quoted commands are fragile in this environment; prefer simpler, verifiable steps

## Next
- Add a DB-available integration-test slice for Stage 7A (skipped when local Postgres is not available)
- Then move to Stage 7B `/decision/compare` once the journal behavior is stable

## Future Layer Awareness
- Intelligent Front Door is now recognized as a future architectural layer.
- It is not current build scope and should follow sufficient stabilization of the decision journal and comparative reasoning layer.

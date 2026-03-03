# Execalc Stage Status

Last updated: 2026-03-02 21:47 UTC

## Stage 4A–4C: Decision Loop Engine
- Spec: docs/product/DECISION_LOOP_ENGINE_SPEC.md
- Endpoint: POST /decision/run
- Persistence metadata: audit.envelope_id + audit.persist
- Test coverage: decision loop unit tests + decision run endpoint test

## Stage 5A: Decision Journal Retrieval
- Endpoint: GET /decision/<envelope_id>

## Stage 5B: Decision Journal Timeline
- Endpoint: GET /decision/recent?limit=N
- DB helper: list_execution_records (tenant-scoped)

## Stage 5C: Smoke Harness Coverage
- /decision/recent is accessible via smoke harness when enabled
- Test: tests/test_decision_recent_smoke_harness.py

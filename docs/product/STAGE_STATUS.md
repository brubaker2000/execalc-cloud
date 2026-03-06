# Execalc Stage Status

Last updated: 2026-03-06
Last verified state: Stage 6 merged to main; local tests passing

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
## Stage 7: Comparative Decision Memory
Suggested sequence:
- 7A: Journal hardening in real use
- 7B: `/decision/compare`
- 7C: Multi-objective comparison logic

## Future Layer Awareness
- Intelligent Front Door is now recognized as a future architectural layer.
- It is not current build scope and should follow sufficient stabilization of the decision journal and comparative reasoning layer.

# Execalc Stage Status

Last updated: 2026-03-21
Last verified state: Stage 4C–4E Execution Boundary Engine implemented, integrated, tested, and pushed on stage8/ui-shell-scaffold

## Stage 4A–4B: Decision Loop Engine (COMPLETE)
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

## Stage 4C: Action Proposal Contract (COMPLETE)
- Spec: docs/product/EXECUTION_BOUNDARY_ENGINE_SPEC.md
- Runtime models added to:
  - src/service/decision_loop/models.py
- New models:
  - ActionProposal
  - ExecutionSnapshot
  - BoundaryDecision

## Stage 4D: Execution Boundary Engine (COMPLETE)
- Engine module:
  - src/service/decision_loop/execution_boundary_engine.py
- Deterministic outcomes:
  - ALLOW
  - BLOCK
  - RECOMPUTE
  - ESCALATE
- Deterministic checks implemented for:
  - proposal expiration
  - missing authority
  - execution window closed
  - blocking policy flags
  - blocking constraint flags
  - missing required inputs
  - material state change
  - elevated risk posture
  - manual review requirement
- Unit test:
  - src/service/decision_loop/test_execution_boundary_engine.py

## Stage 4E: Execution Audit Trail (COMPLETE FOR CURRENT SERVICE PATH)
- Boundary result now emitted in service response as:
  - execution_boundary
- Boundary result also mirrored into:
  - audit.execution_boundary
- Live service integration:
  - src/service/decision_loop/service.py
- Verified by service test:
  - src/service/decision_loop/test_service.py

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

## Stage 7A status (live verified on 2026-03-07)
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

## Current Architecture Reality
Execalc is now operating as a decision-plus-execution-governance system, not merely a decision artifact generator.

Current governed runtime path:
- operator input
- scenario construction
- decision loop engine
- action proposal
- execution boundary engine
- allow / block / recompute / escalate
- execution or human review

The Executive Rail remains a display surface.
The decision service remains the current runtime spine.
A future chat orchestration layer will sit above both.

## Next
- Formalize the runtime architecture docs so the EBE is canon in the system map
- Surface execution_boundary state in the UI Executive Rail
- Define the chat orchestration layer that classifies turns into discuss / decide / action / execute
- Introduce real execution adapters after orchestration exists
- Deepen persistence so execution-boundary events can be queried independently over time

## Future Layer Awareness
- Intelligent Front Door is now recognized as a future architectural layer.
- Chat Orchestration Layer is now recognized as a future architectural layer.
- Neither should bypass the Execution Boundary Engine once action is implicated.

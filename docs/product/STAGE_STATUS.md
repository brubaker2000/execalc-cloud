# Execalc Stage Status

Last updated: 2026-03-29
Last verified state: Stage 8 UI shell scaffold, navigation identity threading, truthful left-rail injection, observe-only Stage 8B anomaly recording, executive-rail anomaly surfacing, runtime-nugget rail surfacing, observe-only signal surfacing, distinct signal styling, routed signal nugget styling, and split stability/drift signal nuggets on execalc and decisions implemented, integrated, verified, and pushed on stage8/ui-shell-scaffold

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

## Stage 8A: Workspace Shell Spine + Truthful Left Rail (COMPLETE ON stage8/ui-shell-scaffold)
- Workspace shell is live on:
  - /execalc
  - /decisions
- Both surfaces use:
  - WorkspaceShell
  - LiveExecutiveBrief
- Left rail is truthful and injected per surface:
  - /decisions uses persisted recent decisions plus explicit project/chat labels
  - /execalc uses current decision state plus explicit project/chat labels
- Shell defaults were neutralized so no fake branded/sample workspace leaks remain
- Root / redirects to /execalc
- Key commits:
  - 1740404 Make workspace shell left rail data injectable
  - fde873d Feed decisions left rail from persisted records
  - 63977e8 Feed execalc left rail from current decision state
  - 19f6fcf Neutralize shell defaults and label decisions workspace
  - eb2e610 Make workspace shell left rail truthful

## Stage 8B: Stability & Drift Foundations (OBSERVE-ONLY ANOMALY RECORDING + SIGNAL SURFACING + RUNTIME NUGGETS IN PLACE)
- Observe-only stability and drift layers now emit live signals and anomaly arrays in code
- Runtime records non-blocking anomalies for:
  - missing navigation context
  - unspecified governing objective
  - non-ALLOW boundary outcomes
- Executive rail now surfaces:
  - anomaly strings
  - decision boundary state
  - structured runtime nuggets
  - observe-only stability/drift signals
- Service tests cover both anomaly-free and anomaly-present paths
- Product docs added and synced:
  - docs/product/STAGE_8B_STABILITY_AND_DRIFT_FOUNDATIONS.md
  - docs/product/SUBSTRATE_VS_EXECALC_DOCTRINE.md
- Key commits:
  - dbcaf16 Record observe-only Stage 8B anomalies
  - 4b7f361 Surface Stage 8B anomalies in executive rail
  - 7cbb980 Surface decision boundary state in execalc rail
  - d16143a Surface decision boundary state in decisions rail
  - 978b245 Render runtime nuggets in executive rail
  - 99f45fb Prioritize runtime nuggets in executive rail
  - 45cd4f5 Surface observe-only signals in executive rail
  - 81a46be Add signal styling to executive rail nuggets
  - 1db91d7 Route observed signals through signal nugget styling
  - a5386e4 Split stability and drift signal nuggets

## Stage 8C: Navigation Identity Threading (COMPLETE ON stage8/ui-shell-scaffold)
- Orchestration path now carries navigation envelope identity
- /orchestration/run accepts and validates navigation
- /decisions orchestration probe sends navigation
- Decision-path scenario now carries:
  - workspace_id
  - project_id
  - chat_id
  - thread_id
- /execalc now threads navigation identity through /api/decision/run
- Verification:
  - backend suite passed for orchestration + decision-path navigation tranches
  - frontend build and lint passed after /execalc navigation patch
- Key commits:
  - e8a3c32 Add navigation envelope to orchestration scenario model
  - 8901a66 Assert orchestration navigation envelope in tests
  - 852d0ae Thread navigation through orchestration service
  - a4d248d Accept navigation in orchestration API
  - 381c760 Send navigation from decisions orchestration probe
  - 7588ebd Thread navigation through decision path audit
  - c9c6353 Thread execalc navigation through decision request

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
- Define the chat orchestration layer that classifies turns into discuss / decide / action / execute
- Introduce real execution adapters after orchestration exists
- Deepen persistence so execution-boundary events can be queried independently over time

## Future Layer Awareness
- Intelligent Front Door is now recognized as a future architectural layer.
- Chat Orchestration Layer is now recognized as a future architectural layer.
- Neither should bypass the Execution Boundary Engine once action is implicated.

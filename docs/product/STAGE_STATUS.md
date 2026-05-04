# Execalc Stage Status

Last updated: 2026-05-04
Last verified state: Stage 9C complete — GAQP corpus persistence layer live on main. Stage 9A GAQPClaim data model and ActivationBundle, Stage 9B extraction pipeline with seven-test admission gate, Stage 9C Postgres gaqp_claims table with idempotent fingerprint write path and full query surface implemented, tested, and merged to main.

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
  - b15114f Suppress signals when matching anomalies exist
  - 04de4b0 Make decisions anomaly labels explicit
  - 246f586 Prioritize drift anomalies above stability anomalies

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

## Stage 8D: Persistent Memory Architecture + Phase 1 Attachment Mapping + Object Contract + Service Seam + Persistence Path + Admission Path + Retrieval Path + Access Policy (ARCHITECTURE COMPLETE, IMPLEMENTATION NOT STARTED)
- Canonical architecture doc:
  - docs/architecture/PERSISTENT_MEMORY_SYSTEM.md
- Narrow Phase 1 implementation-mapping doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md
- Phase 1 object-contract doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md
- Phase 1 service-seam doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md
- Phase 1 persistence-path doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_PERSISTENCE_PATH.md
- Phase 1 admission-path doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_ADMISSION_PATH.md
- Phase 1 retrieval-path doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_RETRIEVAL_PATH.md
- Phase 1 access-policy doc:
  - docs/architecture/PERSISTENT_MEMORY_PHASE1_ACCESS_POLICY.md
- Current posture:
  - architecture, implementation-mapping, object-contract definition, service-seam definition, persistence-path definition, admission-path definition, retrieval-path definition, and access-policy definition are now documented
  - runtime persistent-memory behavior has not been introduced yet
  - the decision journal remains the current tenant-scoped execution record layer
- Key commits:
  - c183ec7 Define persistent memory system architecture
  - 8f1e75a Thread persistent memory architecture into repo truth
  - 81d2548 Map persistent memory phase 1 attachment seams
  - bdd7891 Define persistent memory phase 1 object contract
  - cde4cfc Define persistent memory phase 1 service seam
  - 52ca9f9 Define persistent memory phase 1 persistence path
  - d25ccf8 Define persistent memory phase 1 admission path
  - 91ce24c Define persistent memory phase 1 retrieval path
  - 199dcee Define persistent memory phase 1 access policy

## Stage 9A: GAQPClaim Data Model + ActivationBundle (COMPLETE ON main)
- `GAQPClaim` frozen dataclass with all 21 fields per architecture lock
- `ActivationBundle` dataclass — output of the future Stage 9D activation engine
- `ClaimProvenance`, `CorroborationProfile` supporting objects
- Canonical enumerations: 24 `ClaimType` values, `ConfidenceLevel`, `AdmissionStatus`, `CorpusScope`, `ActivationScope`, `ExtractionMethod`, `Domain`
- GAQP confidence ladder: Seed 0.50 / Developing 0.72 / Strong 0.91 / Structural 1.00
- Deterministic `compute_fingerprint` (sha256 over tenant + envelope + claim_type + normalized content + scope + schema_version)
- `SCHEMA_VERSION = "stage9_v1"`
- Unit tests: `src/service/gaqp/test_models.py`
- Key commits:
  - 5f0b88c Canonize Stage 9A-0 Architecture Lock
  - b759a95 Stage 9A: GAQPClaim data model and ActivationBundle

## Stage 9B: GAQP Extraction Pipeline (COMPLETE ON main)
- `extract_claims()` — extracts `GAQPClaim` candidates from a `DecisionReport`
- Extraction surface: 5 scalar fields + 4 list fields per architecture lock
  - Scalar: `value_assessment`, `risk_reward_assessment`, `supply_demand_assessment`, `asset_assessment`, `liability_assessment`
  - List: `incentives`, `asymmetries`, `tradeoffs.key_tradeoffs`, `confidence_rationale`
- Seven-test sequential admission gate:
  - Tests 1–4 failure → `rejected`
  - Tests 5–7 failure → `needs_review`
  - All pass → `admitted`
- Activation triggers enriched with `objective:` and `scenario:` context at extraction time
- `admitted_claims()` and `needs_review_claims()` filter helpers
- Unit tests: `src/service/gaqp/test_extraction.py`
- Key commit:
  - fba2b9f Stage 9B: GAQP extraction pipeline

## Stage 9C: GAQP Corpus Persistence Layer (COMPLETE ON main)
- `gaqp_claims` Postgres table added to `docs/db/schema.sql`
  - JSONB columns: `provenance`, `activation_triggers`, `corroboration_profile`, `contradiction_refs`, `support_refs`
  - Unique index on `fingerprint` — idempotent backfill safe
  - Indexes: `(tenant_id, claim_type)`, `(corpus_scope, confidence_score)`, `(tenant_id, source_envelope_id)`
- Write path: `insert_claim()` (single), `insert_claims()` (batch with `InsertSummary`)
  - Only `admitted` claims are written; `rejected` and `needs_review` are never persisted
  - `ON CONFLICT (fingerprint) DO NOTHING` — safe to run extraction twice
- Read path: `get_claim()`, `list_claims()` (with type/scope/confidence filters), `list_claims_by_envelope()`
- Unit tests: `src/service/gaqp/test_corpus.py`
- Key commits:
  - 0964c09 Stage 9C: GAQP corpus persistence layer
  - 9ec0142 Stage 9C: GAQP corpus persistence layer

## Current Architecture Reality
Execalc is now operating as a decision-plus-execution-governance system with a live qualitative knowledge corpus.

Current governed runtime path:
- operator input
- scenario construction
- decision loop engine
- action proposal
- execution boundary engine
- allow / block / recompute / escalate
- execution or human review

Parallel GAQP path (Stage 9A–9C live):
- DecisionReport → extraction pipeline → admission tests → GAQPClaim
- Admitted claims → gaqp_claims (Postgres, idempotent)
- Future: activation engine retrieves claims as ActivationBundle alongside next decision

The Executive Rail remains a display surface.
The decision service remains the current runtime spine.
The GAQP corpus is now a live persistence layer, not yet wired into the decision path.

## Next
- Stage 9D: activation engine — scenario in → `ActivationBundle` out (requires 9B + 9C stable)
- Stage 9E: orchestration rail integration — surface `ActivationBundle` to operator right rail
- Backfill: run 9B+9C extraction against all existing `execution_records` once 9C is confirmed stable
- Stage 7B DB-available integration-test slice, when explicitly pulled forward

## Future Layer Awareness
- Intelligent Front Door is now recognized as a future architectural layer.
- Chat Orchestration Layer is now recognized as a future architectural layer.
- Neither should bypass the Execution Boundary Engine once action is implicated.
- LLM decomposition of paragraph-level `DecisionReport` fields (e.g. `executive_summary`) is deferred to Stage 9 v2.

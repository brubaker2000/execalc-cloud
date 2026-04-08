# Execalc Stage Status

Last updated: 2026-04-08
Last verified state: Stage 7B merged to main (PR #41); 73 tests passing

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

## Stage 7A: Postgres Integration + Service Layer (COMPLETE)
- PR: #39, #40
- Lazy-loaded Postgres driver so unit tests no longer fail on eager import
- Service layer extraction for persistence paths
- Persistence-enabled paths covered for:
  - GET /decision/<envelope_id>
  - GET /decision/recent?limit=N
- Local persistence runbook aligned to current env contract
- Local Postgres happy path proven

## Stage 7B: Decision Comparison Endpoint (COMPLETE)
- PR: #41
- Endpoint: GET /decision/compare
- Deterministic compare engine
- Spec: docs/product/COMPARATIVE_DECISION_MEMORY_SPEC.md
- 73 tests (3 errors = DB integration tests requiring live Postgres, expected)
- Last verified commit: 77a3bf2

## Doctrine Tranche: Session 2026-04-08 (COMPLETE)
- CLAUDE.md written as permanent session anchor
- TRUE_NORTH.md corrected: Assets/Liabilities added as 4th Prime Directive lens
- Wave 1 docs created:
  - docs/vision/GAQP_FOUNDING_CHARTER.md
  - docs/product/EXECALC_QUALITATIVE_FORMULA_LIBRARY_V0_1.md
  - docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_CORPUS_SCHEMA.md
  - docs/vision/ENTERPRISE_QUALITATIVE_SYNTHESIS_THESIS.md
- Wave 2 docs created:
  - docs/architecture/PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md
  - docs/product/SIGNAL_ELEVATION_AND_RAIL_CANDIDACY.md
  - docs/architecture/SUBSTRATE_ROUTING_AND_MODEL_TIERING_DOCTRINE.md
- Wave 3 docs created:
  - docs/architecture/NETWORK_HEURISTIC_PROMOTION_MODEL.md
  - docs/product/GAQP_VS_CONSULTING_CRAFT_POSITIONING.md
  - docs/architecture/EXECALC_CATEGORY_ARCHITECTURE_MAP.md

## Next
- Support Stack Phase 4: condition-aware boundary decisions
- Service layer extraction for GET /decision/<envelope_id> and GET /decision/recent
- Stage 7A DB integration-test slice (skip when Postgres not available)
- Stage 8B.8: memory runtime scaffolding
- Persistent Memory Phase 1 runtime: EKE corpus schema + admission endpoint
- Update CANON.md to index new doctrine docs

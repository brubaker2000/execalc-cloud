# Build State Snapshot — 2026-05-04

## Repo State
- Repo: execalc-cloud
- Branch: main
- Last verified code commit: 9ec0142
- Remote alignment: branch aligned with origin after merge
- Working tree at time of this snapshot:
  - clean after Stage 9C corpus persistence layer merge

## Current Completed Tranche
### Stage 9A — GAQPClaim Data Model + ActivationBundle (COMPLETE ON main)
- `GAQPClaim` frozen dataclass with all 21 fields per `docs/gaqp/STAGE_9A0_ARCHITECTURE_LOCK.md`
- `ActivationBundle` dataclass defined (activation engine deferred to Stage 9D)
- `ClaimProvenance` and `CorroborationProfile` supporting objects
- 24-type `ClaimType` enumeration, GAQP confidence ladder, `compute_fingerprint` (sha256)
- `SCHEMA_VERSION = "stage9_v1"`
- Unit tests in `src/service/gaqp/test_models.py`

### Stage 9B — GAQP Extraction Pipeline (COMPLETE ON main)
- `extract_claims()` extracts `GAQPClaim` candidates from a `DecisionReport`
- 5 scalar fields + 4 list fields per architecture lock extraction surface
- Seven-test sequential admission gate: rejected / needs_review / admitted
- Activation triggers enriched with `objective:` and `scenario:` context
- `admitted_claims()` and `needs_review_claims()` filter helpers
- Unit tests in `src/service/gaqp/test_extraction.py`

### Stage 9C — GAQP Corpus Persistence Layer (COMPLETE ON main)
- `gaqp_claims` Postgres table added to `docs/db/schema.sql`
- JSONB columns for provenance, activation_triggers, corroboration_profile, contradiction_refs, support_refs
- Unique index on fingerprint — idempotent backfill guaranteed
- `insert_claim()`, `insert_claims()` (batch with InsertSummary) — only admitted claims written
- `ON CONFLICT (fingerprint) DO NOTHING` — safe to run extraction twice
- `get_claim()`, `list_claims()`, `list_claims_by_envelope()` read surface
- Unit tests in `src/service/gaqp/test_corpus.py`

## Key Recent Commits
- 9ec0142 Stage 9C: GAQP corpus persistence layer (#53)
- 0964c09 Stage 9C: GAQP corpus persistence layer (#52)
- fba2b9f Stage 9B: GAQP extraction pipeline (#51)
- b759a95 Stage 9A: GAQPClaim data model and ActivationBundle (#50)
- 5f0b88c Canonize Stage 9A-0 Architecture Lock (#49)
- 9a7a403 Fix/merge revert audit fixes (#48)
- d91158b GAQP doctrine, Polymorphia/Quaternation engine, audit remediation (#47)
- ac8ba16 Stage8/UI shell scaffold (#46)

## Current Build Reality
- Stage 9A–9C are complete and live on main.
- The GAQP corpus write path is implemented: DecisionReport → extraction pipeline → admission gate → gaqp_claims (Postgres).
- The corpus is not yet wired into the decision path — activation (9D) and rail integration (9E) are the next stages.
- The decision journal (execution_records) remains the primary runtime persistence layer.
- Repo truth is closed after the Stage 9C persistence layer merge.

## Immediate Next Work
1) Stage 9D — activation engine: scenario in → ActivationBundle out (requires 9B + 9C stable)
2) Stage 9E — orchestration rail integration: surface ActivationBundle to operator
3) Backfill — run Stage 9B+9C extraction against existing execution_records once 9C is confirmed stable under real data

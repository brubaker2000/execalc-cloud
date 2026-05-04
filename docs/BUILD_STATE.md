# Build State Snapshot — 2026-05-04

## Repo State
- Repo: execalc-cloud
- Branch: main
- Last verified code commit: 1f3cd15
- Remote alignment: branch aligned with origin after merge
- Working tree at time of this snapshot:
  - clean after Stage 9D+9E activation engine and rail integration merge

## Current Completed Tranche
### Stage 9D — GAQP Activation Engine (COMPLETE ON main)
- `activate()` in `src/service/gaqp/activation.py` — `ScenarioEnvelope` in → `ActivationBundle` out
- Fetches admitted claims across private / tenant / structural scopes
- Deduplicates by `claim_id` across scope queries
- Universal-scope claims always fire; other scopes require activation trigger keyword match
- Sorted by `confidence_score` DESC, capped at `max_claims` (default 20)
- DB errors return empty bundle — never raises to caller
- Unit tests in `src/service/gaqp/test_activation.py` (19 tests)

### Stage 9E — GAQP Orchestration Rail Integration (COMPLETE ON main)
- `activate()` wired into `run_orchestration()` in `src/service/orchestration/service.py`
- Every turn now carries `corpus_intelligence` (`ActivationBundle.to_dict()`) as a top-level field
- `rail_state` gains `corpus_claims_count` on all turn classes
- `evidence_seeking` promoted from stub to live corpus path — `rail_state` mode is `corpus_evidence`
- `assistant_message` reflects claim count or signals empty corpus for evidence-seeking turns
- Unit tests in `src/service/orchestration/test_service_9e.py` (12 tests)

## Key Recent Commits
- 1f3cd15 Stage9/9d activation engine (#54)
- 9ec0142 Stage 9C: GAQP corpus persistence layer (#53)
- 0964c09 Stage 9C: GAQP corpus persistence layer (#52)
- fba2b9f Stage 9B: GAQP extraction pipeline (#51)
- b759a95 Stage 9A: GAQPClaim data model and ActivationBundle (#50)
- 5f0b88c Canonize Stage 9A-0 Architecture Lock (#49)

## Current Build Reality
- Stage 9A–9E are complete and live on main. The full GAQP loop is executable.
- Runtime path: DecisionReport → extraction → admission → gaqp_claims → activation → ActivationBundle → orchestration rail.
- The ActivationBundle surfaces alongside the DecisionReport — operator-visible, never injected into DecisionReport.
- The decision journal (execution_records) remains the primary runtime persistence layer.
- 103 tests passing across GAQP and orchestration suites.
- Repo truth is closed after the Stage 9D+9E merge.

## Immediate Next Work
1) Backfill — run Stage 9B+9C extraction against existing execution_records to bootstrap the corpus from prior history
2) Stage 10 planning — semantic matching, LLM decomposition, claim lifecycle (deferred from Stage 9 v1)

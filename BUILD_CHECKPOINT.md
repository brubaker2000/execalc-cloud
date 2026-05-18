# Execalc Build Checkpoint
4db151e
Last Stable Commit
4db151e

Branch State
main (2 commits ahead of origin)

Current Stage
Stage 9F complete (GAQP bidirectional service wiring + GAQP v1.0 spec alignment)

Next Stage
Stage 9G: Backfill – run 9B+9C extraction against existing execution_records

Verification Status
✔ python -m compileall -q src/service (passed)
✔ pytest -q (297 tests passed)

Notes
- Stage 9A: GAQPClaim data model and ActivationBundle merged to main.
- Stage 9B: GAQP extraction pipeline with seven-test admission gate merged to main.
- Stage 9C: gaqp_claims Postgres table, idempotent write path, and full read surface merged to main.
- Stage 9D: activation engine (scenario → ActivationBundle) merged to main.
- Stage 9E: orchestration rail integration — corpus_intelligence surfaced on all turn classes merged to main.
- Stage 9F: bidirectional GAQP wiring — ActivationBundle pre-conditions run_decision_loop() before
  execution; extract_claims() + insert_claim() fire post-decision, writing admitted claims to the corpus.
  GAQP v1.0 spec alignment: claim type register corrected to 26 types (asset and liability added);
  confidence ladder expanded to 5 rungs (single_source 0.65 added, strong renamed to corroborated);
  inference_flag, source_location, and standards_package_version added to GAQPClaim schema and DB.
  activation.py decoupled from ScenarioEnvelope via _ScenarioLike Protocol.
  ingress.py (type-specific admission gates, all 26 claim types) committed to main.
- Stage 9A-0 architecture lock canonized in docs/gaqp/STAGE_9A0_ARCHITECTURE_LOCK.md.

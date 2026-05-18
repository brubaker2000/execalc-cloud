# Execalc Build Checkpoint
4d8db6f
Last Stable Commit
4d8db6f

Branch State
main (synced with origin)

Current Stage
Stage 9G complete (GAQP corpus backfill pipeline)

Next Stage
Stage 9H: Tier 2 debt — tags/controlled vocabulary, source_hash, standards loader/registry

Verification Status
✔ python -m compileall -q src/service (passed)
✔ pytest -q (307 passed, 1 skipped)

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
- Stage 9G: GAQP corpus backfill pipeline. run_backfill() reads ok=true execution_records in
  ascending record_id order, reconstructs DecisionReport via _report_from_dict(), runs Stage 9B
  extraction, and persists admitted claims via Stage 9C corpus. Idempotent (fingerprint uniqueness
  constraint). Per-record error isolation — bad records skipped, not fatal. CLI entrypoint with
  --tenant-id, --batch-size, --limit, --dry-run flags. 21 tests. DB migration script added at
  docs/db/migrations/001_stage9f_gaqp_v1_columns.sql — run against live DB before first backfill.
- Stage 9A-0 architecture lock canonized in docs/gaqp/STAGE_9A0_ARCHITECTURE_LOCK.md.

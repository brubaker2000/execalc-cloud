# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-05-04 (America/New_York) — refreshed after Stage 9D+9E

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Backfill — run Stage 9B+9C extraction against existing execution_records
   - Bootstrap the corpus from prior decision history already in Postgres.
   - Requires a live DB connection. Fingerprint idempotency means it is safe to run multiple times.
   - Do not run against production data without verifying 9C is stable under real workload first.

2) Preserve workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

3) Keep branch cleanliness and repo-truth discipline intact
   - Keep changes narrowly scoped.
   - Close the truth loop whenever a tranche lands.

---

## NEXT (Queued)

- Stage 10 planning — semantic / embedding-based claim matching, LLM decomposition of paragraph fields, claim lifecycle automation
- Stage 7A DB-available integration-test slice, when explicitly pulled forward

---

## LATER (Explicitly not now)

- Intelligent Front Door implementation
- Chat Orchestration Layer (classifies turns: discuss / decide / action / execute)
- LLM decomposition of paragraph-level DecisionReport fields (Stage 9 v2)
- Semantic / embedding-based claim matching
- Cross-tenant corpus search UI
- Bridges / subscriber-to-subscriber operability
- Any vector DB expansion beyond explicitly scoped semantic fields

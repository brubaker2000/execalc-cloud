# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-05-04 (America/New_York)

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Stage 9D — activation engine
   - Implement scenario → ActivationBundle retrieval against the live gaqp_claims table.
   - Confidence floor filtering and activation_triggers matching are the core query path.
   - Do not wire into the decision report or inject into prompt material — operator-visible output only.

2) Preserve workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

3) Keep branch cleanliness and repo-truth discipline intact
   - Keep changes narrowly scoped.
   - Close the truth loop whenever a tranche lands.

---

## NEXT (Queued)

- Stage 9E: orchestration rail integration — surface ActivationBundle to operator right rail
- Backfill: run Stage 9B+9C extraction against existing execution_records (once 9C is confirmed stable under real data)
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

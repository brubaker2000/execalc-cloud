# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-03-29 (America/New_York)

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Define the next narrow Stage 8 move after decisions anomaly labeling
   - Choose the next smallest governed increment.
   - Prefer runtime honesty, narrow hardening, or truthful surfacing over broad new feature area.
   - Do not invent a wider navigation or orchestration framework until a concrete need appears.

2) Preserve workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

3) Keep Stage 8 work isolated
   - Leave unrelated untracked docs out of Stage 8 commits.
   - Keep branch cleanliness and repo-truth discipline intact.

---

## NEXT (Queued)

- Stage 8 observe-only stability and drift follow-through
- Stage 7A DB-available integration-test slice, when explicitly pulled forward
- Stage 7B: `/decision/compare`
- Stage 7C: multi-objective comparison logic

---

## LATER (Explicitly not now)

- Intelligent Front Door implementation
- Bridges / subscriber-to-subscriber operability
- Any vector DB expansion beyond explicitly scoped semantic fields
- Any new feature surface that outruns the current operational rails

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

1) Thread persistent-memory architecture into repo truth
   - Update repo-truth surfaces to acknowledge `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md` and commit `c183ec7`.
   - Keep the next move architectural and documentary, not runtime implementation.
   - Do not widen beyond the documented phased rollout until explicitly pulled forward.

2) Preserve workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

3) Keep repo-truth work isolated
   - Keep the persistent-memory threading pass scoped to the relevant truth surfaces only.
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

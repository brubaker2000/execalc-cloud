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

1) Final repo-truth alignment for signal-surfacing tranche
   - Sync status surfaces to reflect 45cd4f5.
   - Record that the executive rail now surfaces observe-only stability/drift signals on both `/execalc` and `/decisions`.
   - Remove stale language that still stops at the runtime-nugget tranche.

2) Define the next narrow Stage 8 move after signal surfacing
   - Choose the next smallest governed increment.
   - Prefer runtime honesty, narrow hardening, or truthful surfacing over broad new feature area.
   - Do not invent a wider navigation or orchestration framework until a concrete need appears.

3) Protect workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

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

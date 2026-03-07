# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-03-07 (America/New_York)

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Stage 7A integration-test slice
   - Add a DB-available integration-test path for local Postgres persistence.
   - Skip cleanly when local Postgres is not available.
   - Cover `/decision/run`, `/decision/<envelope_id>`, and `/decision/recent`.

2) Repo truth alignment
   - Keep Stage 7A status, runbook, and next actions synchronized.
   - Preserve the doctrine that plumbing and cognition advance together.

3) Protect workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

---

## NEXT (Queued)

- Stage 7B: `/decision/compare`
- Stage 7C: multi-objective comparison logic
- Refine the decision artifact into a comparable executive memory unit

---

## LATER (Explicitly not now)

- Intelligent Front Door implementation
- Bridges / subscriber-to-subscriber operability
- Any UI work
- Any vector DB expansion beyond explicitly scoped semantic fields
- Any new feature surface that outruns the current operational rails

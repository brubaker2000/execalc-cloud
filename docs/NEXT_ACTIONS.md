# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-03-05 (America/New_York)

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Stage 6 — Persistence hardening + operational defaults
   - Wire persistence in a way that is tenant-safe, testable, and operationally predictable.
   - Deliverables (minimum):
     - Clear enable/disable rules (env flags) with safe defaults
     - Local runbook alignment (docs/product/LOCAL_PERSISTENCE_RUNBOOK.md)
     - CI-safe tests (unit tests do not require DB env vars)
     - Tight tenant scoping guarantees for all read/write paths

2) Documentation hygiene (keep repo as source of truth)
   - Keep stage-map pointer files clean (no conflict markers)
   - Ensure NEXT_ACTIONS aligns with STAGE_STATUS at all times

---

## NEXT (Queued)

- Decide whether persistence hardening lands as:
  - a single Stage 6 PR, or
  - 6A/6B/6C sub-stages (recommended if scope expands)
- Add a small “boot packet” script to print canonical rehydration docs in one command.

---

## LATER (Explicitly not now)

- Any UI work
- Any vector DB expansion beyond explicitly scoped semantic fields
- Any new feature surface not required by Stage 6 persistence hardening

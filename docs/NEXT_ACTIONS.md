# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-03-26 (America/New_York)

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Repo truth alignment for Stage 8
   - Keep Stage 8A, 8B, and 8C status synchronized across repo truth files.
   - Eliminate stale instructions that still describe `/execalc` UI threading as pending.
   - Preserve the doctrine that plumbing and cognition advance together.

2) Define the next narrow build move after navigation threading
   - Choose the next smallest governed Stage 8 increment.
   - Prefer truth-surface alignment or narrowly scoped runtime hardening over broad new surface area.
   - Do not invent a wider navigation framework until a concrete need appears.

3) Protect workstation reliability
   - Prefer short, verifiable commands in this shell environment.
   - Avoid fragile long heredocs and long quoted command chains where possible.

---

## NEXT (Queued)

- Stage 8 repo-truth cleanup across BUILD_STATE / BUILD_COCKPIT / status surfaces
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

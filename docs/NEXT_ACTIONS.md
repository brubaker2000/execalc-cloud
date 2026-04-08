# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-04-08 (America/New_York)

Source of truth for completion claims:
- docs/product/STAGE_STATUS.md

---

## NOW (1–3 items only)

1) Support Stack Phase 4
   - Condition-aware boundary decisions.
   - This is the current active build layer.

2) Service layer extraction
   - Extract service layer for GET /decision/<envelope_id> and GET /decision/recent.
   - Align with service layer pattern established in Stage 7A.

3) Stage 7A DB integration-test slice
   - Add a DB-available integration-test path for local Postgres persistence.
   - Skip cleanly when local Postgres is not available.
   - Cover `/decision/run`, `/decision/<envelope_id>`, and `/decision/recent`.

---

## NEXT (Queued)

- Stage 8B.8: memory runtime scaffolding (once support stack stable)
- Persistent Memory Phase 1 runtime — EKE corpus schema + admission endpoint
- Wave 3 repo promotion docs: NETWORK_HEURISTIC_PROMOTION_MODEL.md, GAQP_VS_CONSULTING_CRAFT_POSITIONING.md
- Update CANON.md to index all Wave 1+2 docs written this session

---

## LATER (Explicitly not now)

- Stage 7B: `/decision/compare` — COMPLETE (PR #41 merged)
- Stage 7C: multi-objective comparison logic
- Intelligent Front Door implementation
- Bridges / subscriber-to-subscriber operability
- Any UI work
- Any vector DB expansion beyond explicitly scoped semantic fields
- Any new feature surface that outruns the current operational rails


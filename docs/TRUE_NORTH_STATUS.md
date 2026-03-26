# Execalc Operational Status

⚠️ This file is NOT doctrine.

Canonical True North doctrine lives in:
- `docs/vision/TRUE_NORTH.md`
- `docs/vision/STAGE_MAP.md`
- `docs/vision/CANONIZATION_PROTOCOL.md`
- `docs/EXECALC_INVARIANTS.md`

This file tracks the current build tranche and enforcement posture only.

---

## Current Tranche
Tranche: Stage 8 — UI Shell Scaffold + Navigation Identity Threading  
Subphase: Repo-truth alignment after live navigation seam closure

---

## Last Verified Gate
Branch: `stage8/ui-shell-scaffold`  
Last verified code commit: `c9c6353`  
Frontend build: PASS  
Frontend lint: PASS  
Recent backend navigation tranches: PASS before current doc-alignment pass  
Remote alignment: branch aligned with origin after push

---

## Notes
- `/execalc` and `/decisions` both run through `WorkspaceShell` with `LiveExecutiveBrief`.
- Left rail behavior is truthful by surface:
  - `/decisions` reflects persisted recent decisions
  - `/execalc` reflects current decision state
- Stage 8B observe-only stability/drift scaffolding exists.
- Navigation identity now threads through:
  - orchestration path
  - decision path
  - `/execalc` request path
- Current work is focused on bringing repo truth surfaces into alignment with actual branch state.

This document must never redefine system doctrine.

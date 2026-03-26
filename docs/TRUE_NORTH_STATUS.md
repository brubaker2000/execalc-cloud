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
Subphase: Truthful shell completion and final repo-truth alignment

---

## Last Verified Gate
Branch: `stage8/ui-shell-scaffold`  
Last verified code commit: `eb2e610`  
Frontend build: PASS  
Frontend lint: PASS  
Recent backend navigation tranches: PASS before current doc-alignment pass  
Remote alignment: branch aligned with origin after push

---

## Notes
- `/execalc` and `/decisions` both run through `WorkspaceShell` with `LiveExecutiveBrief`.
- Left rail behavior is truthful by surface:
  - `/decisions` reflects persisted recent decisions plus explicit project/chat context
  - `/execalc` reflects current decision state plus explicit project/chat context
- Stage 8B observe-only stability/drift scaffolding exists.
- Navigation identity now threads through:
  - orchestration path
  - decision path
  - `/execalc` request path
- Current work is focused on the final repo-truth alignment pass after truthful shell completion.

This document must never redefine system doctrine.

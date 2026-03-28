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
Tranche: Stage 8 — UI Shell Scaffold + Navigation Identity Threading + Observe-Only Stability Signals  
Subphase: Final repo-truth alignment after decisions-rail boundary surfacing

---

## Last Verified Gate
Branch: `stage8/ui-shell-scaffold`  
Last verified code commit: `d16143a`  
Frontend build: PASS  
Frontend lint: PASS  
Recent backend, Stage 8B anomaly, rail-surfacing, execalc-boundary, and decisions-boundary tranches: PASS before current doc-alignment pass  
Remote alignment: branch aligned with origin after push

---

## Notes
- `/execalc` and `/decisions` both run through `WorkspaceShell` with `LiveExecutiveBrief`.
- Left rail behavior is truthful by surface:
  - `/decisions` reflects persisted recent decisions plus explicit project/chat context
  - `/execalc` reflects current decision state plus explicit project/chat context
- Stage 8B observe-only stability/drift anomaly recording exists and is surfaced in the executive rail.
- `/execalc` now surfaces decision execution-boundary state directly from the decision response.
- `/decisions` now surfaces selected decision execution-boundary state directly from persisted decision detail.
- Navigation identity now threads through:
  - orchestration path
  - decision path
  - `/execalc` request path
- Current work is focused on the final repo-truth alignment pass after decisions-rail boundary surfacing.

This document must never redefine system doctrine.

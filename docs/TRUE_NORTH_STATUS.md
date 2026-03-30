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
Subphase: Post-drift-anomaly-visual repo-truth alignment closed

---

## Last Verified Gate
Branch: `stage8/ui-shell-scaffold`  
Last verified code commit: `246f586`  
Frontend build: PASS  
Frontend lint: PASS  
Recent backend, Stage 8B anomaly, boundary-surfacing, runtime-nugget, signal-surfacing, signal-styling, signal-routing, signal-split, signal-suppression, decisions-anomaly-label, anomaly-priority, and drift-anomaly-visual tranches: PASS  
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
- The executive rail now renders structured runtime nuggets instead of only plain insight strings.
- The executive rail now surfaces observe-only stability/drift signals on both `/execalc` and `/decisions`.
- Signal nuggets now render with distinct styling in `LiveExecutiveBrief`.
- Observed signals now route through `kind: "signal"` on both `/execalc` and `/decisions`.
- Stability and drift signals now surface as distinct nuggets with distinct labels and priorities on both pages.
- Matching anomalies now suppress their lower-priority sibling signals on both `/execalc` and `/decisions`.
- `/decisions` now labels anomaly categories explicitly as Stability Anomaly and Drift Anomaly instead of a generic observed anomaly.
- Drift anomalies now rank above stability anomalies on both `/execalc` and `/decisions` for clearer executive prioritization.
- Drift anomalies now render with a distinct visual treatment in `LiveExecutiveBrief`, separate from the default anomaly tone.
- Navigation identity now threads through:
  - orchestration path
  - decision path
  - `/execalc` request path
- Current work is focused on choosing the next narrow Stage 8 increment after the drift-anomaly-visual tranche, with repo-truth alignment closed.

This document must never redefine system doctrine.

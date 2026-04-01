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
Subphase: Persistent-memory retrieval-path repo-truth alignment closed

---

## Last Verified Gate
Branch: `stage8/ui-shell-scaffold`  
Last verified code commit: `91ce24c`  
Frontend build: PASS  
Frontend lint: PASS  
Recent backend, Stage 8B anomaly, boundary-surfacing, runtime-nugget, signal-surfacing, signal-styling, signal-routing, signal-split, signal-suppression, decisions-anomaly-label, anomaly-priority, drift-anomaly-visual, persistent-memory architecture, persistent-memory attachment-map, persistent-memory object-contract, persistent-memory service-seam, persistent-memory persistence-path, persistent-memory admission-path, and persistent-memory retrieval-path tranches: PASS  
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
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md` now exists as the canonical architecture draft for governed persistent memory.
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md` now exists as the narrow Phase 1 implementation map for attaching memory beside the current decision journal.
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md` now exists as the first explicit Phase 1 memory object contract.
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md` now exists as the first governed Phase 1 memory service boundary.
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_PERSISTENCE_PATH.md` now exists as the first separate Phase 1 memory persistence path.
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ADMISSION_PATH.md` now exists as the first explicit Phase 1 memory admission path.
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_RETRIEVAL_PATH.md` now exists as the first governed Phase 1 memory retrieval path.
- Current work should remain architectural and documentary unless runtime memory implementation is explicitly pulled forward beyond the documented phased rollout.

This document must never redefine system doctrine.

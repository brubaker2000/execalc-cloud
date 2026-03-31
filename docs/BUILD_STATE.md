# Build State Snapshot — 2026-03-29

## Repo State
- Repo: execalc-cloud
- Branch: stage8/ui-shell-scaffold
- Last verified code commit: 81d2548
- Remote alignment: branch aligned with origin after push
- Working tree at time of this snapshot:
  - clean after persistent-memory-phase1-attachment-map tranche

## Current Completed Tranche
### Stage 8A — Workspace Shell Spine + Truthful Left Rail (completed on stage8/ui-shell-scaffold)
- Workspace shell is live on:
  - /execalc
  - /decisions
- Both surfaces use:
  - WorkspaceShell
  - LiveExecutiveBrief
- Left rail behavior is truthful by surface:
  - /decisions reads persisted recent decisions and explicit project/chat context
  - /execalc reads current decision state and explicit project/chat context
- Shell defaults were neutralized so fake branded/sample workspace state no longer leaks into runtime surfaces
- Root / redirects to /execalc

### Stage 8B — Stability & Drift Foundations (observe-only anomaly recording + signal surfacing + runtime nuggets in place)
- Observe-only anomaly recording now runs in code for stability/drift audit layers
- Executive rail now surfaces anomaly strings from audit payloads on both `/execalc` and `/decisions`
- `/execalc` now also surfaces decision execution-boundary state directly from the decision response
- `/decisions` now surfaces the selected decision execution-boundary state directly from persisted decision detail
- The executive rail now renders structured runtime nuggets instead of only plain insight strings
- The executive rail now surfaces observe-only stability/drift signals on both `/execalc` and `/decisions`
- Signal nuggets now render with distinct styling in `LiveExecutiveBrief`
- Observed signals now route through `kind: "signal"` on both `/execalc` and `/decisions`
- Stability and drift signals now surface as distinct nuggets with distinct labels and priorities on both pages
- Matching anomalies now suppress their lower-priority sibling signals on both `/execalc` and `/decisions`
- `/decisions` now labels anomaly categories explicitly as Stability Anomaly and Drift Anomaly instead of a generic observed anomaly
- Drift anomalies now rank above stability anomalies on both `/execalc` and `/decisions` for clearer executive prioritization
- Drift anomalies now render with a distinct visual treatment in `LiveExecutiveBrief`, separate from the default anomaly tone
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md` now defines the canonical governed persistent-memory architecture
  - `docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md` now maps the narrow Phase 1 attachment path onto current service/journal seams
- Stability/drift doctrine now matches live observe-only anomaly behavior
- Substrate-vs-Execalc doctrine doc was added to keep product framing honest

### Stage 8C — Navigation Identity Threading (completed on stage8/ui-shell-scaffold)
- NavigationEnvelope exists on orchestration-side scenario flow
- /orchestration/run accepts and validates navigation
- Decisions-page orchestration probe sends navigation
- Decision-path Scenario includes:
  - workspace_id
  - project_id
  - chat_id
  - thread_id
- /execalc now threads navigation identity through /api/decision/run
- Frontend verification passed:
  - npm run build
  - npm run lint
- Backend verification passed during orchestration/decision-path navigation tranches

## Key Recent Commits
- 81d2548 Map persistent memory phase 1 attachment seams
- 8f1e75a Thread persistent memory architecture into repo truth
- c183ec7 Define persistent memory system architecture
- b25d03d Refresh repo truth for drift anomaly visual treatment
- a65b334 Give drift anomalies distinct visual treatment
- 24e03a5 Refresh repo truth for anomaly-priority tranche
- 246f586 Prioritize drift anomalies above stability anomalies
- 4da04c5 Refresh repo truth for decisions anomaly labeling
- 04de4b0 Make decisions anomaly labels explicit
- ca1f4c0 Update Stage 8B foundations for signal suppression
- da0ca44 Refresh repo truth for signal-suppression tranche
- b15114f Suppress signals when matching anomalies exist
- bdb5f49 Refresh repo truth for signal-split tranche
- a5386e4 Split stability and drift signal nuggets
- cb3947d Refresh repo truth for signal-routing tranche
- 1db91d7 Route observed signals through signal nugget styling
- eee7a08 Refresh repo truth for signal-styling tranche
- 81a46be Add signal styling to executive rail nuggets
- 1d117e3 Update Stage 8B foundations for signal surfacing
- 611b374 Refresh repo truth for signal-surfacing tranche
- 45cd4f5 Surface observe-only signals in executive rail
- 99f45fb Prioritize runtime nuggets in executive rail
- 1a4c6aa Refresh repo truth for runtime nugget rail
- 978b245 Render runtime nuggets in executive rail
- dc0c65a Refresh repo truth for decisions rail boundary
- d16143a Surface decision boundary state in decisions rail
- e46d875 Refresh repo truth for decision-boundary rail
- 7cbb980 Surface decision boundary state in execalc rail
- 80025e9 Refresh repo truth for rail anomaly surfacing
- 4b7f361 Surface Stage 8B anomalies in executive rail
- 76a753e Refresh repo truth for Stage 8B anomaly tranche
- dbcaf16 Record observe-only Stage 8B anomalies
- 03b3224 Update repo truth for truthful shell tranche
- eb2e610 Make workspace shell left rail truthful
- d04d406 Align Stage 8 repo truth surfaces
- c9c6353 Thread execalc navigation through decision request
- 7588ebd Thread navigation through decision path audit
- 381c760 Send navigation from decisions orchestration probe
- a4d248d Accept navigation in orchestration API
- 852d0ae Thread navigation through orchestration service
- 8901a66 Assert orchestration navigation envelope in tests
- e8a3c32 Add navigation envelope to orchestration scenario model
- 19f6fcf Neutralize shell defaults and label decisions workspace
- 63977e8 Feed execalc left rail from current decision state
- fde873d Feed decisions left rail from persisted records
- 1740404 Make workspace shell left rail data injectable

## Current Build Reality
- The Stage 8 shell remains truthful on both rails, and the repo now includes both the canonical persistent-memory architecture draft and the narrow Phase 1 attachment map.
- Repo truth is closed again after the persistent-memory Phase 1 attachment-map tranche.
- The next build decision should remain architectural and documentary unless the memory rollout is explicitly pulled forward.

## Immediate Next Work
1) Choose the next smallest governed Stage 8 increment
2) Keep the next move architectural and documentary unless memory implementation is explicitly pulled forward
3) Preserve workstation-safe execution discipline

# Build State Snapshot — 2026-03-26

## Repo State
- Repo: execalc-cloud
- Branch: stage8/ui-shell-scaffold
- Last verified code commit: c9c6353
- Remote alignment: branch aligned with origin after push
- Working tree at time of this snapshot:
  - repo-truth documentation updates in progress

## Current Completed Tranche
### Stage 8A — Workspace Shell Spine (completed on stage8/ui-shell-scaffold)
- Workspace shell is live on:
  - /execalc
  - /decisions
- Both surfaces use:
  - WorkspaceShell
  - LiveExecutiveBrief
- Left rail behavior is truthful by surface:
  - /decisions reads persisted recent decisions
  - /execalc reads current decision state
- Shell defaults were neutralized so fake branded/sample workspace state no longer leaks into runtime surfaces
- Root / redirects to /execalc

### Stage 8B — Stability & Drift Foundations (observe-only scaffold in place)
- Observe-only anomaly slots were added in code
- Stability/drift doctrine scaffolding exists in product docs
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
- The live Stage 8 UI seam that remained at handoff time has been closed.
- Repo truth is being brought into alignment with the actual branch state.
- The next build decision should be a narrow Stage 8 move, not a broad new framework.

## Immediate Next Work
1) Finish repo-truth cleanup across remaining status/cockpit surfaces
2) Choose the next smallest governed Stage 8 increment
3) Preserve workstation-safe execution discipline

# Execalc Cloud — Next Actions (Now / Next / Later)

Purpose:
- This file is the daily execution spine for the build.
- It is updated at the start and end of each shift.
- PRs should reference which "NOW" item(s) they close.
- If chat memory conflicts with this file, this file wins.

Last updated: 2026-02-23 (America/New_York)

---

## NOW (1–3 items only)

1) Stage 3 Delegation Guardrails — enforce PR-only merges, CODEOWNERS for sensitive paths, and required CI checks.
   - Deliverables:
     - .github/CODEOWNERS finalized (replace placeholder handle, include src/ enforcement paths)
     - GitHub branch protection configured for main (PR required, status checks required, no force push)
     - CI workflows confirmed as required checks

2) Stage 2 Completion Hygiene — eliminate any remaining non-production-path smoke/test dependencies.
   - Deliverables:
     - smoke scripts use known registered tenant(s) only
     - gates rely on /livez and /readyz (production posture)
     - no dev harness required for deploy validation

3) Boot & Handoff Protocol — make daily chat resets deterministic and auditable.
   - Deliverables:
     - documented Mouse shift handoff template (PR description format)
     - repo boot packet command(s) identified and documented (exsync + canon reads)

---

## NEXT (Queued)

- Add docs/decisions/ADR-0001-delegation-guardrails.md summarizing the delegation/merge policy.
- Add scripts/boot_packet.sh to print canonical "rehydration" docs in one command.
- Tighten CODEOWNERS to include src/service/auth/** and src/service/tenant/** after confirming exact paths.

---

## LATER (Explicitly not now)

- Stage 4 Reflex classification scaffold
- Stage 5 Executive Knowledge Engine wiring
- Any UI work
- Any vector database expansion beyond clearly scoped semantic fields

## 2026-03-01
- Cloud Run: set EXECALC_CONNECTOR_CREDENTIAL_REQUIRED to {"*":[]}
- Reason: allow echo connector smoke tests to run without credentials; credential gating reserved for real connectors


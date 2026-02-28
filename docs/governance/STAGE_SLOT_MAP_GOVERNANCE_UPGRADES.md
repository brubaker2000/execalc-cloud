# Stage Slot Map — Governance Thinking Upgrades (Pointer)

Purpose:
- Assign each governance upgrade to the correct stage.
- Prevent premature wiring.
- Keep Stage 2 disciplined while preserving future intent.

---

## Stage 2 — Governance Spine & Multi-Tenant Structural Integrity (NOW)

Allowed:
- Tenant enforcement invariants remain deterministic.
- Smoke harness hardening that does not weaken production posture.
- Remove accidental test/tool coupling (example: pytest dependency inside unittest suite).
- Boot and rehydration procedure that forces repo anchoring.

Not allowed:
- Canon enforcement that introduces new runtime logic paths.
- Ingress classification or memory wiring.
- Reflex activation gating.

---

## Stage 3 — Delegation Guardrails + Canon Spine (NEXT)

Allowed:
- Branch protection, PR-only merges, required checks.
- CODEOWNERS finalized for sensitive paths (docs, CI, infra, runtime enforcement code).
- Repo handoff templates and boot packet scripting.

Docs-only additions (no runtime enforcement yet):
- Canon ID conventions (PD-01, C7-01..07, INV-###, ADR-####, TEN-###).
- Canon header standard.
- Canon Registry design and initial registry file.

Optional enforcement (late Stage 3, if safe):
- CI rules that require review/labeling when canon paths change.

---

## Stage 4 — Reflex Scaffold (LATER)

Belongs here:
- Activation density gates.
- Reflex reliability thresholds.
- Regression tests and guardrails for reflex triggering.

---

## Stage 5 — Knowledge Engine Wiring (LATER)

Belongs here:
- Ingress classification taxonomy (Canon/Policy/Evidence/Commentary/Hypothesis/Task).
- Metadata requirements and validation.
- Promotion authority rules and audit trail.
- Memory classes and promotion paths (active/deferred/reference-only, dormant memory).

---

## Stage 6 — Polymorphic Runtime (LATER)

Belongs here:
- Cross-framework arbitration at scale.
- Multi-lens conflict handling in complex runtime contexts.
- Hardening of any cognition-layer behavior that can affect multi-tenant correctness.

---

## Canonical References
- docs/NEXT_ACTIONS.md
- docs/STAGE_MAP.md (pointer)
- docs/EXECALC_INVARIANTS.md
- docs/invariants/INV-001_ai_is_subroutine.md
- docs/EDITOR_ONLY_DEV_PROTOCOL.md
- docs/governance/FUTURE_GOVERNANCE_EXPANSIONS.md

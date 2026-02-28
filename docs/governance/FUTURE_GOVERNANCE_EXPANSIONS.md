# Future Governance Expansions (Design-Locked, Not Yet Implemented)

Purpose:
- Preserve governance upgrades as repo-tracked intent.
- Prevent chat-only doctrine.
- Explicitly defer enforcement until the correct stage so we do not wire cognition prematurely.

Status:
- This document is a design register, not executable policy.
- No runtime logic is authorized by this file alone.

---

## A. Canon Registry + Machine-Checkable Doctrine (Planned)

### Problem
Governance doctrine drifts when it is only described conversationally. We need canon to be indexable, reviewable, and eventually enforceable.

### Design (Docs-First)
1) Canon IDs (stable identifiers)
- Prime Directive: PD-01
- Core 7 frameworks: C7-01 through C7-07
- Invariants: INV-### (INV-001 already exists)
- Tenant governance: TEN-### (reserved)
- ADRs: ADR-####

2) Canon header standard (for canon-eligible docs)
Each canon doc SHOULD start with a small header block:
- Canon-ID:
- Title:
- Status: draft | active | locked
- Owner:
- Last-reviewed:
- Change-notes: (short)

3) Canon Registry index
Create a registry file that lists all canon objects and their locations:
- docs/canon/CANON_REGISTRY.md (planned)

### Enforcement (Deferred)
- CI checks and drift detection are deferred until Stage 3+.
- No enforcement is permitted in Stage 2.

### Stage Slot
- Docs-first design: Stage 3
- CI enforcement: Stage 3 (late) / Stage 4 (if it touches runtime gates)

---

## B. Doctrine Drift Detection (Planned)

### Problem
Edits to doctrine (Prime Directive, invariants, canon) can silently change system behavior and investor-facing truth.

### Design
1) Doctrine Change Rules
Changes to canon docs require:
- PR (never direct-to-main)
- CODEOWNERS approval on canon paths
- A short ADR or changelog entry for high-impact doctrine

2) Machine-checkable drift (future)
Options:
- Touched-canon detector in CI: if files under docs/canon/** or docs/invariants/** changed, require:
  - PR label "doctrine-change"
  - or presence of a corresponding ADR file

### Stage Slot
- Policy + CODEOWNERS: Stage 3
- CI automation: Stage 3 (late) / Stage 4

---

## C. Ingress Classification Hygiene (Planned)

### Problem
If all incoming information is treated equally, the system cannot preserve truth, provenance, or promotion authority.

### Taxonomy (Target)
Ingress items must be classified as one of:
- Canon
- Policy
- Evidence
- Commentary
- Hypothesis
- Task

Required metadata (target):
- source
- timestamp
- tenant_id
- classification
- confidence (optional)
- promotion_authority

Promotion rules (target):
- Canon promotion requires explicit authority and an audit trail.
- Evidence can be promoted into Policy/Canon only with citations and review.

### Stage Slot
- Design + docs: Stage 5
- Runtime enforcement: Stage 5 (late) / Stage 6 (if it intersects polymorphic arbitration)

---

## D. Activation Density Gates (Planned)

### Problem
Reflexes should not become brittle or noisy.

### Design (Target)
- Reflexes have confidence + activation density thresholds.
- Low-density reflexes remain available but do not auto-fire.
- Regression tests for high-frequency reflex paths.

### Stage Slot
- Design + tests: Stage 4
- Runtime gating: Stage 4 (late)

---

## E. Non-Negotiables (Already Active)

These are already binding today:
- Repo is the source of truth; chat is not authoritative.
- No stage skipping.
- Infrastructure before cognition.
- Governance before intelligence.
- Editor-only development.

References:
- docs/EXECALC_INVARIANTS.md
- docs/invariants/INV-001_ai_is_subroutine.md
- docs/EDITOR_ONLY_DEV_PROTOCOL.md
- docs/NEXT_ACTIONS.md
- docs/STAGE_MAP.md (pointer)

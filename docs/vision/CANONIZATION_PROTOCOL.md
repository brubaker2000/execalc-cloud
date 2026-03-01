# Canonization Protocol

This document governs how ideas move from chat into the constitutional spine of Execalc.

---

## Core Principle

Chat is ideation.  
Repo is doctrine.  
Code is enforcement.

If an idea is not committed to the repository in structured form, it does not exist.

---

## The Three-State Rule

Every idea must pass through three states:

### Stage A — Concept (Chat Only)
- Exists only in an ideation thread
- May be exploratory, incomplete, speculative
- Not considered binding

### Stage B — Canonical Spec (Repo)
- Distilled into structured markdown
- Stored in an appropriate directory (`vision`, `runtime`, `governance`, or `capabilities`)
- Includes:
  - Clear definition
  - Object model (if applicable)
  - Governance implications
  - Required primitives
  - Risks and edge cases
- Versioned via git commit

Only after Stage B is complete may implementation begin.

### Stage C — Code Enforcement
- Implemented in `/src`
- Covered by:
  - Unit tests
  - Invariant tests (if applicable)
  - Regression tests (if applicable)
- Logged in decision log if doctrine-level impact

---

## Dev Chat Operating Rule

When a feature chat is brought into dev chat, the dev chat must:

1. Extract doctrine
2. Extract object model
3. Identify invariants
4. Identify required primitives
5. Identify spine impact
6. Generate structured repo artifacts

The dev chat does not implement directly from ideation.

---

## Conflict Resolution

If:
- Chat conflicts with repo → repo wins.
- Repo conflicts with invariants → invariants win.
- Code conflicts with invariants → tests must fail until corrected.

All doctrine changes must be deliberate, versioned, and logged.

---

## Required Canon Files

At minimum, the following files anchor every new dev chat:

- `docs/vision/TRUE_NORTH.md`
- `docs/vision/STAGE_MAP.md`
- `docs/EXECALC_INVARIANTS.md`
- `docs/vision/CANONIZATION_PROTOCOL.md`

No build decision should bypass these anchors.

---

## Drift Prevention Rule

No capability may be implemented unless:

1. It has a canonical spec.
2. It passes the Spine Non-Preclusion Checklist.
3. It aligns with TRUE_NORTH.
4. It does not violate invariants.

Skipping canonization introduces entropy and is prohibited.

---

## Constitutional Checkpoint

Major structural changes must be committed as explicit checkpoints.

A checkpoint commit message must state:

"Constitutional update: [brief description]"

This ensures historical traceability of doctrine evolution.

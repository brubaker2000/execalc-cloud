# Execalc Canonical Decisions Log (Append-Only)

This file is the single landing zone for every “locked” decision.
Rule: if it is locked, it gets logged here the same day and committed.

## How to log a decision (template)

### YYYY-MM-DD — DEC-XXX — <Title>
- **Status:** Locked
- **Scope:** Global runtime | Tenant-private | Build-only | Documentation-only
- **Owner:** Operator (Jeff) | GM
- **Why it matters:** One sentence
- **Decision:** The crisp rule or commitment (no prose)
- **Implications:** What it changes, what it constrains
- **Implementation pointers:** files/paths to enforce it (tests, code, docs)
- **Evidence:** commit hash(es), PR link(s) if applicable

---

## Decisions

### 2026-02-01 — DEC-001 — Canonical documentation landing zone
- **Status:** Locked
- **Scope:** Build-only
- **Owner:** Operator (Jeff) + GM
- **Why it matters:** Prevents drift and “conveyor belt” loss; every locked decision becomes durable, reviewable, and enforceable.
- **Decision:** All locked decisions must be written to `docs/canon/05_DECISIONS_LOG.md` and pushed to the repo.
- **Implications:** No future “locked” rule is considered real until it is committed.
- **Implementation pointers:** `docs/canon/*` (index, governance locks, architecture, runbooks, GM handoff)
- **Evidence:** (to be filled on commit)


# Execalc Invariants Index

This directory contains **binding architectural invariants**. These are non-negotiable constraints for Execalc cloud builds.

**Rule:** If an invariant conflicts with an implementation detail, the implementation must change.

## Active Invariants

- **INV-001 — AI Is a Subroutine, Not the System**
  - Status: Binding architectural invariant
  - File: `INV-001_ai_is_subroutine.md`
  - Summary: Deterministic-first architecture; Postgres is system of record; embeddings are attributes (not a silo); tenant isolation must never depend on AI; explainable retrieval; graceful degradation.

## Enforcement

Invariants are enforced through:
- Design review (PR checklist / gate review)
- Repository documentation (canonical “True North”)
- Tests (where feasible) and CI checks to prevent drift

## Adding a New Invariant

Every new invariant must include:
- ID (e.g., `INV-002`)
- Status (binding vs guideline)
- Purpose
- Rules (must/forbidden language)
- Enforcement notes (tests / gates / review hooks)

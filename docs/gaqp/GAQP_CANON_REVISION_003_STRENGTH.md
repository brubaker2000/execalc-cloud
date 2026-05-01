# GAQP Canon Revision 003
## Strength as the 21st Canonical Claim Type

**Status:** Canonized
**Revision ID:** GAQP-CR-003
**Date:** 2026-05-01
**Authority:** Execalc GAQP Standards Body
**Taxonomy version prior:** 1.2 (20 types)
**Taxonomy version after:** 1.3 (21 types)

---

## I. Governing Rationale

Strength cannot be safely collapsed into Declaration of Value or Tendency because its evidence requirement, competitive orientation, and internal-capability specificity require distinct runtime handling — and because organizations must be able to toggle, query, and activate Strength claims directly without translating through adjacent types.

The decisive distinction is:

> A Strength is a confirmed internal capability or advantage. A Declaration of Value is an assertion of worth. A Tendency is a market or behavioral pattern. Strength is none of these — it is demonstrated organizational capability that creates competitive differentiation.

---

## II. Definition

A confirmed internal capability, resource, or positional advantage that provides competitive differentiation. A Strength must be evidenced — demonstrated through performance, outcome, or structural assessment — not merely declared. It is always internal in origin and positive in polarity.

---

## III. Why Existing Types Are Insufficient

| Adjacent Type | Why Strength Is Different |
|---|---|
| **Declaration of Value** | A Declaration of Value asserts what something is worth or capable of. A Strength is a confirmed competitive capability — it has been demonstrated, not just stated. Evidence is required for Strength; assertion is sufficient for Declaration of Value. |
| **Tendency** | A Tendency is a probabilistic behavioral or market pattern. A Strength is an organizational capability — internal, controlled, and competitively oriented. A Tendency is observed externally; a Strength is possessed internally. |
| **Doctrine** | Doctrine is a standing operating rule elevated to institutional authority. A Strength is a capability assessment, not a rule. |

---

## IV. Required Metadata

| Field | Type | Purpose |
|---|---|---|
| capability_domain | string | The specific domain of the strength (operational / relational / technical / financial / structural) |
| evidence_basis | string | What demonstrates this is real — performance data, outcomes, assessments |
| competitive_context | string | What specifically this advantage is measured against |
| sustainability | enum | Enduring / Temporary / Condition-dependent |
| origin | fixed | Always: Internal |
| polarity | fixed | Always: Positive |

---

## V. Polymorphic Activation

Strength sensitivity should default high for organizations operating in competitive environments where capability mapping is strategic:
- Sports analytics teams (player and team capability profiling)
- Military and defense (force capability assessment)
- M&A and investment (target capability evaluation)
- Competitive intelligence functions
- Strategy and planning teams

---

## VI. Canon Revision Process Record

1. Concept developed through SWOT taxonomy analysis — 2026-05-01
2. Polymorphic activation argument established: organizations must toggle and query Strength directly
3. Evidence requirement established as the key distinction from Declaration of Value
4. Canonized and committed to repo

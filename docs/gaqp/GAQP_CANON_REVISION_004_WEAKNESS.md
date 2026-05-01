# GAQP Canon Revision 004
## Weakness as the 22nd Canonical Claim Type

**Status:** Canonized
**Revision ID:** GAQP-CR-004
**Date:** 2026-05-01
**Authority:** Execalc GAQP Standards Body
**Taxonomy version prior:** 1.3 (21 types)
**Taxonomy version after:** 1.4 (22 types)

---

## I. Governing Rationale

Weakness cannot be safely collapsed into Constraint or Diagnostic Signal because its addressability, competitive-disadvantage orientation, and correctable-capability specificity require distinct runtime handling — and because the distinction between what can be fixed and what cannot is one of the most consequential distinctions in strategic decision-making.

The decisive distinction is:

> A Weakness is correctable. A Constraint is not. Collapsing both into the same type destroys the most important information either claim carries: what response is appropriate.

---

## II. Definition

A confirmed internal capability gap, resource deficiency, or operational limitation that creates competitive disadvantage and is addressable through deliberate action. A Weakness is always internal in origin and negative in polarity. It is distinguished from a Constraint by its correctability — a Weakness can be addressed with investment, restructuring, development, or strategic choice; a Constraint cannot.

---

## III. Why Existing Types Are Insufficient

| Adjacent Type | Why Weakness Is Different |
|---|---|
| **Constraint** | A Constraint is a hard limit — it governs what is permissible and cannot be changed, only worked around. A Weakness is a correctable capability gap — it can be addressed. Conflating them produces wrong responses: routing a Weakness to "work around it" and a Constraint to "fix it" are both strategic errors. |
| **Diagnostic Signal** | A Diagnostic Signal is uncertain — it warrants attention before confirmation. A Weakness is confirmed. The runtime handling is fundamentally different: a Diagnostic Signal triggers investigation; a Weakness triggers remediation planning. |
| **Observation** | An Observation is a noticed pattern not yet fully durable. A Weakness is a confirmed, assessed capability gap with competitive consequences. The confidence floor is higher. |

---

## IV. Required Metadata

| Field | Type | Purpose |
|---|---|---|
| capability_domain | string | The specific domain of the gap (operational / relational / technical / financial / structural) |
| correction_path | string | What action would address this weakness |
| correction_cost | enum | High / Medium / Low / Unknown |
| competitive_impact | enum | Critical / Significant / Moderate / Minor |
| urgency | enum | Immediate / Near-term / Long-term / Monitoring |
| addressability | fixed | Always: Correctable |
| origin | fixed | Always: Internal |
| polarity | fixed | Always: Negative |

---

## V. Polymorphic Activation

Weakness sensitivity should default high for organizations engaged in capability assessment and competitive planning:
- Sports analytics (player and team gap analysis)
- Military and defense (force readiness assessment)
- Due diligence and M&A (target weakness evaluation)
- Board and executive strategy reviews
- Organizational development functions

---

## VI. Canon Revision Process Record

1. Concept developed through SWOT taxonomy analysis — 2026-05-01
2. Addressability established as the governing distinction from Constraint
3. Confirmation requirement established as the governing distinction from Diagnostic Signal
4. Canonized and committed to repo

# GAQP Canonical Claim Type Taxonomy
## Generally Accepted Qualitative Principles — Execalc / Players Capital Group

**Status:** Canonized  
**Version:** 1.0  
**Canonized:** 2026-04-25  
**Authority:** Execalc GAQP Standards Body  

---

## The 18 Canonical Claim Types

Every atomic nugget in the GAQP system belongs to exactly one of these 18 types.
This taxonomy is the governing nomenclature for qualitative classification across all
Execalc tenants, sessions, and runtime contexts.

This list is locked. Changes require explicit canon revision with documented rationale.

---

| # | Type | Definition |
|---|---|---|
| 1 | **Axiom** | Foundational durable truth; broadly applicable; not heavily context-dependent; treated as given within the corpus |
| 2 | **Definition** | Stable named construct with accepted meaning; governs how a term is used within the system |
| 3 | **Ontological Assertion** | A claim about the fundamental nature of a thing — what it IS, not just what it does or means |
| 4 | **Principle** | Portable judgment rule; broader than a tactic, narrower than an axiom; applicable across situations |
| 5 | **Doctrine** | A Principle elevated to institutional authority; governs a domain or tenant as a standing operating rule |
| 6 | **Heuristic** | Compressed decision shortcut or rule of thumb; fires above a confidence threshold |
| 7 | **Best Practice** | Recommended action pattern under recognizable conditions; procedural and repeatable |
| 8 | **Tendency** | Probabilistic behavioral or market pattern; confirmed across independent observations |
| 9 | **Observation** | Meaningful noticed pattern that is not yet fully durable; a candidate for promotion to Tendency or Institutional Precedent |
| 10 | **Event** | Time-bound fact with strategic significance; anchors the corpus to a specific moment |
| 11 | **Institutional Precedent** | A past resolved event whose outcome carries normative weight; distinct from Event by its forward-governing force |
| 12 | **Constraint** | A hard limit, prohibition, dependency, or boundary condition that governs what is permissible |
| 13 | **Threshold Condition** | A tipping point or boundary condition that, when crossed, changes the classification of surrounding claims |
| 14 | **Objective** | A target end-state or desired condition; governs direction without prescribing method |
| 15 | **Tradeoff** | A paired gain-loss relationship that requires explicit judgment to navigate |
| 16 | **Causal Claim** | A directional cause-effect assertion: X drives Y; open or closed causal pathway |
| 17 | **Declaration of Value** | A stated first principle about what an asset, action, or position is worth or capable of |
| 18 | **Diagnostic Signal** | A weak but strategically relevant indicator that something may be true; warrants attention before confirmation |

---

## Excluded from Taxonomy (with rationale)

| Type | Reason for Exclusion |
|---|---|
| **Analogy** | A reasoning tool, not a claim type. Assertive analogies resolve to Causal Claim or Institutional Precedent. Decorative analogies are not governed claims. |
| **Framework Reference** | Provenance metadata, not a claim. The invocation of a named framework (e.g. Porter's Five Forces) is captured in the provenance_source metadata field on the underlying claim. |
| **Pattern** | Subsumed by Tendency. A confirmed recurring pattern is a Tendency; an unconfirmed one is an Observation. |

---

## Governance Notes

- Every atomic nugget must be assigned exactly one claim type at ingress.
- Claim type determines activation scope, confidence floor, and composability rules.
- Observation is the entry-level type for unverified signals; promotion to Tendency or Institutional Precedent requires corpus corroboration.
- Doctrine and Axiom are the highest-authority types; they cannot be overridden by a single session or tenant without explicit canon revision.
- Threshold Condition is the only type that can alter the classification of adjacent claims — treat with care.

---

## Historical Note

This taxonomy was resolved by reconciling two independently derived 13-type lists
(GAQP Founding Charter v1.0 and GAQP & Execalc Runtime Reference, April 2026).
The union produced 23 candidate types. Five were collapsed or reclassified.
Two borderline types (Analogy, Framework Reference) were deliberately excluded
as reasoning tools or metadata rather than governed claim types.

The result is 18 canonical types — the permanent GAQP claim type standard.

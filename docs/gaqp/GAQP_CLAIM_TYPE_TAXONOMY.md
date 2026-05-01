# GAQP Canonical Claim Type Taxonomy
## Generally Accepted Qualitative Principles — Execalc / Players Capital Group

**Status:** Canonized  
**Version:** 1.6  
**Canonized:** 2026-04-25  
**Revised:** 2026-04-30 (Canon Revision GAQP-CR-001 — added Complaint as #19)  
**Revised:** 2026-05-01 (Canon Revision GAQP-CR-002 — added Tactic as #20)  
**Revised:** 2026-05-01 (Canon Revision GAQP-CR-003 — added Strength as #21)  
**Revised:** 2026-05-01 (Canon Revision GAQP-CR-004 — added Weakness as #22)  
**Revised:** 2026-05-01 (Canon Revision GAQP-CR-005 — added Threat as #23)  
**Revised:** 2026-05-01 (Canon Revision GAQP-CR-006 — added Opportunity as #24)  
**Authority:** Execalc GAQP Standards Body  

---

## The 24 Canonical Claim Types

Every atomic nugget in the GAQP system belongs to exactly one of these 24 types.
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
| 19 | **Stakeholder Complaint Claim** | A stakeholder-originated assertion that a product, service, policy, decision, or experience failed to meet expectation, caused harm, created dissatisfaction, or imposed an unreasonable burden; carries stakeholder provenance; may aggregate into pattern evidence; may create legal, operational, reputational, or design significance depending on context |
| 20 | **Tactic** | A specific action, maneuver, or procedure deployed in an adversarial or competitive context to achieve an immediate objective; situationally activated, opponent-aware, time-sensitive, and degrades in effectiveness when the adversary adapts; the operational expression of strategy applied against a specific threat, opponent, or competitive condition |
| 21 | **Strength** | A confirmed internal capability, resource, or positional advantage that provides competitive differentiation; must be evidenced through performance or structural assessment, not merely declared; always internal in origin and positive in polarity |
| 22 | **Weakness** | A confirmed internal capability gap, resource deficiency, or operational limitation that creates competitive disadvantage and is addressable through deliberate action; distinguished from Constraint by correctability — a Weakness can be fixed, a Constraint cannot; always internal in origin and negative in polarity |
| 23 | **Threat** | An external condition, adversarial action, or environmental shift that may cause harm, erode competitive advantage, or require defensive response; aggregates adversarial, competitive, regulatory, market, and environmental harm signals; always external in origin and negative or cautionary in polarity |
| 24 | **Opportunity** | An externally arising, time-sensitive condition that may create competitive advantage or value if acted upon before the window closes or competitors capture it; action-loading — demands response evaluation within a defined or implied window; always external in origin and positive in polarity |

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

The result was 18 canonical types.

**Canon Revision GAQP-CR-001 (2026-04-30):** Stakeholder Complaint Claim added as type #19.
Governing rationale: Complaint cannot be safely collapsed into Observation, Diagnostic Signal, or
Event because its stakeholder provenance, failure directionality, aggregation behavior, and
legal-operational implications require distinct runtime handling.
Full revision document: docs/gaqp/GAQP_CANON_REVISION_001_COMPLAINT.md

**Canon Revision GAQP-CR-002 (2026-05-01):** Tactic added as type #20.
Governing rationale: Tactic cannot be safely collapsed into Best Practice, Heuristic, or Doctrine
because its adversarial dimension, situational specificity, immediate-objective orientation,
counter-tactic vulnerability, and opponent-adaptive degradation require distinct runtime handling.
Full revision document: docs/gaqp/GAQP_CANON_REVISION_002_TACTIC.md

**Canon Revision GAQP-CR-003 (2026-05-01):** Strength added as type #21.
Governing rationale: Strength cannot be safely collapsed into Declaration of Value or Tendency
because its evidence requirement, competitive orientation, and internal-capability specificity
require distinct runtime handling. Polymorphic activation argument: organizations must toggle
and query Strength directly without translating through adjacent types.
Full revision document: docs/gaqp/GAQP_CANON_REVISION_003_STRENGTH.md

**Canon Revision GAQP-CR-004 (2026-05-01):** Weakness added as type #22.
Governing rationale: Weakness cannot be safely collapsed into Constraint or Diagnostic Signal
because its addressability, competitive-disadvantage orientation, and correctable-capability
specificity require distinct runtime handling. Addressability is the governing distinction
from Constraint: a Weakness can be fixed, a Constraint cannot.
Full revision document: docs/gaqp/GAQP_CANON_REVISION_004_WEAKNESS.md

**Canon Revision GAQP-CR-005 (2026-05-01):** Threat added as type #23.
Governing rationale: Threat cannot be safely collapsed into Tactic, Threshold Condition, or
Causal Claim because it is the aggregating external-negative condition type — the claim that
signals defensive response is required regardless of which underlying mechanism is driving harm.
Full revision document: docs/gaqp/GAQP_CANON_REVISION_005_THREAT.md

**Canon Revision GAQP-CR-006 (2026-05-01):** Opportunity added as type #24.
Governing rationale: Opportunity cannot be safely collapsed into Objective, Observation, Causal
Claim, or Diagnostic Signal because its time-bounded window, action requirement, and inaction
cost create a structurally distinct type whose most important property — the window closes —
is carried by no existing type.
Full revision document: docs/gaqp/GAQP_CANON_REVISION_006_OPPORTUNITY.md

The result is 24 canonical types. SWOT is now fully contained within GAQP as four first-class
claim types (Strength #21, Weakness #22, Threat #23, Opportunity #24).

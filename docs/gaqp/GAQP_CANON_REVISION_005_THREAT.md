# GAQP Canon Revision 005
## Threat as the 23rd Canonical Claim Type

**Status:** Canonized
**Revision ID:** GAQP-CR-005
**Date:** 2026-05-01
**Authority:** Execalc GAQP Standards Body
**Taxonomy version prior:** 1.4 (22 types)
**Taxonomy version after:** 1.5 (23 types)

---

## I. Governing Rationale

Threat cannot be safely collapsed into Tactic, Threshold Condition, or Causal Claim because it is the aggregating external-negative condition type — the claim that signals defensive response is required regardless of which underlying mechanism is driving the harm. An organization must be able to surface, toggle, and respond to Threats as a unified category, not reconstruct them from filtered subsets of other types.

The decisive distinction is:

> A Tactic is what the adversary deploys. A Threshold Condition is a tipping point that may be neutral. A Causal Claim is directional. A Threat is the condition that requires defensive response — it unifies adversarial, environmental, and structural harm signals into a single activatable type.

---

## II. Definition

An external condition, adversarial action, or environmental shift that may cause harm, erode competitive advantage, or require defensive response. A Threat is always external in origin and negative or cautionary in polarity. It serves as the primary claim type for defensive strategic reasoning, aggregating across adversarial, competitive, regulatory, market, and environmental sources of harm.

---

## III. Why Existing Types Are Insufficient

| Adjacent Type | Why Threat Is Different |
|---|---|
| **Tactic** | A Tactic is a specific adversarial maneuver with activation conditions, counter-tactics, and time sensitivity. A Threat is the broader condition the tactic operates within. A competitor's pricing tactic is a Tactic. The competitive pricing pressure it creates is a Threat. They are different levels of the same situation. |
| **Threshold Condition** | A Threshold Condition is a tipping point — it may be neutral, positive, or negative. A Threat is specifically harmful. Threshold Conditions can become Threats when crossed; they are not Threats until they are directionally harmful. |
| **Causal Claim** | A Causal Claim asserts X drives Y. It is directional but not inherently defensive. A Threat is specifically the claim that external conditions require organizational response. The response requirement is not carried by Causal Claim. |
| **Diagnostic Signal** | A Diagnostic Signal is weak and uncertain. A Threat may be confirmed and severe. Collapsing them loses the urgency distinction. |

---

## IV. Threat Source Taxonomy

| Source | Description |
|---|---|
| **Adversarial** | A competitor, opponent, or hostile actor is taking or planning action against the organization |
| **Environmental** | Market conditions, economic shifts, or structural changes create harm exposure |
| **Regulatory** | Legal or compliance changes impose new risk or constraint |
| **Competitive** | Competitive dynamics erode advantage without a specific adversarial actor |
| **Technological** | Technological change disrupts existing capabilities or market position |
| **Reputational** | External conditions risk damage to standing, trust, or relationships |

---

## V. Required Metadata

| Field | Type | Purpose |
|---|---|---|
| threat_source | enum | Adversarial / Environmental / Regulatory / Competitive / Technological / Reputational |
| severity_level | enum | Critical / High / Medium / Low |
| time_horizon | enum | Immediate / Near-term / Long-term / Emerging |
| likelihood | enum | High / Probable / Possible / Low |
| mitigation_options | string | Known defensive responses available |
| linked_tactics | list | Specific adversarial Tactics contributing to this Threat |
| linked_threshold_conditions | list | Threshold Conditions whose crossing would escalate this Threat |
| origin | fixed | Always: External |
| polarity | fixed | Always: Negative or Cautionary |

---

## VI. Polymorphic Activation

Threat sensitivity should default high for organizations with adversarial or competitive exposure:
- Military and defense (adversarial threat assessment is the primary intelligence function)
- Sports analytics (opponent capability and game-plan threat analysis)
- Competitive intelligence functions
- Legal and regulatory risk teams
- Financial services and investment risk teams
- National security and intelligence agencies

---

## VII. Canon Revision Process Record

1. Concept developed through SWOT taxonomy analysis — 2026-05-01
2. Aggregating-type role established: Threat unifies adversarial, environmental, and structural harm signals
3. Distinction from Tactic established at the level vs. condition level
4. Distinction from Threshold Condition established by directional harm requirement
5. Canonized and committed to repo

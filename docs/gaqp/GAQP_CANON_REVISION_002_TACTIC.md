# GAQP Canon Revision 002
## Tactic as the 20th Canonical Claim Type

**Status:** Canonized
**Revision ID:** GAQP-CR-002
**Date:** 2026-05-01
**Authority:** Execalc GAQP Standards Body
**Taxonomy version prior:** 1.1 (19 types)
**Taxonomy version after:** 1.2 (20 types)

---

## I. Governing Rationale

Tactic cannot be safely collapsed into Best Practice, Heuristic, or Doctrine because its adversarial dimension, situational specificity, immediate-objective orientation, counter-tactic vulnerability, and opponent-adaptive degradation require distinct runtime handling.

The decisive distinction is:

> A tactic is an adversarially-aware, situationally-activated maneuver deployed to achieve an immediate objective against a specific opponent or competitive condition.

No existing type captures the adversarial dimension. Best Practices do not have opponents. Heuristics do not degrade when countered. Doctrine operates at the strategic level, not the operational. Tactic is the claim type that lives at the intersection of all three — and is reducible to none of them.

---

## II. Claim Type Name

**Full name:** Tactic
**Type number:** 20

---

## III. Definition

A specific action, maneuver, or procedure deployed in an adversarial or competitive context to achieve an immediate objective. A Tactic is situationally activated, opponent-aware, time-sensitive, and degrades in effectiveness when the adversary adapts. It is the operational expression of strategy applied against a specific threat, opponent, or competitive condition.

---

## IV. Core Distinctions from Adjacent Types

| Adjacent Type | Why Tactic Is Different |
|---|---|
| **Best Practice** | Best Practice is opponent-agnostic and broadly applicable. A Tactic requires an adversary or competitive context. Best Practices do not degrade when countered — Tactics do. |
| **Heuristic** | A Heuristic is a compressed decision shortcut firing above a confidence threshold. A Tactic is a deliberate adversarial maneuver, not a shortcut. Heuristics are passive; Tactics are active. |
| **Doctrine** | Doctrine governs a domain at the strategic level as a standing operating rule. A Tactic is the operational-level specific action — the execution of doctrine against a specific opponent in a specific moment. Blitzkrieg as a doctrine is different from blitzkrieg as a tactical execution in France, 1940. |
| **Objective** | An Objective is a target end-state. A Tactic is the specific maneuver used to reach it. Objectives govern direction; Tactics govern method in adversarial conditions. |

---

## V. Structural Properties

**Adversarially aware:** A Tactic presupposes an opponent, competitor, or opposing force. Without an adversarial or competitive context, the claim resolves to Best Practice or Heuristic.

**Situationally activated:** A Tactic fires in defined conditions — a game state, a threat level, a competitive posture, a negotiation phase. It is not always-on.

**Immediate-objective oriented:** A Tactic achieves something now. Its time horizon is shorter than Doctrine or Principle.

**Counter-tactic vulnerable:** Every Tactic has a response. Effectiveness degrades when the adversary adapts. This is the property that most decisively separates Tactic from all other claim types — no other type in the taxonomy degrades through opponent adaptation.

**Historically traceable:** Tactics accumulate an outcome record. The blitzkrieg worked in France, degraded in the Soviet Union. The box defense holds against a single interior scorer, collapses against perimeter spacing. Performance history generates Institutional Precedents and Threshold Conditions linked to the Tactic.

---

## VI. Required Metadata

In addition to standard GAQP metadata fields, every Tactic requires:

| Field | Type | Purpose |
|---|---|---|
| tactic_type | enum | offensive / defensive / counter / deceptive / positioning / transitional |
| adversary_context | string | What opponent type or competitive condition activates this tactic |
| activation_condition | string | The specific situation or game state that triggers deployment |
| counter_tactic_links | list | Links to nuggets that neutralize or respond to this tactic |
| degradation_condition | string | When and why effectiveness drops |
| time_sensitivity | enum | immediate / short-term / sustained |
| domain | enum | military / sports / legal / competitive / negotiation / intelligence / political / operational |

---

## VII. Integration with the Signal Graph

A Tactic does not stand alone. It generates and connects to a cluster of related claim types:

```
Tactic
  ├── generates → Institutional Precedent (historical outcome records)
  ├── activates under → Threshold Condition (game state, threat level)
  ├── derives from → Doctrine (tactical expression of strategic doctrine)
  ├── confirms (when successful repeatedly) → Tendency
  ├── subject to → Constraint (conditions prohibiting or limiting use)
  └── opposed by → Counter-Tactic (also a Tactic, linked via counter_tactic_links)
```

The signal graph around a single well-documented Tactic is among the richest in the taxonomy. Blitzkrieg alone generates dozens of linked Institutional Precedents, Threshold Conditions, Causal Claims, and Tendencies.

---

## VIII. Canonical Examples by Domain

**Military:**
- Blitzkrieg: rapid armored breakthrough with close air support to collapse lines before response
- Flanking maneuver: force redeployment to attack the weakest point of an opponent's position
- Feint: simulated attack on one front to draw resources from the actual target

**Sports:**
- Box defense: four perimeter defenders plus one in the paint against a dominant interior scorer
- Full-court press: defensive pressure across the entire court to force turnovers and fatigue
- Pick and roll: screen plus roll to the basket, forcing a defensive coverage decision

**Legal:**
- Motion in limine: pre-trial exclusion of prejudicial evidence before the jury sees it
- Voir dire challenge: strategic juror removal to shape the panel composition
- Deposition as discovery: use deposition testimony to establish inconsistencies before trial

**Negotiation and business:**
- Price anchoring: set the first number to control the negotiation range
- Preemptive market entry: move before a competitor can establish position
- Deliberate delay: slow the timeline to increase the counterparty's pressure

**Intelligence:**
- Disinformation: introduce false signal into an adversary's intelligence stream
- Source compartmentalization: limit knowledge of an asset to reduce exposure risk

---

## IX. Theoretical Grounding

The Tactic claim type emerges from the convergence of multiple intellectual disciplines that independently recognized the same category:

**Boyd's OODA Loop:** Tactics are the operational expressions of the Orient→Decide→Act cycle applied in adversarial tempo competition. The organization that cycles through OODA faster wins. Tactics are the mechanism of tempo advantage.

**Cognitive science:** Tactics are adaptive heuristics with opponent-awareness built in. They update faster than ordinary heuristics because the adversary is actively countering them. They are System 2 heuristics — deliberate rather than automatic.

**Common law:** Legal tactics are the situational application of doctrine to a specific dispute before a specific tribunal. The distinction between legal doctrine and legal tactics is centuries old and precisely maps onto the Doctrine/Tactic distinction in GAQP.

**Expert systems:** Production rules in adversarial contexts — the IF-THEN logic of expert systems applied against an active opponent rather than a static environment.

Tactic is not an invented category. It is the category that every serious intellectual discipline dealing with adversarial conditions has independently recognized. GAQP names it, governs it, and makes it machine-processable.

---

## X. Tenant Sensitivity

Tactic is a high-sensitivity claim type for organizations operating in adversarial or competitive environments. On the Knowledge Policy slider panel, Tactic sensitivity should default high for:

- Defense and intelligence organizations
- Sports analytics teams
- Litigation practices
- Competitive intelligence functions
- M&A and negotiation teams
- Political and strategic advisory

Organizations without adversarial context (internal process teams, academic institutions, nonprofits) may default Tactic sensitivity low without meaningful knowledge loss.

---

## XI. Canon Revision Process Record

1. Concept originated in ideation session — 2026-05-01
2. Polymorphic analysis conducted across cognitive science, military theory, legal reasoning, information theory, and expert systems
3. Exclusion analysis conducted against Best Practice, Heuristic, Doctrine, and Objective
4. Governing rationale formalized
5. Definition, metadata schema, signal graph integration, and domain examples developed
6. Theoretical grounding established across multiple disciplines
7. Canonized and committed to repo

Per the GAQP Founding Charter: the taxonomy is locked except through explicit canon revision with documented rationale. This document constitutes that rationale. The taxonomy is updated to version 1.2.

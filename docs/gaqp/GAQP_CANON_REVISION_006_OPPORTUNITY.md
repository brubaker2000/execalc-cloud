# GAQP Canon Revision 006
## Opportunity as the 24th Canonical Claim Type

**Status:** Canonized
**Revision ID:** GAQP-CR-006
**Date:** 2026-05-01
**Authority:** Execalc GAQP Standards Body
**Taxonomy version prior:** 1.5 (23 types)
**Taxonomy version after:** 1.6 (24 types)

---

## I. Governing Rationale

Opportunity cannot be safely collapsed into Objective, Observation, Causal Claim, or Diagnostic Signal because its external origin, time-bounded window, action requirement, competitive pressure, and inaction cost create a structurally distinct claim type whose most important property — that the window closes — is carried by no existing type.

The decisive distinction is:

> An Objective is an internal aim. An Observation is passive recognition. A Causal Claim is directional. A Diagnostic Signal is weak. An Opportunity says: something outside us has opened a value window, the window can close, inaction has a cost, and competitors may move first.

---

## II. Definition

An externally arising, time-sensitive condition that may create competitive advantage, value, or strategic gain if acted upon before the window closes or before competitors capture it. An Opportunity is always external in origin and positive in polarity. It is action-loaded: it does not merely describe a favorable condition, it demands response evaluation within a defined or implied window.

---

## III. Why Existing Types Are Insufficient

| Adjacent Type | Why Opportunity Is Different |
|---|---|
| **Objective** | An Objective is an internal target end-state the organization has set for itself. An Opportunity is an external condition that creates value the organization has not yet claimed. Objectives are chosen; Opportunities are discovered. |
| **Observation** | An Observation is passive — a meaningful pattern noticed that is not yet durable. An Opportunity is active — it demands evaluation and potential response. An Observation may become an Opportunity when its action implications are recognized, but they are different claims. |
| **Causal Claim** | A Causal Claim asserts X drives Y. It is directional but not action-loading. "Market consolidation drives pricing pressure" is a Causal Claim. "Market consolidation creates an 18-month acquisition window before a larger competitor moves" is an Opportunity. The window and the action requirement are not present in the Causal Claim. |
| **Diagnostic Signal** | A Diagnostic Signal is weak — it warrants attention before confirmation. An Opportunity may be well-evidenced. More importantly, a Diagnostic Signal does not carry a time window or action requirement. |
| **Tendency** | A Tendency is a confirmed recurring pattern. It may inform an Opportunity but is not itself action-loading or time-bounded. |

---

## IV. Required Metadata

| Field | Type | Purpose |
|---|---|---|
| source_condition | string | The external condition creating the opportunity |
| value_potential | string | What advantage or gain may be captured |
| time_window | string | How long the window is estimated to remain open |
| action_required | string | What the organization must do to capture this |
| competitive_pressure | string | Who else may capture this and how quickly |
| uncertainty_level | enum | High / Medium / Low |
| evidence_basis | string | What supports the existence of this opportunity |
| owner | string | Who is accountable for evaluating and pursuing |
| expiration_date | date | When the window is estimated to close or require review |
| linked_objective | string | Which organizational objective this opportunity supports |
| linked_risks | list | Risks associated with pursuing this opportunity |
| linked_constraints | list | Constraints that limit pursuit of this opportunity |
| origin | fixed | Always: External |
| polarity | fixed | Always: Positive |

---

## V. Runtime Behavior

Opportunity claims are action-loading. Unlike most claim types that are stored and activated by context, an Opportunity should trigger evaluation and prioritization at admission. Specifically:

- Opportunity claims with short `time_window` values should surface with elevated priority on the executive rail
- Unowned Opportunity claims (no `owner` assigned) should trigger escalation
- Expired or past-window Opportunity claims should be promoted to Institutional Precedent for outcome recording
- Opportunity claims with high `competitive_pressure` should activate Threat detection for the corresponding competitive actors

---

## VI. The SWOT Completion

With Opportunity canonized as #24, GAQP now natively contains all four SWOT components as first-class claim types:

| SWOT | GAQP Type | # | Key Distinction |
|---|---|---|---|
| Strength | Strength | 21 | Confirmed internal capability; evidence required |
| Weakness | Weakness | 22 | Correctable internal gap; distinguished from Constraint by addressability |
| Opportunity | Opportunity | 24 | External time-bounded value window; action-loading |
| Threat | Threat | 23 | External defensive-response condition; aggregates adversarial, environmental, regulatory harm |

SWOT is not a lens on GAQP. SWOT is contained within GAQP.

Organizations that currently run SWOT analyses can import them directly into the governed corpus without translation. Every SWOT element is a first-class claim type with full metadata, confidence tracking, composability, and runtime activation.

---

## VII. Polymorphic Activation

Opportunity sensitivity should default high for organizations engaged in value creation and growth:
- Real estate investors (acquisition window detection)
- Investment and private equity (deal sourcing and market timing)
- Business development functions
- Strategic planning teams
- M&A advisory
- Competitive intelligence functions

---

## VIII. Canon Revision Process Record

1. Concept developed through SWOT taxonomy analysis — 2026-05-01
2. Time window and action requirement established as the governing structural distinctions
3. Inaction cost identified as the property that no existing type carries
4. Runtime behavior specified: Opportunity claims are action-loading at admission
5. SWOT completion noted: all four SWOT components now first-class GAQP types
6. Canonized and committed to repo

# GAQP Cross-Document Tag Vocabulary

**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

---

## I. Purpose

The cross-document tag vocabulary defines the controlled set of tags that enable retrieval and correlation across documents, sessions, and tenants. Where the Tagging System (`GAQP_TAGGING_SYSTEM.md`) defines namespaces and rules, this document defines the actual vocabulary within each namespace.

This vocabulary is the seam between individual claim storage and corpus-level intelligence. Without a shared vocabulary, two tenants storing claims about the same phenomenon use different labels and cannot be compared.

---

## II. Domain Vocabulary

The five canonical domains are closed. All claims must map to exactly one.

| Domain | Covers |
|---|---|
| `strategy` | Competitive positioning, market thesis, growth vectors, platform decisions, partnerships |
| `capital` | Investment decisions, financing, capital structure, valuation, returns |
| `operations` | Process, execution, capacity, efficiency, fixed vs. variable cost, supply chain |
| `human_behavior` | Incentives, psychology, negotiation, stakeholder dynamics, culture |
| `governance` | Regulatory, legal, compliance, fiduciary, risk management, audit |

---

## III. Subdomain Vocabulary (Illustrative — extensible by tenant)

Subdomains narrow the domain for retrieval. These are illustrative — tenants may extend.

**strategy:**
- `competitive_moat`, `market_entry`, `platform_expansion`, `partnership_model`, `product_strategy`, `brand_positioning`

**capital:**
- `valuation_methodology`, `debt_structure`, `equity_dilution`, `return_profile`, `exit_strategy`, `working_capital`

**operations:**
- `fixed_ops`, `variable_ops`, `capacity_planning`, `supply_chain`, `unit_economics`, `margin_structure`

**human_behavior:**
- `incentive_design`, `negotiation_dynamics`, `principal_agent`, `cultural_alignment`, `talent_retention`

**governance:**
- `regulatory_compliance`, `fiduciary_duty`, `audit_trail`, `risk_framework`, `legal_exposure`

---

## IV. Evidence Status Vocabulary

The evidence status vocabulary describes how a claim was established. Closed set.

| Value | Meaning | Retrieval weight |
|---|---|---|
| `observed` | Directly witnessed or measured — empirical grounding | Highest |
| `corroborated` | Multiple independent sources confirm | High |
| `argued` | Reasoned conclusion from premises — logically derived | Medium |
| `inferred` | Drawn by extension from related evidence | Lower |
| `unverified` | Claimed but not yet tested against any external reference | Lowest |

---

## V. Activation Trigger Vocabulary

Activation triggers tell the retrieval engine when to surface a claim. They are the conditions under which a claim becomes relevant. Structured as `{namespace}:{value}`.

**Standard trigger namespaces:**

| Namespace | Example | Meaning |
|---|---|---|
| `scenario:` | `scenario:draft_trade` | Surfaces when this scenario type is active |
| `claim_type:` | `claim_type:doctrine` | Surfaces alongside other claims of this type |
| `domain:` | `domain:capital` | Surfaces in capital-domain reasoning contexts |
| `objective:` | `objective:maximize_roi` | Surfaces when this governing objective is stated |
| `counterparty:` | `counterparty:seller` | Surfaces in negotiations with this party type |
| `signal:` | `signal:margin_compression` | Surfaces when this diagnostic signal is detected |

A claim may carry any number of activation triggers. More triggers = broader activation surface.

---

## VI. Polarity Vocabulary

| Value | Use |
|---|---|
| `positive` | The claim describes something that advances the objective |
| `cautionary` | The claim warns of a condition that may become adverse |
| `negative` | The claim describes something that harms the objective |
| `neutral` | The claim is factual or structural with no valence |
| `mixed` | The claim contains both positive and negative elements |

---

## VII. Durability Class Vocabulary

| Value | Meaning | Default retention |
|---|---|---|
| `enduring` | Governs regardless of when retrieved | Perpetual |
| `medium_term` | Relevant within a defined time window | Review after 12 months |
| `ephemeral` | Relevant only for a specific event or window | Expires with the event |

---

## VIII. Freshness Class Vocabulary

| Value | Meaning |
|---|---|
| `timeless` | No temporal decay — the claim is always equally valid |
| `date_sensitive` | Validity depends on when it is retrieved |
| `event_bound` | Valid only until a named event resolves |
| `expiring` | Has an explicit expiry date set at creation |

---

## IX. Governing Rule

> Controlled vocabulary is the difference between a searchable corpus and a labeled pile. Every field with an enumerated set of values must use only values from this vocabulary. Extension requires a canon revision — not unilateral deviation.

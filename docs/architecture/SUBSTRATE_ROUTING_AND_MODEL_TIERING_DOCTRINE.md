# Substrate Routing and Model Tiering Doctrine

## Purpose

This doctrine defines how Execalc should use one or more language-model substrates beneath a single governed operating layer.

It begins from a foundational principle:

> Execalc is one governed system, but it does not need to use one model for every kind of work.  
> The governance layer is the product. The model layer is the engine room.

---

## Why This Doctrine Exists

Different classes of work have different requirements for:
- quality
- latency
- cost
- safety
- traceability
- consequence

If all tasks are routed to the same premium substrate, operating expense may rise unnecessarily. If trust-critical work is routed to a weak substrate, quality may collapse.

The solution is governed tiering.

---

## Foundational Principle

**One mind at the surface, multiple engines underneath.**

The operator should experience a single coherent system with one doctrine, one memory discipline, one execution boundary, and one judgment standard.

Underneath that surface, Execalc may route different tasks to different substrates according to policy.

---

## Task Classes

### Tier 1 — Low-Stakes Cognitive Plumbing

Use the least expensive safe substrate for:
- parsing
- classification
- extraction
- summarization
- formatting
- retrieval preparation
- lightweight drafting
- schema normalization

### Tier 2 — Core Judgment

Use the strongest trusted substrate for:
- executive synthesis
- decision framing
- tradeoff analysis
- ambiguity resolution
- scenario compression
- operator-facing recommendations
- memory admission reasoning
- rail or doctrine candidate evaluation

### Tier 3 — Verification / Challenge

Use a separate or equivalent-quality substrate when warranted for:
- adversarial review
- contradiction checking
- high-stakes challenge runs
- structured second-pass validation
- especially sensitive operator-facing output

---

## Routing Rule

> **Use the cheapest model that is safe for the specific layer of work.**

This is not a cost-minimization doctrine alone. It is a **governed suitability doctrine**.

The right question for any new capability:  
**"Is this trust-critical or labor?"** — that determines model tier.

---

## Tasks That Should Not Be Cheapened Recklessly

The following should remain strongly governed and generally routed to premium or premium-plus verification pathways:

- final executive recommendations
- memory admission decisions
- action proposals
- operator-loyal synthesis
- high-impact conflict arbitration
- doctrine or rail promotion decisions that may influence system memory or category language

---

## Routing Metadata

Every routed task should ideally preserve metadata such as:

| Field | Description |
|---|---|
| `task_class` | Tier 1 / 2 / 3 |
| `substrate_used` | Which model handled this task |
| `routing_reason` | Why this tier was selected |
| `escalation_reason` | If upgraded from a lower tier, why |
| `confidence_posture` | Expected output confidence |
| `verification_performed` | Whether a challenge pass ran |

This ensures routing remains auditable and tunable.

---

## Escalation Triggers

A task should be escalated upward in model tier when:

- ambiguity remains unusually high
- the output affects durable system state
- the issue is operator-critical
- the stakes are high
- conflicting evidence is substantial
- prior low-tier output appears unstable or weak

---

## Model Tier Table

| Layer | Role | Model Tier |
|---|---|---|
| Prime Directive evaluation | Judgment | Premium (Opus-class) |
| Memory admission gate | Judgment | Premium |
| Reflex gate decisions | Judgment | Premium |
| Executive synthesis | Judgment | Premium |
| Doctrine or rail promotion | Judgment | Premium |
| Summarization | Labor | Cheapest safe |
| Normalization | Labor | Cheapest safe |
| Extraction | Labor | Cheapest safe |
| Formatting | Labor | Cheapest safe |
| Retrieval preparation | Labor | Cheapest safe |

---

## Economic Thesis

Tiered routing can materially improve unit economics.

This allows Execalc to:
- reduce operating expense
- offer more competitive pricing
- preserve margin
- subsidize higher-quality judgment where it matters most

The real strategic gain is not merely lower cost. It is **better allocation of cognitive spend**.

---

## Product Integrity Rule

The operator must never feel like they are using a bag of unrelated models.

All routing must preserve:
- one governing doctrine
- one memory system
- one executive posture
- one explanation standard

Model diversity must be **invisible at the experience layer** and visible only at the governance and audit layer.

---

## Relationship to Invariants

This doctrine implements the model-tier invariant established in `docs/EXECALC_INVARIANTS.md`.

The invariant holds: cost optimization that downgrades trust-critical layers is a violation — not a feature.

Any routing change that moves a Tier 2 or Tier 3 task into Tier 1 territory must pass explicit review against the invariant before implementation.

---

## Thesis

Execalc should be model-agnostic at the governance layer and model-selective at the execution layer.

That is how the system preserves both economics and integrity.

The goal is not to worship a model. The goal is to govern the use of models so the right engine is applied to the right labor at the right cost and quality threshold.

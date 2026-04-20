# PRIME_DIRECTIVE_RUNTIME_ENFORCEMENT.md

## Status
Draft v0.1

## Owner
Governance / Core 7

## Position in Core 7
Framework 1 — The governing compass. Fires before final output is delivered. All other Core 7 frameworks operate within the constraints it defines.

---

## Purpose

The Prime Directive is the top-level governance framework. Its doctrine is canonized in `docs/vision/TRUE_NORTH.md` and `CLAUDE.md`. This document is its runtime counterpart: what enforcement actually looks like in code, what fields are required, where it fires, and what happens when it fails.

Doctrine without runtime enforcement is philosophy. This document converts the philosophy into a gate.

---

## The Enforcement Mandate

Every decision output, recommendation, or governed synthesis that exits Execalc toward an operator must pass Prime Directive evaluation before delivery.

The three lenses must be evaluated — not all three must be favorable, but all three must be examined. An output that skips any lens has not cleared the gate regardless of how sound the reasoning appears.

> **The sin is not an unfavorable lens. The sin is an unevaluated one.**

---

## When Prime Directive Evaluation Fires

Prime Directive evaluation is **required** whenever Execalc produces:

| Output Type | PD Gate Required |
|---|---|
| Decision recommendation | Yes |
| Strategic analysis | Yes |
| Risk assessment | Yes |
| Opportunity identification | Yes |
| Executive summary | Yes |
| Scenario-triggered output | Yes |
| Proactive alert (PSA Mode) | Yes |
| General query response (null pathway) | No |

The null pathway (general queries: recipes, lookups, etc.) is exempt. All governed outputs are not.

---

## The Three Lens Fields

Every governed output must carry explicit Prime Directive evaluation fields:

```python
@dataclass
class PrimeDirectiveEvaluation:
    # Lens 1: Assets vs. Liabilities
    assets_liabilities_assessment: str       # Required — cannot be empty
    assets_liabilities_verdict: Verdict      # FAVORABLE | UNFAVORABLE | NEUTRAL | UNKNOWN

    # Lens 2: Risk / Reward
    risk_reward_assessment: str              # Required — cannot be empty
    risk_reward_verdict: Verdict             # FAVORABLE | UNFAVORABLE | NEUTRAL | UNKNOWN

    # Lens 3: Supply / Demand
    supply_demand_assessment: str            # Required — cannot be empty
    supply_demand_verdict: Verdict           # FAVORABLE | UNFAVORABLE | NEUTRAL | UNKNOWN

    # Gate outcome
    gate_result: GateResult                  # PASS | BLOCK | ESCALATE | FLAG
    gate_rationale: str                      # Required when result is not PASS
    unevaluated_lenses: list[str]            # Must be empty for PASS
    evaluator_model_tier: str                # Must be Premium (Opus-class) — this is judgment
```

```python
class Verdict(Enum):
    FAVORABLE = "favorable"
    UNFAVORABLE = "unfavorable"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"         # Acceptable — signals missing information

class GateResult(Enum):
    PASS = "pass"               # All three lenses evaluated; output may proceed
    BLOCK = "block"             # Hard governance violation; output does not proceed
    ESCALATE = "escalate"       # Requires elevated authority before proceeding
    FLAG = "flag"               # Passes with explicit notation of concerning finding
```

---

## Gate Logic

```
All three lenses evaluated?
    No → BLOCK (unevaluated lens is a governance failure, not a pass condition)
    Yes → continue

Any lens returns BLOCK-triggering condition?
    Yes → BLOCK
    No → continue

Any lens returns ESCALATE-triggering condition?
    Yes → ESCALATE
    No → continue

Any lens unfavorable?
    Yes → FLAG (output proceeds with explicit notation; tradeoff was seen and named)
    No → PASS
```

**BLOCK-triggering conditions:**
- Output recommends action that degrades assets or increases liabilities without explicit tradeoff acknowledgment
- Output recommends action where risk clearly exceeds reward without survival justification
- Output exploits a supply/demand position that is not structurally real (fictional leverage)

**ESCALATE-triggering conditions:**
- Output involves irreversible action above materiality threshold
- Output involves a counterparty whose interests directly conflict with operator's (requires Polymorphia confirmation)

---

## Model Tier Requirement

Prime Directive evaluation must use a **Premium (Opus-class) model**. This is judgment, not labor.

Using a labor-tier model for Prime Directive evaluation violates the multi-model routing invariant and produces ungoverned output that has only the appearance of governance.

---

## Enforcement Position in the Decision Loop

```
Operator input
    ↓
Stage 0: Strategic Terrain Classification
    ↓
Stages 1–5: Reflex and Activation System
    ↓
Judgment Call (Premium model, full context package)
    ↓
→ PRIME DIRECTIVE EVALUATION GATE ←
    ↓
    PASS → Output delivered to operator (with PD fields attached)
    FLAG → Output delivered with explicit notation
    ESCALATE → Operator prompted before delivery
    BLOCK → Output withheld; operator notified of block reason
```

---

## Audit Requirements

Every Prime Directive evaluation must appear in the session audit trail:

| Event | Auditable Fields |
|---|---|
| Lens evaluation | lens, assessment text, verdict |
| Gate outcome | result, rationale, timestamp |
| BLOCK event | blocking lens, reason, output hash |
| ESCALATE event | escalation trigger, authority required |
| FLAG event | flagged lens, tradeoff description |

A BLOCK or ESCALATE event with no audit record is a governance failure.

---

## What This Converts

Without this doc: the Prime Directive is a philosophical commitment that may or may not influence reasoning depending on whether the model happens to apply it.

With this doc: the Prime Directive is a structural gate. Outputs either pass the gate or they do not proceed. The gate is auditable, reproducible, and independent of whether the model "felt like" applying it.

This is the difference between a governed system and an aspirationally governed one.

---

## Relationship to Other Doctrine

| Document | Relationship |
|---|---|
| `TRUE_NORTH.md` | Prime Directive doctrine and founding lens definitions |
| `CLAUDE.md §4` | Canonical two-tier structure and enforcement doctrine |
| `RUNTIME_REASONING_SEPARATION.md` | PD evaluation is a runtime gate, not a reasoning step |
| `REFUSAL_AS_SUCCESS_DOCTRINE.md` | BLOCK is a successful gate outcome |
| `EXECALC_INVARIANTS.md` | Multi-model routing invariant — evaluation must use Premium tier |
| `FOUNDING_ORIGIN.md` | Origin of the three lenses from PCG's three-legged stool |

# POLYMORPHIA_MAP_SPEC.md

## Status
Draft v0.1 — Pre-Stage-8 blocker spec

## Owner
Architecture / Stage 8C

## Purpose
This document specifies the Polymorphia dimensional map — its required structure, how it is produced, how it is validated, and how it flows through the judgment pipeline.

It exists because `POLYMORPHIA_RUNTIME_USAGE.md` defines what the dimensional map contains and what it governs, but does not specify who produces it and how. This document closes that gap.

---

## The Foundational Principle

> **The LLM proposes the map. The system governs the map.**

Polymorphia is not a post-processing step. It is not a separate model call. It is a **structured output requirement** placed on the Stage 5 Judgment Call.

The LLM generates the dimensional map as part of its primary output. The system then validates the map against completeness and consistency requirements before the output proceeds to the Prime Directive gate.

This means the dimensional map is not an external analysis layered on top of the LLM's reasoning. It is evidence that the LLM's reasoning has considered multiple valid interpretations of the situation.

---

## Who Produces the Map

The Stage 5 Judgment Call (the Opus-class LLM call) produces the dimensional map as a required component of its structured output.

The output template for every scenario includes a `polymorphia` field. The model is required to populate this field. An output that does not include a populated `polymorphia` field fails the output schema validation and is not delivered.

**The model receives:**
- The operator's input
- The assembled context package (corpus fragments, scenario logic, reflexes, memory)
- The output schema, which explicitly requires a `polymorphia` block

**The model must produce:**
- At minimum 2 dimensions
- Each dimension with a confidence score
- A designated dominant dimension
- A `collapsed_reading_warning` flag if only one dimension is identified

**The system validates:**
- Schema completeness (required fields present)
- Minimum dimension count (≥ 2, unless input is genuinely one-dimensional — see exception below)
- Internal consistency (dominant dimension must have highest confidence score)
- Collapsed reading detection (if model produces only 1 dimension despite complex signals, system flags it)

---

## Required Dimensions

Every dimensional map must address the following axes. These are not optional — they are the minimum Polymorphia evaluation:

| Axis | What It Covers | Required? |
|---|---|---|
| **Strategic frame** | What strategic situation is this, and what does that imply? | Always |
| **Risk/opportunity balance** | Where does the risk-reward sit on this dimension? | Always |
| **Stakeholder perspective** | How does the dominant stakeholder read this differently than the operator? | When stakeholders identified |
| **Time horizon** | Does the near-term and long-term reading diverge? | When horizon is stated or implied |
| **Alternative interpretation** | What is the most credible alternative framing of this situation? | Always |

The model is free to add additional dimensions beyond these five. The model is not free to omit the required ones without explicit suppression justification.

---

## Map Schema

```json
{
  "polymorphia": {
    "dimensions": [
      {
        "id": "D1",
        "axis": "strategic_frame",
        "label": "Competitive Threat Reading",
        "description": "The signal pattern indicates market share erosion from a direct competitor entering the lower-price segment.",
        "implied_action": "Defensive posture. Accelerate differentiation or reduce price exposure in the threatened segment.",
        "confidence": 0.87,
        "prime_directive_lenses": {
          "assets_liabilities": "Negative — margin erosion likely in lower-price segment",
          "risk_reward": "Asymmetric downside if competitor establishes foothold",
          "supply_demand": "Competitor filling a segment you have underserved"
        }
      },
      {
        "id": "D2",
        "axis": "alternative_interpretation",
        "label": "Market Maturation Reading",
        "description": "The signal may reflect structural maturation of the core segment rather than a competitor action.",
        "implied_action": "Portfolio pivot. Evaluate adjacent segments rather than defending a naturally declining core.",
        "confidence": 0.58,
        "prime_directive_lenses": {
          "assets_liabilities": "Mixed — core asset still valuable but declining trajectory",
          "risk_reward": "Different risk profile than D1; maturation is slower but less reversible",
          "supply_demand": "Demand ceiling may have been reached; not a competitor effect"
        }
      }
    ],
    "dominant_dimension": "D1",
    "dominant_reasoning": "Signal pattern weights toward competitor action: price movement is sudden, not gradual; timing correlates with competitor product launch.",
    "collapsed_reading_warning": false,
    "resolution_required": false,
    "suppressed_axes": []
  }
}
```

---

## Suppressed Axes

If the model determines that a required axis is not applicable to this input, it must explicitly suppress it with a stated reason:

```json
"suppressed_axes": [
  {
    "axis": "time_horizon",
    "reason": "No decision horizon stated or implied by operator. Temporal dimension not evaluable."
  }
]
```

An axis that is suppressed without a stated reason fails validation and is treated the same as a missing axis.

---

## Validation Rules

The system applies these checks to every dimensional map before the output proceeds:

| Check | Pass | Fail |
|---|---|---|
| Schema completeness | All required fields present | Missing field → schema error → revised judgment call |
| Minimum dimensions | ≥ 2 dimensions present, OR suppressed axes justify a single dimension | 1 dimension, no suppression reasoning → collapsed_reading_warning set to true |
| Confidence ordering | dominant_dimension has highest confidence score | Dominant dimension is not highest confidence → inconsistency flag |
| PD lens coverage | Each dimension addresses all three PD lenses | Missing lens on any dimension → flag |
| Suppression justification | All suppressed axes have stated reasons | Suppressed without reason → treated as missing |

**Validation is not the LLM re-checking itself.** Validation is a structural integrity check performed by the system on the map the LLM returned.

---

## Collapsed Reading Detection

A collapsed reading occurs when the model returns only one dimension despite signal complexity that implies multiple valid interpretations.

**How it is detected:**
- If scenario detection returned a secondary scenario with confidence ≥ 0.55, at least one dimension must address the secondary scenario framing
- If Stage 1 extracted signals from multiple activation signal categories, the map must include dimensions that address the divergent signal sources
- If only one dimension is present and the above conditions are not met, `collapsed_reading_warning` is set to true

**What happens when collapsed reading is detected:**
- The output proceeds (not blocked)
- The operator sees the warning: "This analysis reflects a single reading of your situation. An alternative framing was possible but not developed. You may wish to consider [brief description of suppressed alternative]."
- The collapsed reading event is logged in the audit trail

---

## The Exception: Genuinely One-Dimensional Inputs

Some inputs are genuinely one-dimensional. The operator asks a narrow operational question where multiple strategic frames do not apply. In this case:

- The model produces one dimension
- No `collapsed_reading_warning` is set
- A `single_dimension_justified` flag is set to true with the model's reasoning

**The bar for this exception is high.** The governing question: "Would a thoughtful senior advisor have considered at least one alternative framing before answering?" If yes, a second dimension is required.

---

## How the Map Flows Through the Pipeline

```
Stage 5 (Judgment Call)
  → LLM produces dimensional map as part of structured output
  → System validates map (completeness, consistency, collapse detection)
  
Prime Directive Gate
  → Checks that all PD lenses appear in the dominant dimension
  → Does not re-evaluate alternative dimensions (that is Reintegration's role)

Recursive Reintegration (Stage 8D / Core 7 F7)
  → Check 2: Polymorphia Consistency
  → Verifies secondary dimensions were acknowledged or explicitly set aside
  → If secondary dimensions appear in the map but are not addressed in the 
     recommendation, Reintegration flags the omission

Operator Delivery
  → Dominant dimension drives the recommendation
  → Alternative dimensions are presented as "Alternative reading considered"
  → collapsed_reading_warning and resolution_required surface explicitly
```

---

## Operator Disclosure Format

When the operator receives the output, the Polymorphia section surfaces as:

```
PRIMARY READING (confidence: 87%)
[Dominant dimension description and implied action]

ALTERNATIVE READING CONSIDERED (confidence: 58%)
[Secondary dimension description]
[Stated reason why dominant reading was prioritized over this alternative]

[If collapsed_reading_warning = true]
NOTE: This analysis reflects a single reading. An alternative framing was 
identified but not fully developed. Consider whether [alternative] changes your view.
```

---

## Current Engine.py Mapping

The current `engine.py` already produces `actors`, `incentives`, and `asymmetries` as scaffolded Polymorphia fields. These map to the new schema as follows:

| Current field | New schema equivalent |
|---|---|
| `actors` | Populates `stakeholder_perspective` dimension's `description` |
| `incentives` | Populates `implied_action` fields across dimensions |
| `asymmetries` | Becomes a dimension or sub-element of `risk_opportunity_balance` dimension |

Stage 8C does not delete these fields — it replaces the template logic that produces them with the structured LLM output that produces the full dimensional map. The output object shape expands; it does not break.

---

## Design Principle

> The LLM proposes the map. The system governs the map. Polymorphia is not a label applied to the output after the fact — it is a structural requirement placed on the output before it is delivered. The difference between a system that has Polymorphia and a system that calls itself Polymorphic is the schema validation that enforces it.

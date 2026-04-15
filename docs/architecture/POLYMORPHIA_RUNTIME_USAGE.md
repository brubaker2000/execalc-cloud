# POLYMORPHIA_RUNTIME_USAGE.md

## Status
Draft v0.1

## Owner
Architecture / Core 7

## Position in Core 7
Framework 2 — Activates after Prime Directive framing is established, before memory and EKE corpus loading.

---

## What Polymorphia Is

Polymorphia is the Multi-Dimensional Logic (MDL) framework — the Core 7 component that prevents the system from collapsing a complex situation to a single interpretive axis.

Most analytical tools, and most human cognition under pressure, reduce complexity: bullish or bearish, good or bad, go or no-go. The reduction feels like clarity. It is usually the elimination of the most important information.

**Polymorphia holds multiple valid logical perspectives simultaneously and refuses to prematurely resolve them.**

The question Polymorphia answers is not "what is the right reading?" It is: "what are all the valid ways to read this situation, and what does each reading imply for what we should do?"

---

## Why It Is Framework 2

Framework ordering in Core 7 is not arbitrary. Polymorphia sits at position 2 because:

1. **Prime Directive** (Framework 1) establishes the evaluation frame — what lenses matter (assets/liabilities, risk/reward, supply/demand). It answers: *what are we evaluating against?*

2. **Polymorphia** (Framework 2) then applies those lenses across multiple simultaneous readings of the situation. It answers: *what are all the valid interpretations, filtered through those lenses?*

Polymorphia that runs without a Prime Directive frame is unconstrained; it produces interesting perspectives but no governed prioritization. Prime Directive that runs without Polymorphia collapses the situation before the full picture can be seen.

---

## Runtime Activation

### When Polymorphia Fires

Polymorphia is active on every input. It is not a conditional component. Every situation that enters the judgment pipeline receives multi-dimensional analysis.

The **depth** of Polymorphia activation scales with situational complexity:

| Signal Pattern | Activation Depth |
|---|---|
| Single clear scenario, high-confidence signals | Lightweight — 2–3 dimensions identified |
| Multiple scenario candidates with overlapping signals | Full depth — all valid frames enumerated |
| Conflicting signals or ambiguous framing | Maximum depth — dimensions surfaced and ranked; operator must resolve before judgment proceeds |
| High-stakes or irreversible decision class | Full depth regardless of signal clarity |

---

## What Polymorphia Produces

Polymorphia's output is a **dimensional map** — a structured list of valid interpretive lenses for the current situation, each with its implied reading and decision consequence.

### Dimensional Map Structure

```
{
  "situation_summary": "...",
  "dimensions": [
    {
      "id": "D1",
      "label": "Competitive Threat Reading",
      "frame": "The signal pattern suggests market share erosion from a direct competitor.",
      "implied_action": "Defensive posture; accelerate differentiation or reduce price exposure.",
      "confidence": 0.87,
      "primary_directive_lenses": {
        "assets_liabilities": "Negative — margin erosion likely",
        "risk_reward": "Asymmetric downside if unaddressed",
        "supply_demand": "Competitor filling undefended segment"
      }
    },
    {
      "id": "D2",
      "label": "Market Maturation Reading",
      "frame": "The signal may reflect structural market maturation rather than a competitor action.",
      "implied_action": "Portfolio pivot; current product may be past peak; explore adjacencies.",
      "confidence": 0.61,
      "primary_directive_lenses": {
        "assets_liabilities": "Mixed — core asset still valuable but declining",
        "risk_reward": "Different risk profile from D1",
        "supply_demand": "Demand ceiling may have been reached"
      }
    }
  ],
  "collapsed_reading_warning": false,
  "resolution_required": false,
  "dominant_dimension": "D1"
}
```

If `resolution_required` is true, the system surfaces the dimensional map to the operator and does not proceed to judgment until the operator confirms the framing.

---

## Collapsed Reading Warning

Polymorphia carries a governance obligation: it must detect and flag when a situation has been prematurely collapsed to a single reading.

**Collapse triggers when:**
- Only one dimension is identified despite ambiguous signals
- The dominant dimension has confidence below 0.70 but no secondary dimension is generated
- Operator inputs explicitly assert a single framing that the signal evidence does not fully support

When collapse is detected, the system does not silently accept the single-dimension reading. It surfaces:

```
POLYMORPHIA WARNING: This situation may support multiple valid interpretations. 
The current framing collapses it to [label]. 
Suppressed alternatives: [list]. 
Confirm this framing before proceeding?
```

---

## Polymorphia and Uncertainty

Polymorphia does not resolve uncertainty. It governs how uncertainty is handled:

1. **Named uncertainty** — dimensions that exist but cannot be ranked with confidence are labeled as unresolved and presented explicitly
2. **Resolution pathway** — for each unresolved dimension, the system identifies what information would resolve it
3. **Partial progression** — where a dominant dimension has sufficient confidence, judgment may proceed on that dimension while the unresolved dimensions remain open and flagged

> "The sin isn't imbalance. The sin is blindness." — Prime Directive Enforcement Doctrine

Polymorphia's version of this: the sin is not complexity. The sin is pretending the situation is simpler than it is.

---

## Relationship to Other Core 7 Components

| Component | Relationship |
|---|---|
| Prime Directive (F1) | Sets the evaluation lenses Polymorphia applies across dimensions |
| Persistent Memory (F3) | Past operator decisions on similar multi-dimensional situations inform dimension weighting |
| EKE (F4) | Corpus entries are loaded per dimension, not per situation — different frames pull different frameworks |
| Proactive Solutions Architecture (F6) | PSA activates per dimension — different dimensions may trigger different proactive alerts |
| Recursive Reintegration (F7) | Final output review checks that the delivered recommendation did not silently collapse the Polymorphia output |

---

## Audit Requirements

Every Polymorphia activation must produce an audit record containing:
- All dimensions identified
- Confidence score per dimension
- Whether a collapsed reading warning was triggered
- Whether operator resolution was required and how it was resolved
- Which dimension was designated dominant and why

---

## Design Principle

> Polymorphia is not the framework that finds the answer. It is the framework that prevents the wrong answer from being found too fast.

The value of Polymorphia is not in the complexity it generates — it is in the collapses it prevents. An analysis that correctly identifies three valid readings and explicitly designates one dominant is more trustworthy than an analysis that identified only one reading and was never challenged on it.

The governing standard: **every dimension that a thoughtful senior advisor would have considered must appear in the output.** Polymorphia is the guarantee that it does.

# SCENARIO_DETECTION_ALGORITHM.md

## Status
Draft v0.1 — Pre-Stage-8 blocker spec

## Owner
Architecture / Stage 8B

## Purpose
This document specifies the scenario detection algorithm — the mechanism by which Stage 2 of the Reflex and Activation System maps extracted signals to one or more of the 25 canonical scenarios with a confidence score.

This spec exists because "score each scenario against matched signals" is not an algorithm. This document makes it one.

---

## Why This Is the Most Critical Decision in Stage 8

If scenario detection is wrong, everything downstream is wrong.

The context package assembled in Stage 4, the reflexes fired in Stage 3, the corpus entries loaded, the Carats activated, the Prime Directive frame applied — all of these depend on the correct scenario being identified in Stage 2. A misclassification at this stage produces a plausible-sounding but incorrectly framed output. That is not a cosmetic error. It is a governance failure.

The algorithm must therefore be:
- **Robust** — not dependent on exact keyword matches
- **Explainable** — every score must be traceable to the evidence that produced it
- **Multi-method** — no single scoring mechanism is reliable across all input types
- **Escalation-aware** — when confidence is genuinely low, escalate rather than guess

---

## The Hybrid Three-Layer Model

Scenario detection uses three scoring layers in sequence. Each layer produces a score contribution. The layers are combined via weighted blend. LLM arbitration is reserved for genuine ambiguity — it is not the default mechanism.

```
Layer 1: Deterministic Signal Match  (fast, cheap, reliable for clear cases)
Layer 2: Embedding Similarity         (context-aware, handles paraphrase)
Layer 3: LLM Arbitration             (tie-breaker only, Opus-class, expensive)
                ↓
       Confidence Score (0.0 – 1.0)
                ↓
     Primary + Secondary Scenario
```

---

## Layer 1: Deterministic Signal Match

**What it does:** Score each of the 25 scenarios against the extracted signals from Stage 1 using the activation signal list defined in `SCENARIO_REGISTRY.md`.

**How it works:**

For each scenario, count how many of its defined `Activation Signals` appear in the signal list from Stage 1. Weight by signal specificity:

| Signal Type | Weight |
|---|---|
| Exact phrase match | 1.0 |
| Stem/partial match | 0.6 |
| Semantic synonym (rule-based) | 0.4 |

**Score formula:**

```
L1_score(scenario) = Σ(matched_signal_weights) / max_possible_score
```

Where `max_possible_score` is the theoretical maximum if all activation signals for that scenario matched.

**Model tier:** Rule-based. No model call.

**Output:** Raw L1 score (0.0–1.0) per scenario.

**Strength:** Fast, deterministic, auditable. Every score traces directly to matched signal text.  
**Weakness:** Brittle for paraphrase, domain-specific language, or unusual framing.

---

## Layer 2: Embedding Similarity

**What it does:** Compute vector similarity between the operator's input and each scenario's definition + trigger conditions.

**How it works:**

1. Embed the operator's raw input text using a lightweight embedding model
2. Embed each scenario's definition + trigger conditions (pre-computed at system init; not recomputed per request)
3. Compute cosine similarity between input embedding and each scenario embedding
4. Normalize to 0.0–1.0 scale

**Scenario embeddings are pre-computed** at startup and cached. Only the input embedding is computed per request. This keeps Layer 2 fast.

**Model tier:** Labor (embedding model, not generative). Haiku-class or dedicated embedding model.

**Output:** Raw L2 score (0.0–1.0) per scenario.

**Strength:** Handles paraphrase, domain-specific language, and inputs that don't use the activation signal vocabulary.  
**Weakness:** Can return high similarity scores for superficially similar but contextually different situations.

---

## Blended Score (After Layers 1 and 2)

Combine L1 and L2 scores with the following weights:

```
blended_score(scenario) = (0.60 × L1_score) + (0.40 × L2_score)
```

**Rationale for weighting:**
- L1 is deterministic and directly tied to the governance doctrine in `SCENARIO_REGISTRY.md`. It should dominate.
- L2 provides context-awareness but is noisier. It supplements, not overrides.

These weights are v0.1 defaults. They should be calibrated against real session data during Stage 8 testing.

**After blending:** Rank all 25 scenarios by blended score. Identify primary (highest) and secondary (second highest).

---

## Layer 3: LLM Arbitration (Tie-Breaker Only)

**Trigger condition:** Layer 3 fires ONLY when:

```
blended_score(primary) - blended_score(secondary) < 0.15
```

This means the top two scenarios are within 15 percentage points of each other. This is genuine ambiguity — not a case where one scenario is clearly dominant.

**What it does:** Present the top 3 scenarios (with their definitions and the operator's input) to an Opus-class model and ask it to classify.

**Prompt structure:**
```
The following input has been submitted to a governed executive judgment system.
Classify it as one of these scenarios. Return only the scenario ID and a one-sentence reasoning.

Input: [operator input]

Candidate scenarios:
[Scenario A — definition + trigger conditions]
[Scenario B — definition + trigger conditions]
[Scenario C — definition + trigger conditions]
```

**Output:** LLM classification + reasoning sentence.

**Score update:** LLM classification sets the primary scenario. The LLM's confidence language is mapped to a numeric confidence:
- "clearly" / "strongly" / "unambiguously" → 0.85
- "likely" / "probably" → 0.75
- "possibly" / "may be" / "could be" → 0.65
- Expresses uncertainty → ambiguity_flag = true

**Model tier:** Premium (Opus-class). This is the only model call in Stage 2.

**Audit requirement:** Every Layer 3 invocation must be logged with: trigger condition (why L3 fired), candidate scenarios, LLM output, resulting classification.

---

## Confidence Threshold and Escalation

After all three layers:

| Final Confidence | Action |
|---|---|
| ≥ 0.70 | Proceed with primary scenario |
| 0.55 – 0.69 | Surface top 2 scenarios to operator; request confirmation before proceeding |
| < 0.55 | Ambiguity flag = true; surface top 3 candidates; route to Scenario 21 (Opportunity Discovery) as safe container if operator does not resolve |

**The 0.70 threshold is a calibration target, not a fixed invariant.** During Stage 8 testing, this threshold should be evaluated against real session data. If the system is escalating too frequently (>20% of sessions), recalibrate Layer 1/L2 weights or lower the threshold. If it is escalating too rarely and producing low-quality downstream reasoning, raise it.

---

## Audit Output Contract

Every Stage 2 run must produce:

```json
{
  "l1_scores": { "scenario_id": score, ... },
  "l2_scores": { "scenario_id": score, ... },
  "blended_scores": { "scenario_id": score, ... },
  "l3_triggered": false,
  "l3_result": null,
  "primary_scenario": { "id": 18, "name": "Competitive Threat", "confidence": 0.87 },
  "secondary_scenario": { "id": 3, "name": "Pricing and Positioning", "confidence": 0.61 },
  "ambiguity_flag": false,
  "escalation_required": false
}
```

This record is the proof that scenario detection was performed correctly and through what evidence. Without it, the governed reasoning is not reconstructable.

---

## Implementation Notes for Stage 8B

1. Scenario signal lists from `SCENARIO_REGISTRY.md` must be loaded into a signal lookup at service init — not read from file on every request.
2. Scenario embeddings must be pre-computed at init and cached — not computed per request.
3. The L1 synonym table (for semantic synonym matching) must be defined explicitly — not inferred. Start with a minimal synonym set for the most common signal variants.
4. Layer 3 should be rate-budget-tracked — if L3 is firing on >30% of inputs, the L1/L2 layers are under-performing and need recalibration, not more LLM spend.

---

## Design Principle

> Scenario detection must be multi-method, not single-method. No single mechanism is reliable across all input types. The hybrid model produces scores that are auditable, calibratable, and escalation-aware — and reserves expensive model calls for genuine ambiguity, not routine classification.

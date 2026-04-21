# CARAT_ACTIVATION_DISCIPLINE.md

## Status
Canonical v1.0

## Owner
Executive Knowledge Engine (EKE) / Activation Engine

---

## The Core Problem

Context is not free. Loading too many frameworks, nuggets, and carats into the reasoning context does not improve output quality — it degrades it.

This is not a performance concern. It is a reasoning quality concern.

Large language models degrade under context clutter. Load twelve frameworks into the context package and the model does not apply all twelve well. It produces a diluted version of each, or gravitates toward whichever framework dominated its training data. The result is the *appearance* of multi-framework reasoning without the substance.

This failure mode is insidious because the output looks rigorous. It cites multiple frameworks, uses the right vocabulary, and sounds authoritative. But the reasoning is diluted — each framework got a fraction of the attention it needed to be useful.

> **Over-loading with plausibly relevant frameworks produces confident-sounding output built on shallow application. This is exactly what ungoverned AI does. The activation discipline exists to prevent governed AI from making the same mistake.**

---

## The Governing Principle

> **Load the minimum set that guarantees the situation is seen correctly. Add depth only when the situation demands it.**

This is the single governing rule for context assembly. Every other rule in this document is a consequence of it.

---

## The Lawyer Analogy

A lawyer who has read every case ever decided is only useful if they know which two or three precedents are actually controlling for this specific argument.

Citing forty cases does not strengthen the brief. It weakens it — it signals that the lawyer could not identify what was actually determinative, so they included everything plausibly relevant and hoped the judge would sort it out.

The EKE corpus and the carat registry exist so the system *can* load the right frameworks. The activation discipline exists so it *only* loads the ones doing real work for this specific situation.

The same principle governs the grandmaster in speed chess. They do not run every calculation available to them. They pattern-match to the two or three frameworks most load-bearing for this position and reason from there. Breadth of knowledge is not the advantage. Knowing which knowledge is controlling right now is.

---

## What "Doing Real Work" Means

A framework, nugget, or carat is doing real work if:

1. **It changes what gets scrutinized.** Without it, a material risk, asymmetry, or leverage point would go unexamined.
2. **It changes the reasoning posture.** It orients the model toward a question or dimension it would not otherwise prioritize.
3. **It is specific to this situation.** It is not merely plausible — it is actually relevant to the scenario and signals present.

If a carat or nugget does not clear at least one of these tests, it should not be in the context package for this session.

---

## Tiered Carat Activation

### Tier 1 — Always-On (1–3 carats per scenario)
These fire automatically whenever the scenario is classified. They are load-bearing: the reasoning is materially worse without them. The always-on set for any scenario is deliberately small.

Examples:
- Crisis Management → Survivability First always fires
- Negotiation / Deal Dynamics → Tempo Control + Asymmetric Advantage always fire
- Capital Raise → Risk-Weighted Return + Survivability First always fire

### Tier 2 — Conditional (remaining eligible carats)
These fire only when specific signals in the input indicate they are needed.

- Second-Order Effects fires for Negotiation when signals indicate a multi-party dynamic
- Signal-to-Noise Suppression fires when signals indicate spin, narrative control, or information management
- Bias Neutralization fires when signals indicate the operator is emotionally invested in a specific outcome

If the signal is not present, the carat stays dormant. It does not get loaded "just in case."

**The rule:** conditional carats require a positive activation signal, not merely the absence of a reason to exclude them.

---

## The One Primary, One Secondary Rule

Most sessions have one dominant scenario and at most one secondary.

- The **primary scenario** loads its always-on carats in full.
- The **secondary scenario** loads only its single highest-priority carat — the one most likely to add something not already covered by the primary set.

This prevents combinatorial explosion when scenarios overlap.

A Capital Raise under competitive pressure does not need the full Competitive Conflict carat set. It needs Survivability First and Risk-Weighted Return from the capital scenario, and at most one carat from the competitive scenario — the one that adds something the capital carats do not already cover.

---

## Corpus Entry Discipline

The same principle applies to EKE corpus entries — thought leadership nuggets, monolith patterns, thinker activations.

A nugget injection is two to four sentences distilling the applicable insight. It is not a biography, a full framework explanation, or a literature survey. The corpus anchor is available if the model needs to go deeper — it is not pre-loaded.

**The target context package for a standard governed session:**
- One scenario clearly classified
- Two to three always-on carats
- Zero to two conditional carats (only if signals warrant)
- One to two thinker nuggets that are specifically relevant
- Sufficient reasoning space for the model to actually think

That is a sharp context package. It arrives prepared, not cluttered.

---

## Progressive Depth

The first pass loads lean. This produces a governed first-pass output.

If the operator pushes deeper — asks a follow-on, requests more rigor, or the Prime Directive evaluation returns FLAG — the next pass escalates:
- Conditional carats activate
- Additional corpus entries load
- Data layers are queried if relevant

Depth is not refused. It is staged. The system does not front-load everything it knows about a topic before understanding what the operator actually needs.

---

## Context Package Priority Order

When the budget is constrained, items are trimmed in reverse priority — lowest priority first. The governance layer is never trimmed.

```
1. Compliance constraints          ← never trimmed
2. Prime Directive frame           ← never trimmed
3. Always-on carats                ← never trimmed
4. Scenario logic                  ← trimmed only under severe constraint
5. Conditional carats              ← trimmed when budget is tight
6. EKE corpus entries              ← trimmed to the most relevant
7. Operator memory                 ← summarized if necessary
8. Session context                 ← always present but compressed
```

---

## The Failure Mode to Prevent

The worst failure mode is not under-loading. Under-loading produces generic output — recognizable and correctable.

The worst failure mode is **over-loading with plausibly relevant content that is not actually controlling**. This produces:

- Output that cites many frameworks but applies none of them sharply
- Confident language that obscures shallow reasoning
- The appearance of rigor without the substance

This is what ungoverned AI already does. A governed system that over-loads its context package has added process without adding quality. It has made the mistake more elaborate, not less.

**The activation discipline is what separates a prepared context from a cluttered one.**

---

## Calibration Over Time

Recursive Analysis feeds outcome data back into the activation engine. Over time, the system learns which carats actually contributed to outcome quality for which scenarios.

A carat that is consistently activated but never materially changes the reasoning gets demoted from always-on to conditional. A conditional carat that consistently improves output gets promoted.

This is how the activation engine becomes more precise without being redesigned. The 37-scenario × 25-carat space gets progressively mapped to what actually works — not by architectural change, but by evidence accumulation.

---

## Relationship to Existing Doctrine

| Document | Relationship |
|---|---|
| `CARAT_REGISTRY_PHASE1.md` | The 25 carats this discipline governs |
| `SCENARIO_REGISTRY.md` | The 37 scenarios that select eligible carats |
| `EXECUTIVE_KNOWLEDGE_ENGINE_ACTIVATION_AND_SIGNALING_MODEL.md` | The broader activation and signaling model |
| `EXECALC_COGNITIVE_ENGINE_ARCHITECTURE.md` | Where carat activation sits in the cognitive loop |
| `REFLEX_AND_ACTIVATION_SYSTEM.md` | Stage 4 — context package assembly |
| `RUNTIME_REASONING_SEPARATION.md` | The platform governs what reasoning receives; this doc defines how |

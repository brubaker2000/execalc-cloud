# REFLEX_AND_ACTIVATION_SYSTEM.md

## Status
Draft v0.1

## Owner
Executive Knowledge Engine (EKE) / Runtime Layer

## Purpose
This document specifies the Reflex and Activation System — the detection and loading layer that fires before any LLM judgment call.

Its job is to answer one question as fast and accurately as possible:

> **What situation is this, and what logic should be loaded to handle it?**

Everything downstream — the EKE corpus, the Carats, the Prime Directive evaluation, the decision artifact — depends on this layer getting the answer right. A misclassified situation loads the wrong logic and produces a plausible-sounding but incorrectly framed output. That is a governance failure.

This system is not the judge. It is the dispatcher.

---

## Why This Layer Exists

The LLM has broad capability but no automatic situational awareness. Given a negotiation scenario, it will not automatically load Voss's calibrated questions, Clausewitz's center of gravity logic, and the BATNA framework — unless something loads that context before the call begins.

The Reflex and Activation System is that something.

It pre-encodes situational judgment so the LLM call begins with the right lenses already active, not with a blank context that relies on the model to self-navigate.

This is the grandmaster analogy made operational: the grandmaster does not calculate from scratch in speed chess — they pattern-match to pre-loaded frameworks. The Reflex and Activation System is the pattern-matching layer.

---

## Stage 0: Strategic Terrain Classification

Before signal extraction begins, every input is classified by **strategic terrain** — the problem type that the input belongs to. This is the enforced first-pass ingress tag.

Terrain classification fires before polarity detection, before thinker activation, and before carat selection. Without it, Polymorphia activates later than it should, and scenario matching operates on raw signal rather than on a pre-classified problem frame.

**Terrain classes (non-exhaustive):**
- Competitive war
- Capital structure / allocation
- Internal alignment / execution breakdown
- Reputation / signal integrity
- Deal / transaction
- Operational bottleneck
- Strategic drift
- Market entry / expansion
- Relationship / negotiation

**Rule:** Every input receives a terrain tag before the cascade continues. If the terrain is genuinely ambiguous, it is flagged as such — not silently defaulted. The terrain tag is carried through all subsequent stages and appears in the run receipt.

**Model tier:** Labor (rule-based or Haiku-class — this is classification, not judgment)

---

## The Five-Stage Detection Cascade

### Stage 1: Signal Extraction

**What it does:** Identifies activation signals present in the raw input.

**How it works:**
- Scan input text for phrases, keywords, and patterns that match the activation signal library
- Each of the 25 scenarios carries a signal list (see `SCENARIO_REGISTRY.md`)
- Signal extraction is a lightweight operation — Haiku-class model or rule-based matching
- Output: a scored list of matched signals with source text references

**Model tier:** Labor (cheapest safe — this is extraction, not judgment)

**Output contract:**
```
{
  "matched_signals": [
    { "signal": "losing share", "source": "we are losing share to...", "scenario_candidates": [18] },
    { "signal": "competitor", "source": "their new product...", "scenario_candidates": [18, 3] }
  ],
  "unmatched_content": "...",
  "extraction_confidence": 0.87
}
```

**Null pathway — no signals found:**

If Stage 1 finds no activation signals, the cascade does not continue.

The input is a general query. The system responds directly through the LLM without loading scenario context, reflexes, Carats, corpus entries, or Prime Directive evaluation framing. The response is clean, capable, and ungoverned — because nothing in the input called for governance.

This is an explicit design principle, not a fallback:

> **The governed architecture is not a wrapper around every response. It is triggered by situation recognition. No situation — no activation. But no activation does not mean no capability.**

The null pathway is not a degraded experience. The operator has access to a fully capable general-purpose assistant with internet access — the full power of the underlying LLM and its connected resources. An operator asking for baseball statistics gets baseball statistics. An operator asking for a recipe gets a recipe. An operator researching a topic gets web-assisted research.

The governed architecture remains invisible until the situation calls for it — which is what makes the system feel like a knowledgeable peer rather than a compliance gate. The peer is always capable. It is selectively governed.

**Null pathway output contract:**
```
{
  "matched_signals": [],
  "unmatched_content": "...",
  "extraction_confidence": 0.00,
  "pathway": "null — general response, no activation cascade"
}
```

The null pathway routes directly to a standard LLM call. No audit record is required beyond logging that the null pathway was taken. The session context (operator, tenant) remains active for subsequent inputs.

---

### Stage 2: Scenario Detection

**What it does:** Maps extracted signals to one or more of the 25 canonical scenarios.

**How it works:**
- Score each scenario against the matched signals
- A scenario scores higher when multiple signals align to it
- Consider trigger conditions, not just signal keywords — the full scenario definition matters
- Output: ranked scenario candidates with confidence scores

**Model tier:** Labor for simple cases; Premium (Opus-class) when signals are ambiguous or contradictory

**Output contract:**
```
{
  "primary_scenario": { "id": 18, "name": "Competitive Threat", "confidence": 0.91 },
  "secondary_scenario": { "id": 3, "name": "Pricing and Positioning", "confidence": 0.62 },
  "considered_but_rejected": [
    { "id": 17, "name": "Risk Mitigation", "confidence": 0.31, "reason": "signals are competitive, not general risk" }
  ],
  "ambiguity_flag": false
}
```

**Escalation rule:** If no scenario reaches 0.70 confidence, the ambiguity flag is set to true. The runtime surfaces the top 2–3 candidates to the operator and requests clarification before proceeding. It does not silently route to a low-confidence scenario.

**Default fallback:** If ambiguity cannot be resolved, route to Scenario 21 (Opportunity Discovery) as the broadest safe container and request clarifying input.

---

### Stage 3: Reflex Gate

**What it does:** Determines which pre-loaded response patterns (reflexes) fire for the detected scenario.

**How it works:**
- Each scenario has an associated reflex set — pre-encoded patterns that activate automatically
- Reflexes are not the judgment. They are priming logic: what questions to ask, what lenses to apply, what warnings to surface
- The reflex gate checks each candidate reflex against the active scenario and the input content
- Reflexes may be suppressed if the input signals indicate the reflex is not applicable

**Model tier:** Rule-based (no model call needed for standard cases)

**Reflex types:**
- **Diagnostic reflex** — surfaces questions the operator should answer before a decision is made
- **Warning reflex** — flags known risks associated with this scenario type
- **Framework reflex** — pre-loads a specific analytical framework relevant to this scenario
- **Posture reflex** — sets the recommended stance (aggressive, conservative, patient, etc.)

**Example — Scenario 7 (Negotiation) reflex set:**
- Diagnostic: "What is the BATNA? What is the counterpart's BATNA?"
- Warning: "Silence after an anchor is not rejection — wait before speaking"
- Framework: Load Voss calibrated question protocol (HTL-0142)
- Posture: Tactical empathy posture active (HTL-0139)

**Output contract:**
```
{
  "active_reflexes": [
    { "type": "diagnostic", "content": "What is the BATNA?", "priority": 1 },
    { "type": "warning", "content": "Silence after anchor is not rejection", "priority": 2 },
    { "type": "framework", "corpus_id": "HTL-0142", "priority": 3 },
    { "type": "posture", "value": "tactical_empathy", "priority": 4 }
  ],
  "suppressed_reflexes": [],
  "reflex_gate_version": "v0.1"
}
```

---

### Stage 4: Activation Pathway

**What it does:** Loads the full context package the LLM judgment call will receive.

**How it works:**
- Pull all EKE corpus entries associated with the detected scenario
- Load eligible Carats for this scenario (per Carat Registry activation criteria)
- Apply any active compliance cartridges as highest-priority constraints
- Assemble the context package in priority order: compliance → Carats → scenario logic → corpus entries → operator history

**Model tier:** No model call — this is assembly, not reasoning

**Context package structure:**
```
{
  "compliance_constraints": [...],        // active compliance cartridges, if any
  "active_carats": [...],                 // loaded Carat overlays
  "scenario_context": { ... },            // detected scenario definition + primary output template
  "active_reflexes": [...],               // from Stage 3
  "corpus_entries": [...],                // relevant EKE Monolith / Nugget entries
  "operator_memory": [...],               // admitted memory relevant to this scenario
  "prime_directive_frame": { ... },       // the two-tier PD structure pre-loaded
  "session_context": { ... }              // current operator, tenant, session metadata
}
```

**Priority order within the context package:**
1. Compliance constraints (overrides everything)
2. Prime Directive frame (evaluation lens)
3. Active Carats (strategic overlays)
4. Scenario logic (what this situation requires)
5. Active reflexes (pre-loaded patterns)
6. EKE corpus entries (relevant heuristics/frameworks)
7. Operator memory (historical governed claims)
8. Session context (current state)

---

### Stage 5: Judgment Call

**What it does:** The actual LLM call, with the full context package loaded.

**How it works:**
- The model receives the context package, the operator's input, and the output template for the detected scenario
- The model reasons within the loaded context — it does not need to self-navigate the situation from scratch
- Output is structured according to the scenario's primary output definition
- The model must produce a traceable output: every claim must reference the context that supports it

**Model tier:** Premium (Opus-class) — this is judgment, not labor

**Output is not final:** The judgment call output passes to the Prime Directive evaluation gate before delivery.

---

## Scenario-to-Corpus Mapping (v0.1)

Pre-loaded corpus associations for each scenario bucket. Full per-scenario mapping is a follow-on spec.

| Scenario Bucket | Primary Corpus Associations |
|---|---|
| Growth & Opportunity | Drucker (HTL-0015 to 0021), Bezos (HTL-0055 to 0061), Christensen (HTL-0125 to 0131), Porter (HTL-0132 to 0138), Jay Abraham (JA-0001 to 0006) |
| Deal & Capital | Voss (HTL-0139 to 0145), Munger (HTL-0035 to 0041), Taleb (HTL-0118 to 0124), Jay Abraham (JA-0001 to 0006) |
| Org & Execution | Covey (HTL-0001 to 0007), Welch (HTL-0076 to 0082), Grove (HTL-0090 to 0096), Willink (HTL-0029 to 0034) |
| Risk & Defense | Sun Tzu (HTL-0022 to 0028), Clausewitz (HTL-0104 to 0110), Taleb (HTL-0118 to 0124), Kahneman (HTL-0111 to 0117) |
| Strategic Insight | Munger (HTL-0035 to 0041), Musk (HTL-0062 to 0068), Boyd (HTL-0097 to 0103), Perry Marshall (PM-0001 to 0038) |

---

## Reflex Registry (v0.1 — Starter Set)

The following reflexes are pre-loaded for the most critical scenarios. Full registry is a follow-on spec.

| Scenario | Reflex | Type | Corpus Anchor |
|---|---|---|---|
| 7 — Negotiation | What is the BATNA? | Diagnostic | — |
| 7 — Negotiation | Silence after anchor is not rejection | Warning | HTL-0142 |
| 7 — Negotiation | Tactical empathy posture | Posture | HTL-0139 |
| 7 — Negotiation | Label emotions before making moves | Framework | HTL-0141 |
| 16 — Crisis Management | Contain before communicating | Posture | — |
| 16 — Crisis Management | Who needs to know right now? | Diagnostic | — |
| 16 — Crisis Management | What is the survivability exposure? | Warning | PD-022 |
| 8 — Due Diligence | What assumptions have not been tested? | Diagnostic | HTL-0036 |
| 8 — Due Diligence | Invert: what would make this deal fail? | Framework | HTL-0036 |
| 18 — Competitive Threat | Where are they unprepared? | Framework | HTL-0025 |
| 18 — Competitive Threat | Are we fighting or flanking? | Diagnostic | HTL-0023 |
| 14 — Strategic Drift | Name the three most important things | Diagnostic | HTL-0003 |
| 14 — Strategic Drift | What would you stop doing today? | Framework | HTL-0019 |

---

## Explainability vs. Traceability

These are not the same thing and must not be treated as such.

**Explainability** is a narrative. It is the system's ability to produce a coherent account of why something happened. Explainability is useful for operator communication. It is not sufficient for governance.

**Traceability** is a record. It is the system's ability to prove — from auditable artifacts — what logic fired, under what constraints, with what result. Traceability does not depend on the model's ability to articulate its reasoning. It depends on the runtime's audit trail.

Execalc commits to traceability. Explainability is a secondary output — useful when it can be produced, but never a substitute for the audit record.

> If the run receipt exists and the explanation does not, governance is intact.  
> If the explanation exists and the run receipt does not, governance has failed.

This distinction matters for regulated environments, legal review, and enterprise buyers. They do not need the system to tell a good story. They need to be able to verify what happened.

---

## Audit Requirements

Every detection cascade run must produce an audit record containing:

- raw input hash (for traceability without storing raw content)
- signals extracted and matched
- scenarios considered and their confidence scores
- primary and secondary scenario designations
- reflexes activated and suppressed
- Carats loaded
- corpus entries loaded
- compliance constraints active
- model tier used at each stage
- timestamp

This audit record is the proof that the system's logic was activated correctly for this situation. Without it, governed judgment is not reconstructable.

---

## Current Code State

The existing `support_stack.py` contains a `ReflexRegistry` and `ReflexGateDecision` class that are Phase 1 scaffolding. The gate currently returns allow-all. The `ReflexRegistry` is in-memory with no persistence and no scenario association.

Stage 8 replaces this scaffolding with the five-stage cascade defined above. The data models in `support_stack.py` can be extended; the gate logic must be rebuilt.

---

## Required Follow-On Specs

1. `SCENARIO_CARAT_MAPPING.md` — which Carats are eligible for each of the 25 scenarios
2. `SCENARIO_CORPUS_MAPPING.md` — full per-scenario corpus entry associations
3. `REFLEX_REGISTRY_FULL.md` — complete reflex set for all 25 scenarios
4. `ACTIVATION_PATHWAY_CONTRACT.md` — formal schema for the context package
5. `JUDGMENT_CALL_OUTPUT_CONTRACT.md` — what the LLM must produce, per scenario

---

## Design Principle

The Reflex and Activation System is not intelligence. It is preparation.

By the time the LLM receives the input, the situation should already be classified, the relevant logic already loaded, and the output template already primed. The model's job is to reason within a prepared context — not to navigate a blank page.

The difference between a governed judgment system and a raw LLM call is exactly this preparation layer.

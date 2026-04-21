# EXECALC_COGNITIVE_ENGINE_ARCHITECTURE.md

## Status
Canonical v1.0

## Owner
Architecture / Core 7

---

## Purpose

This document defines the Cognitive Engine architecture of Execalc — the runtime model showing how the Seven Core Governance Frameworks interact as a unified loop.

Each framework has its own specification document. This document is not a replacement for those specs. It is the map that shows how the seven parts connect and in what order they fire.

Without this map, the frameworks exist as independent doctrine. With it, they become an executable governance loop.

---

## The Seven Core Governance Frameworks (Canonical Order)

The Core 7 operate in serial order. Order is not arbitrary — each framework unlocks the next.

| Position | Framework | Role in the Loop |
|---|---|---|
| 1 | Prime Directive | Governing compass — defines what counts as a valid output |
| 2 | Multi-Dimensional Logic (MDL) / Polymorphia | Multi-actor, multi-lens situational modeling |
| 3 | Persistent AI Memory | Governed accumulation of institutional intelligence |
| 4 | Executive Knowledge Engine (EKE) | Knowledge activation — loads the right inputs |
| 5 | Heuristic Coding System | Strategic instinct library — encoded operator and thinker heuristics |
| 6 | Proactive Solutions Architecture | Pre-loaded response patterns activated by situation recognition |
| 7 | Recursive Analysis | Self-referential examination of outputs against doctrine |

---

## The Cognitive Loop

```
Operator Input / Ambient Signal
        ↓
[Stage 0] Strategic Terrain Classification
        ↓
[Stage 1–3] Reflex and Activation System
  (Signal extraction → Scenario detection → Reflex gate → Context assembly)
        ↓
[EKE] Knowledge Activation
  Monolith patterns + relevant nuggets + cartridges + data sources
        ↓
[Polymorphia] Multi-Actor Strategic Modeling
  Actor map + incentive map + asymmetry analysis
        ↓
[Heuristic Coding System] Strategic Instinct Activation
  Domain-matched heuristics injected into reasoning context
        ↓
[Stage 5] Judgment Call (Premium model)
  Full context package → structured decision artifact
        ↓
[Prime Directive] Governance Gate
  Three-lens evaluation → PASS / FLAG / ESCALATE / BLOCK
        ↓
Output delivered (or withheld)
        ↓
[Persistent Memory] Admission Gate
  Governed write: does this output meet admission criteria?
        ↓
[Recursive Analysis] Feedback Loop
  Outcome vs. assumptions → heuristic reinforcement or revision
        ↓
[Proactive Solutions Architecture] Opportunity / Risk Detection
  Pattern detection across memory → surface signals without being asked
```

---

## Stage-by-Stage Description

### Stage 0 — Strategic Terrain Classification
Before any framework fires, every input receives a terrain tag: competitive war, capital structure, deal, execution breakdown, crisis, market entry, negotiation, etc. This tag determines which frameworks are most active downstream.

**Model tier:** Labor (Haiku-class or rule-based)  
**Spec:** `REFLEX_AND_ACTIVATION_SYSTEM.md §Stage 0`

---

### EKE — Knowledge Activation
The Executive Knowledge Engine selects which knowledge enters the reasoning context. It does not retrieve everything — it activates the lightest sufficient knowledge set for the detected terrain and scenario.

Knowledge strata accessed in priority order:
1. Compliance constraints (if active)
2. Client cartridges (tenant-specific policy)
3. Execalc runtime cartridges
4. Thought leadership nuggets (reflex-triggered)
5. Monolith patterns (always-on baseline)
6. Data lakes (query-based)
7. Internet search (on-demand, lowest trust weight)

**Spec:** `EXECUTIVE_KNOWLEDGE_ENGINE_STRATA.md`, `EXECUTIVE_KNOWLEDGE_ENGINE_ACTIVATION_AND_SIGNALING_MODEL.md`

---

### Polymorphia — Multi-Actor Strategic Modeling
Polymorphia evaluates the situation from multiple valid logical perspectives simultaneously. It models competing actors, incentive structures, and power asymmetries.

Required output fields: `actors`, `incentives`, `asymmetries`

**Activation rule:** Required for any scenario involving negotiation, financing, partnership, regulatory interaction, or multi-party strategy.

**Invariant:** Polymorphia lenses are read-only — they observe, annotate, and surface tension but cannot write to memory or trigger execution.

**Spec:** `POLYMORPHIA_RUNTIME_SPEC.md`

---

### Heuristic Coding System — Strategic Instinct Activation
The Heuristic Coding System injects domain-matched encoded heuristics into the reasoning context. These are not generic principles — they are governed claims that have passed admission criteria and been tagged for activation.

Heuristics enter the system through three promotion paths:
- Operator insight → admission review → heuristic record
- Thought leader nugget → publication gate → global heuristic
- Pattern synthesis → confidence scoring → weighted activation

**Spec:** `HEURISTIC_CODING_SYSTEM.md`

---

### Judgment Call — Premium Model Reasoning
With the full context package assembled — terrain classification, EKE knowledge, Polymorphia framing, heuristic injections, active reflexes — the judgment call fires. This is the only point in the loop where the LLM does substantive reasoning work.

**Model tier:** Premium (Opus-class) — mandatory  
**Output:** Structured decision artifact per scenario output template

---

### Prime Directive — Governance Gate
The Prime Directive evaluation fires after the judgment call and before any output is delivered to the operator. It is a structural gate, not a reasoning step.

All three lenses must be evaluated:
1. **Assets vs. Liabilities** — does this action improve or degrade the balance sheet position?
2. **Risk / Reward** — is the risk/reward balance explicit and acceptable?
3. **Supply / Demand** — is there a structural imbalance being leveraged or exposed?

Gate outcomes: PASS → FLAG → ESCALATE → BLOCK

**The sin is not an unfavorable lens. The sin is an unevaluated one.**

**Model tier:** Premium (Opus-class) — mandatory  
**Spec:** `PRIME_DIRECTIVE_RUNTIME_ENFORCEMENT.md`

---

### Persistent Memory — Admission Gate
After a governed output is delivered, the memory admission gate evaluates whether any element of this interaction qualifies for persistent storage. Memory is not a transcript — it is a governed claim store.

Every candidate memory unit must satisfy:
- **Materiality** — does it change what the operator would rationally do?
- **Durability** — will it remain relevant beyond this session?
- **Provenance** — is the source known and credible?
- **Decision Relevance** — could it activate in a future governed decision?

**Spec:** `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md`

---

### Recursive Analysis — Feedback Loop
Recursive Analysis feeds outcomes back into the loop. When decision results become known, the system examines whether assumptions held, whether risks materialized, and whether the output matched expectations.

This stage:
- Strengthens or revises heuristics based on outcome evidence
- Updates confidence scores on admitted memory units
- Surfaces patterns across multiple decision cycles
- Can trigger new Proactive Solutions Architecture signals

**Spec:** `RECURSIVE_ANALYSIS_MODEL.md`

---

### Proactive Solutions Architecture — Ambient Detection
The final layer enables Execalc to surface opportunities and risks without being asked. Pattern detection runs across stored memory, heuristics, and scenario history to identify signals worth surfacing.

Signal levels:
- **Silent** — observed, not surfaced (background context update)
- **Passive** — surfaced in digest or rail (informational)
- **Active escalation** — interrupts operator only when strategic weight justifies it

**Spec:** `PROACTIVE_SOLUTIONS_ARCHITECTURE.md`

---

## What the Loop Produces

A single pass through the Cognitive Loop produces:

| Output | Where it goes |
|---|---|
| Decision artifact | Delivered to operator (if PASS or FLAG) |
| Prime Directive evaluation record | Audit trail |
| Activated knowledge log | Run receipt |
| Memory admission decisions | Persistent memory store |
| Recursive analysis inputs | Heuristic update queue |
| Proactive signal candidates | PSA monitoring layer |

---

## Relationship to the Strategic Mesh

The Cognitive Engine is one layer of the Strategic Mesh:

```
Security Enforcement Layer     ← tenant isolation, auth, deny-by-default
Operational Control Layer      ← Support Stack, fusebox, rate limiting
Cognitive Engine               ← Core 7 Frameworks (this document)
```

The Cognitive Engine governs how reasoning occurs. The layers above it enforce who can invoke it and what the runtime constraints are. The Cognitive Engine does not override security or operational controls — it operates within them.

---

## Design Principles

**Governance before intelligence.** The Prime Directive gate fires after reasoning but before delivery. Reasoning does not determine whether output is delivered — governance does.

**Preparation, not blank-page reasoning.** By the time the LLM judgment call fires, the situation is classified, the knowledge is loaded, the actor map is built, and the heuristics are active. The model reasons within a prepared context.

**Accumulating intelligence.** Every pass through the loop is an opportunity to strengthen the system. Memory admission and recursive analysis ensure the loop compounds over time.

**The null pathway remains fully capable.** When no activation signals are detected, the Cognitive Loop does not fire. The operator has access to a fully capable general-purpose assistant. Governance is invisible until the situation calls for it.

---

## Relationship to Existing Specs

| Document | Relationship |
|---|---|
| `REFLEX_AND_ACTIVATION_SYSTEM.md` | Stages 0–4: the dispatcher layer before judgment |
| `PRIME_DIRECTIVE_RUNTIME_ENFORCEMENT.md` | Framework 1 runtime spec |
| `POLYMORPHIA_RUNTIME_SPEC.md` | Framework 2 runtime spec |
| `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md` | Framework 3 doctrine |
| `EXECUTIVE_KNOWLEDGE_ENGINE_STRATA.md` | Framework 4 knowledge architecture |
| `HEURISTIC_CODING_SYSTEM.md` | Framework 5 runtime spec |
| `PROACTIVE_SOLUTIONS_ARCHITECTURE.md` | Framework 6 runtime spec |
| `RECURSIVE_ANALYSIS_MODEL.md` | Framework 7 runtime spec |
| `EXECALC_STRATEGIC_OPERATING_SYSTEM_MODEL.md` | The OS model this engine sits inside |

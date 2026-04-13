# EKE_HEURISTIC_OBJECT_CLASSIFICATION_MODEL.md

## Status
Draft v0.1

## Owner
Executive Knowledge Engine (EKE)

## Purpose
This document defines the canonical object classification model for EKE heuristic corpus entries.

It exists because the seed heuristic dataset (230+ entries across Historical Thought Leaders, Contemporary Thought Leaders, Perry Marshall, and Jay Abraham) contains entries that are ontologically distinct but were loaded into a single flat schema. Before any of these entries can be activated at runtime, they must be reclassified under this model.

The problem this solves: if everything is called a "heuristic," the runtime cannot know whether an entry should activate a judgment overlay, trigger a reflex, supply a communication posture, or define a principle. That ambiguity is fatal to governed activation.

---

## The Five Object Classes

Each entry in the EKE corpus belongs to exactly one primary object class. An entry may carry secondary tags but must have a single governing class.

### 1. Heuristic
A decision rule derived from experience that produces reliable output under conditions of uncertainty.

A heuristic is:
- actionable — it directs behavior, not just awareness
- bounded — it applies within a defined context
- fallible — it is not an axiom; it can be wrong in edge cases
- fast-activating — it reduces deliberation time

Example: "When the buyer goes silent after an anchor, wait. The first one to speak loses leverage." (Voss)

Runtime role: activates during decision synthesis; supplies a judgment shortcut the operator has pre-endorsed.

---

### 2. Principle
A foundational claim about how a system, person, or domain behaves that holds across many contexts.

A principle is:
- broader than a heuristic — it does not specify action
- slower to activate — it governs framing, not a specific move
- more durable — it survives context changes

Example: "Begin with the end in mind." (Covey)

Runtime role: activates during scenario framing; shapes how the problem is structured before specific heuristics apply.

---

### 3. Mental Model
A structured representation of how a system works that can be used to reason about it.

A mental model is:
- descriptive — it explains how something works
- predictive — it generates expectations about outcomes
- transferable — it applies across domains

Example: "First principles thinking: decompose to irreducible facts, then reason up." (Musk/Aristotle)

Runtime role: activates during analysis; supplies the reasoning scaffold the operator uses to think through the problem.

---

### 4. Reflex
A pre-loaded response pattern that activates automatically when a specific signal or scenario class is detected.

A reflex is:
- pre-encoded — it fires without deliberation
- signal-triggered — activation depends on pattern recognition
- bounded in authority — it may recommend but not govern final output

Example: "When you detect a force multiplier opportunity, immediately assess: Is this controllable? Is the timing right? What is the asymmetric upside?" (synthesized from Boyd + Musk)

Runtime role: activates during signal detection; triggers a specific analytical procedure or question set.

---

### 5. Communication Stance
A posture or register the system adopts when delivering output in a particular context.

A communication stance is:
- tone-defining — it governs how something is said, not what
- context-sensitive — it applies to output format, not analytical logic
- not a judgment asset — it should not influence the substance of analysis

Example: "In high-stakes negotiations, be explicitly collaborative in posture, not neutral." (Voss)

Runtime role: shapes output delivery in synthesis; does not influence analytical judgment.

---

## Why This Classification Matters

If an entry is classified as a Heuristic when it is actually a Communication Stance, it may be activated during judgment synthesis when it should only influence delivery. That is a governance error.

If an entry is classified as a Principle when it is actually a Mental Model, the runtime cannot correctly manage conflicts — a clashing principle suppresses reasoning while a clashing mental model triggers a tension flag.

The five classes carry different:
- activation triggers
- precedence rules
- conflict handling logic
- audit requirements
- link structures (to Carats, Thinkers, Scenarios)

---

## Mapping to EKE Strata

| Object Class | Primary Stratum | Notes |
|---|---|---|
| Heuristic | Monolith / Thought Leadership Nuggets | May be encoded as Carat overlay if scenario-specific |
| Principle | Monolith | Governance-critical; slow to change |
| Mental Model | Monolith / Cartridges | May be packaged into scenario cartridges |
| Reflex | Runtime Cartridges | Requires Activation Pathway spec |
| Communication Stance | Runtime Cartridges | Output layer only; must not enter judgment chain |

---

## Mapping to Carat Eligibility

Not every heuristic becomes a Carat. A Carat is a governed strategic overlay with a specific activation pathway.

A corpus entry is Carat-eligible if:
- it operates at the strategic overlay level (not atomic insight)
- it has clearly defined activation criteria
- it has clearly defined exclusions
- it can be governed under the Carat Registry Standard (see `CARAT_REGISTRY_STANDARD.md`)

Entries that are single atomic insights (one principle, one heuristic) are Thought Leadership Nuggets, not Carats.
Entries that aggregate multiple heuristics under a strategic posture are Carat candidates.

---

## Seed Dataset Classification Status

The seed heuristic dataset (v0.1, pending commit as `EKE_MONOLITH_SEED_CORPUS_DATASET.md`) contains:

| Source Set | Entry Range | Estimated Primary Class | Ontological Risk |
|---|---|---|---|
| Historical Thought Leaders (HTL) | HTL-0001 to HTL-0145 | Mixed: Heuristic, Principle, Mental Model | High — multi-class entries common |
| Contemporary Thought Leaders (CTL) | CTL-0001 to CTL-0041 | Mixed: Heuristic, Mental Model, Communication Stance | Medium |
| Perry Marshall Carat Set (PM) | PM-0001 to PM-0038 | Mixed: Heuristic, Reflex, Carat candidate | High — labeled "Carats" but not all qualify |
| Jay Abraham Executive Module (JA) | JA-0001 to JA-0006 | Heuristic, Principle | Low |

**Current classification status: unresolved.** No entry in the seed dataset has been formally classified under this model. Runtime activation of unclassified entries is prohibited.

---

## Reclassification Protocol

Before any seed dataset entry may be activated at runtime, it must be:

1. Assigned a primary object class from the five defined above
2. Reviewed for Carat eligibility (if Heuristic or Reflex)
3. Assigned a governance status (draft / candidate / approved)
4. Linked to its source thinker as provenance
5. Tagged with eligible scenarios

Reclassification is batch-processable. Priority order: Reflexes first (highest activation risk), then Heuristics, then Principles, then Mental Models, then Communication Stances.

---

## Required Follow-On Specs

1. `EKE_THINKER_REGISTRY.md` — canonical list of recognized thought leaders with governance status
2. `EKE_ACTIVATION_PATHWAY_SPEC.md` — how object classes activate in the runtime cascade
3. `EKE_CONFLICT_RESOLUTION_RULES.md` — what happens when two active heuristics conflict
4. `EKE_MONOLITH_SEED_CORPUS_DATASET.md` — the actual 230+ entry dataset, pending reclassification notation

---

## Current Limitation

This model defines the five object classes and the reclassification protocol. It does not yet specify:
- serialization format for classified entries
- weighting model across object classes
- runtime precedence when multiple classes activate simultaneously
- test suite for classification consistency

Accordingly, this is a draft governance spec, not a complete runtime spec.

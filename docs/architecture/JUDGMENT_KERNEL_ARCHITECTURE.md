# Judgment Kernel Architecture

## Purpose

This document defines the Judgment Kernel as the deterministic orchestration core of Execalc.

The Judgment Kernel is the runtime authority that governs how reasoning proceeds once a situation has been framed.

The LLM produces interpretation and language.
The Judgment Kernel controls the ordered decision process.

This document exists to clarify:
- what the Judgment Kernel is
- what it is responsible for
- how it relates to reflexes, diagnostics, cartridges, nuggets, and governance
- how it produces structured executive outputs
- why its order-of-operations must remain stable and auditable

---

## Core Definition

The Judgment Kernel is the deterministic orchestration layer that governs how Execalc reasons at decision time.

It is not a separate intelligence source.
It is the system layer that determines how governed intelligence is assembled, checked, and converted into executive output.

The Kernel does not replace:
- the Prime Directive
- the Monolith
- cartridges
- nuggets
- diagnostics
- reflexes
- tenant governance

Instead, it coordinates them in the correct order.

---

## Why the Judgment Kernel Exists

Without a Judgment Kernel, Execalc risks becoming one or more of the following:

- a prompt-driven answer system
- a loose collection of heuristics
- an ungoverned retrieval stack
- a chat wrapper with inconsistent reasoning
- a system whose outputs depend too heavily on language-model improvisation

The Kernel exists to prevent that drift.

It provides:
- deterministic order-of-operations
- stable runtime discipline
- enforceable governance sequencing
- model independence at the orchestration layer
- auditability of decision formation

In practical terms, the Kernel is what makes Execalc a governed reasoning system rather than a probabilistic assistant.

---

## Kernel Contract

Given a minimum input tuple such as:

- tenant_id
- operator_id or user_id
- scenario input

the Kernel must be able to:

- normalize the input into a governable runtime form
- classify the situation or load an existing scenario frame
- activate relevant reflexes
- select appropriate strategic overlays
- retrieve and assemble relevant knowledge units
- invoke diagnostics or comparison procedures where needed
- apply Prime Directive and governance constraints
- generate a structured executive output
- create a decision journal envelope or equivalent persistence payload when authorized

This contract defines the minimum runtime obligations of the Kernel.

---

## What the Kernel Governs

The Kernel governs reasoning order, not all intelligence content.

It is responsible for:

### 1. Reasoning sequence
The order in which major runtime steps occur.

### 2. Activation discipline
Which instruments may activate, and when.

### 3. Governance sequencing
Ensuring governance is not applied too late or skipped.

### 4. Procedural integration
Coordinating reflexes, diagnostics, cartridges, nuggets, and decision artifacts into one coherent run.

### 5. Output discipline
Ensuring the system produces structured executive value, not merely commentary.

### 6. Audit readiness
Ensuring key reasoning events can be recorded and reviewed.

---

## What the Kernel Does Not Do

The Judgment Kernel does not itself function as:

- the source of all knowledge
- the only governance mechanism
- the user interface
- the persistence layer
- a substitute for diagnostic procedures
- a substitute for cartridge design
- a substitute for the LLM's natural language generation

The Kernel orchestrates.
It does not collapse the rest of the architecture into itself.

---

## Canonical Position in the Runtime Model

The repo runtime model already establishes the following layered relationship:

1. Language Layer (LLM)  
2. Judgment Layer (Kernel)  
3. Reflex Layer  
4. Overlay Layer (Carats / cartridges)  
5. Knowledge Layer (Nuggets)  
6. Governance Layer (Prime Directive and constraints)  
7. Persistence Layer (Decision Journal)

This document preserves that central idea while clarifying the operational role of the Kernel.

The Kernel sits at the center of runtime orchestration.
It is not “everything,” but it is what gives the overall flow its order and enforceability.

---

## Deterministic Order of Operations

The Judgment Kernel should preserve a canonical order-of-operations.

A typical kernel sequence is:

1. Ingress normalization  
2. Scenario detection, loading, or routing  
3. Context attachment  
4. Reflex scan and activation  
5. Cartridge or overlay selection  
6. Nugget and knowledge retrieval  
7. Diagnostic or comparison procedure invocation where appropriate  
8. Prime Directive evaluation and governing constraints  
9. Structured executive output generation  
10. Decision journal envelope creation or equivalent persistence handoff when authorized

This sequence may evolve in implementation detail, but its governing logic must remain stable.

---

## Step-by-Step Interpretation

### 1. Ingress normalization
Raw operator input, signal input, or routed structured input is converted into a usable runtime form.

### 2. Scenario detection, loading, or routing
The Kernel determines what kind of situation is present, or attaches the run to an existing Scenario object.

### 3. Context attachment
Relevant operator, tenant, historical, and situational context is made available.

### 4. Reflex scan and activation
Automatic pattern detectors evaluate whether any reflexes should fire.

### 5. Cartridge or overlay selection
The runtime selects relevant strategic overlays that should shape posture and reasoning.

### 6. Nugget and knowledge retrieval
Relevant atomic logic units and supporting governed knowledge are assembled.

### 7. Diagnostic or comparison procedure invocation
If the situation requires more structured procedure, the Kernel coordinates diagnostic or comparative logic.

### 8. Prime Directive evaluation and governing constraints
Reasoning is filtered through value, risk/reward, supply/demand, and other active governance constraints.

### 9. Structured executive output generation
The run produces a recommendation, analysis, or decision artifact precursor in a governed format.

### 10. Decision journal envelope creation
Where appropriate, the run is packaged for persistence, audit, or later comparison.

---

## Relationship to Runtime Objects

The Kernel should operate on explicit runtime objects rather than loose prompt state.

Typical object relationships include:

- Signal
- Scenario
- KnowledgeAsset
- Cartridge
- Nugget
- Diagnostic
- Reflex
- DecisionArtifact
- AuthorizationObject

A typical object flow may look like:

Signal  
→ Scenario  
→ Reflex / Cartridge / Nugget / Diagnostic activation  
→ DecisionArtifact  
→ AuthorizationObject when execution is permitted

The Kernel is what orchestrates that flow into a disciplined runtime path.

---

## Relationship to Reflexes

Reflexes are automatic pattern detectors and triggers.

The Kernel does not replace reflexes.
It provides the ordered environment in which reflexes can fire safely and meaningfully.

The Kernel is responsible for:
- running reflex scans at the correct point
- preventing reflex chaos or uncontrolled ordering
- ensuring reflex outputs feed into governed reasoning rather than bypass it

Reflexes provide instinctive activation.
The Kernel provides orchestration discipline.

---

## Relationship to Cartridges and Overlays

Cartridges shape strategic posture inside a scenario or domain.

The Kernel is responsible for:
- determining when cartridge selection should occur
- ensuring client or tenant overlays receive correct precedence
- preventing arbitrary overlay stacking
- keeping cartridge influence subordinate to governance

Cartridges shape how the system thinks in context.
The Kernel decides when and how they enter the run.

---

## Relationship to Nuggets and Knowledge

Nuggets are atomic strategic insights.
Knowledge strata provide different levels of authority, scope, and trust.

The Kernel is responsible for:
- coordinating knowledge activation order
- distinguishing between permanent governed knowledge and temporary supplementation
- making sure retrieval supports the reasoning path rather than replacing it
- preventing lower-trust sources from dominating higher-trust governed logic

Knowledge provides substance.
The Kernel provides disciplined assembly.

---

## Relationship to Diagnostics

Diagnostics are callable analytical procedures.

The Kernel is responsible for:
- deciding where diagnostics fit in the reasoning sequence
- coordinating explicit or authorized invocation
- ensuring diagnostics operate on structured context
- connecting diagnostic outputs to executive reporting and decision artifacts

Diagnostics provide procedural rigor.
The Kernel integrates that rigor into the broader reasoning run.

---

## Relationship to Governance

The Kernel is governance-dependent and governance-enforcing.

It must not allow:
- reflex activation before basic framing
- overlay usage without precedence logic
- knowledge activation without scope discipline
- output generation before Prime Directive filtering
- persistence without proper envelope discipline

This is why the Kernel is inseparable from governance, even though it is not itself the whole governance system.

In practical terms, the Kernel is the orchestration mechanism that ensures governance happens in the right order.

---

## Relationship to the LLM

The LLM is an interpretation and expression engine.

The Kernel must remain stable across LLM changes.

The model may assist with:
- interpretation
- framing assistance
- summarization
- explanation
- narrative presentation

The model must not determine whether the ordered governance steps execute.

That decision belongs to the Kernel.

This protects Execalc from model drift and prompt fragility.

---

## Model Independence Doctrine

Kernel logic must remain stable across LLM changes.

This means:

- no prompt may replace kernel order-of-operations
- no model should decide whether governance steps occur
- the system should preserve orchestrated reasoning discipline across model upgrades
- the explanation engine may vary while the reasoning path remains governed

This doctrine is essential for long-term system reliability.

---

## Expected Output Shape

At minimum, the Kernel should be able to produce or support a structured executive output containing:

- executive_summary
- recommendation
- rationale
- key_risks
- alternatives
- confidence
- sensitivity
- next_actions

In many cases, this output should then be formalized into a DecisionArtifact or equivalent structured record.

The output should reflect executive usefulness, not just fluent prose.

---

## Decision Journal Envelope

The Kernel should be able to create a persistence-ready envelope when the run warrants durable storage.

Typical contents may include:

- linked scenario reference
- operator and tenant scope
- detected scenario type
- reflexes fired
- cartridges selected
- nuggets or knowledge sources used
- diagnostics invoked
- assumptions
- confidence
- sensitivities
- output summary
- persistence eligibility or status

This envelope is what allows later comparison, audit, and strategic memory.

---

## Auditability Requirements

The Kernel must be able to record enough information to make reasoning auditable.

At minimum, the system should be able to record:

- which scenario was detected
- which reflexes fired and why
- which cartridges or overlays were applied
- which nuggets or knowledge sources were selected
- whether diagnostics were invoked
- what assumptions were used
- what constraints mattered
- confidence level
- key sensitivities
- whether persistence occurred

Auditability is not optional.
It is one of the defining reasons the Kernel exists.

---

## Architectural Non-Negotiables

### 1. Ordered execution must remain real
The Kernel cannot be reduced to a storytelling metaphor.

### 2. Governance cannot be bypassed by prompts
The system must not allow rhetorical fluency to skip structural checks.

### 3. Runtime reasoning must remain object-aware
The Kernel should operate on explicit objects and governed state.

### 4. Tenant isolation is absolute by default
Kernel orchestration must preserve scope and boundary discipline.

### 5. Output must remain executive-grade
The Kernel exists to produce decision value, not just language.

---

## Failure Modes Prevented

A well-defined Kernel architecture helps prevent:

- prompt-driven reasoning drift
- skipped governance steps
- unstable execution order
- hidden model dependence
- reflex or overlay chaos
- unstructured executive outputs
- weak audit trails
- persistence without sufficient envelope discipline

---

## Near-Term Implementation Guidance

Phase 1  
Expand and pin the Kernel architecture in documentation.

Phase 2  
Align the Kernel definition with runtime object scaffolding and activation logic.

Phase 3  
Represent Kernel sequencing explicitly in service/module boundaries.

Phase 4  
Connect Kernel output to decision artifacts, comparison flows, and persistence mechanisms.

The exact code structure may evolve, but the orchestration contract should remain stable.

---

## Summary

The Judgment Kernel is the deterministic orchestration core of Execalc.

It governs how runtime reasoning proceeds once a situation enters the system.

Its role is to coordinate:
- framing
- reflex activation
- cartridge selection
- knowledge assembly
- diagnostic procedure integration
- Prime Directive evaluation
- structured executive output
- decision journal packaging

The LLM supplies interpretation and language.
The Kernel supplies order, discipline, and auditability.

That distinction is one of the main reasons Execalc can function as a governed strategic operating system rather than a probabilistic chatbot.

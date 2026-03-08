# Execalc Runtime Model

## Purpose

This document defines the runtime model of Execalc and how its major layers, objects, and orchestration mechanisms interact at decision time.

The runtime model is the bridge between architectural doctrine and executable system behavior.

It explains:
- the major runtime layers
- the role of the Judgment Kernel
- how runtime objects move through the system
- how governance, knowledge, diagnostics, and outputs fit together
- what must remain non-negotiable as implementation advances

---

## Core Definition

Execalc's runtime model is a governed multi-layer execution system.

It is not a single prompt flow.
It is not a generic agent loop.
It is not a chatbot with add-ons.

It is a structured runtime environment in which:
- situations are framed
- governance is applied
- knowledge is activated
- analytical procedures are executed
- structured outputs are produced
- persistence and authorization are handled under rule

The runtime model defines how those things happen together.

---

## Why the Runtime Model Matters

Without an explicit runtime model, the system risks becoming:

- a loose collection of prompts
- an unstable orchestration chain
- a set of disconnected features
- a retrieval-heavy assistant with weak governance
- a product whose outputs are hard to audit or trust

A real runtime model creates:
- architectural clarity
- execution discipline
- stable interfaces between components
- clearer implementation pathways
- auditability
- tenant-safe orchestration

This is one of the main things that makes Execalc look like a serious platform rather than a clever prompt stack.

---

## Canonical Runtime Layers

The runtime model should be understood through seven major layers.

### 1. Language Layer
The LLM handles interpretation and expression.

Its job is to help with:
- natural-language input handling
- semantic interpretation
- summarization
- explanation
- final language generation

The LLM is subordinate to governed orchestration.

### 2. Judgment Layer
The Judgment Kernel acts as the deterministic orchestration core.

Its job is to:
- preserve runtime order-of-operations
- coordinate activation of runtime instruments
- ensure governance happens in the right sequence
- produce structured executive outputs

### 3. Reflex Layer
The Reflex Layer contains encoded runtime instincts that detect patterns and trigger logic.

Examples:
- Blind/Deaf Reflex
- Compromise Awareness Reflex
- Free Agent Reflex
- governance checkpoint reflexes

### 4. Overlay Layer
The Overlay Layer contains cartridges and other situational strategic overlays.

Its job is to shape posture and reasoning in context.

Examples:
- negotiation cartridge
- due diligence cartridge
- SWOT overlays
- client policy cartridges

### 5. Knowledge Layer
The Knowledge Layer contains the governed intelligence sources used during reasoning.

Examples:
- Monolith
- thought leadership nuggets
- Execalc cartridges
- client cartridges
- proprietary data sources
- client data sources
- internet search
- bounded free agent supplementation

### 6. Governance Layer
The Governance Layer constrains reasoning and execution.

It includes:
- Prime Directive
- Strategic Mesh controls
- tenant boundaries
- authorization checks
- anti-bypass discipline
- runtime safety controls

### 7. Persistence Layer
The Persistence Layer captures durable outputs and runtime history where appropriate.

Examples:
- decision journal envelopes
- decision artifacts
- audit events
- comparison-ready historical records

These layers together define the runtime environment of Execalc.

---

## Relationship to the Reasoning Stack

The runtime model aligns directly with the seven-layer reasoning stack already defined in the repo.

Reasoning stack view:
1. Interface Layer
2. Context and Memory Layer
3. Detection and Framing Layer
4. Governance Layer
5. Knowledge Layer
6. Analytical Procedure Layer
7. Decision and Action Layer

Runtime model view:
1. Language Layer
2. Judgment Layer
3. Reflex Layer
4. Overlay Layer
5. Knowledge Layer
6. Governance Layer
7. Persistence Layer

These are not contradictory models.
They are two views of the same system.

- The reasoning stack explains how cognition unfolds conceptually.
- The runtime model explains which execution layers are active at runtime.
- The Judgment Kernel and runtime scaffolding supply the orchestration bridge between them.

---

## The Role of the Judgment Kernel

The Judgment Kernel is the orchestration center of the runtime model.

It is the layer that prevents Execalc from degrading into a prompt-driven answer engine.

The Kernel is responsible for:
- deterministic sequencing
- activation discipline
- governance ordering
- procedural integration
- executive output discipline
- audit readiness

The model may change.
The Kernel contract should not drift casually.

The LLM speaks.
The Kernel governs.

---

## The Role of Runtime Scaffolding

The runtime scaffolding defines the conceptual components that allow the runtime model to operate in practice.

These components include:
- Scenario Intake Processor
- Knowledge Activation Orchestrator
- Cartridge Selector
- Nugget Retrieval Engine
- Diagnostic Registry
- Diagnostic Executor
- Reflex Registry
- Decision Artifact Builder
- Authorization Gate
- Runtime Audit Trail

The runtime model defines the layers.
The scaffolding defines the machinery that moves through those layers.

---

## Core Runtime Object Families

The runtime model operates on explicit objects, not loose conversational state.

The core runtime object families currently recognized in the repo are:

1. Scenario
2. Signal
3. KnowledgeAsset
4. Cartridge
5. Nugget
6. Diagnostic
7. Reflex
8. DecisionArtifact
9. AuthorizationObject

These objects are what make the runtime model implementation-ready.

They allow the system to:
- route situations
- select governed instruments
- create durable outputs
- enforce scope and permissions
- support persistence and audit

---

## Canonical Runtime Flow

A typical runtime flow should look like this:

Signal or operator input  
→ Scenario framing or routing  
→ Context attachment  
→ Reflex scan  
→ Cartridge selection  
→ Knowledge activation  
→ Diagnostic or comparison procedure invocation where needed  
→ Prime Directive and governance evaluation  
→ Structured executive output  
→ DecisionArtifact creation  
→ AuthorizationObject creation when execution is permitted  
→ Journal or audit persistence where appropriate

This is the working runtime path that turns input into governed value.

---

## Runtime Layer Interpretation

### Language Layer
Handles semantic interpretation and final language production.

### Judgment Layer
Coordinates the runtime sequence and ensures the system follows governed order-of-operations.

### Reflex Layer
Detects patterns that may require automatic activation or warning logic.

### Overlay Layer
Injects situational or domain-specific strategic posture into the reasoning run.

### Knowledge Layer
Supplies the relevant governed substance for reasoning.

### Governance Layer
Constrains what the system may conclude, recommend, surface, or execute.

### Persistence Layer
Stores durable artifacts and runtime history when policy and usefulness warrant it.

---

## Governance in the Runtime Model

Governance is not an outer shell added after reasoning.
It is a live runtime layer.

This means the runtime model must ensure:

- governance precedes unrestricted execution
- knowledge activation respects scope and precedence
- diagnostics do not bypass permissions
- reflexes do not run wild
- outputs do not surface without proper checks
- persistence does not happen casually
- tenant isolation remains absolute by default

A runtime model without active governance is not Execalc.

---

## Knowledge Activation in the Runtime Model

Knowledge activation should follow disciplined escalation.

A practical precedence order already established in the repo is:

1. Security and tenant boundaries
2. Client cartridges / client policy
3. Core governance and Prime Directive
4. Execalc cartridges
5. Monolith
6. Thought leadership nuggets
7. Data sources
8. Internet search
9. Free agent contributors as temporary supplements

This matters because not all knowledge sources are equal.
The runtime model must protect authority, trust weighting, and scope.

---

## Diagnostics and Procedures in the Runtime Model

The runtime model must distinguish between knowledge and procedure.

Knowledge provides substance.
Procedure provides method.

This is why diagnostics, comparison procedures, and reflexes must remain distinct runtime elements.

The runtime model should support:
- explicit diagnostic invocation
- scenario-aware diagnostic suggestion
- governed reflex activation
- comparison procedures for tradeoff evaluation
- structured transition from analysis to decision artifact

This procedural layer is one of the reasons Execalc can produce repeatable executive outputs instead of merely plausible text.

---

## Output Model

The runtime model should culminate in structured executive output.

At minimum, runtime should be able to produce:
- executive_summary
- recommendation
- rationale
- key_risks
- alternatives
- confidence
- sensitivity
- next_actions

In many cases, this should become a `DecisionArtifact` suitable for:
- review
- comparison
- journaling
- future recall
- governed action support

The runtime model is therefore output-disciplined, not merely language-disciplined.

---

## Persistence Model

Persistence is a runtime layer, not just a storage afterthought.

The runtime model should support:
- optional decision journal envelope creation
- audit event recording
- durable decision artifact storage where appropriate
- comparison-ready historical records
- tenant-safe retrieval of prior decisions

Not every runtime event must persist.
But important governed reasoning should be persistable in a structured way.

---

## Authorization and Execution

The runtime model must also recognize that reasoning and execution are not the same thing.

A strong runtime model therefore includes an authorization boundary between:
- recommendation
- decision artifact
- action authorization
- downstream execution

This is why `AuthorizationObject` matters.

It creates a governed bridge between reasoning and action rather than allowing uncontrolled automation.

---

## Architectural Non-Negotiables

### 1. No prompt may replace the runtime model
The ordered runtime path must remain real.

### 2. The Kernel must remain authoritative
Deterministic orchestration cannot be optional.

### 3. Governance must be enforceable and auditable
The model is not valid unless it can be checked and traced.

### 4. Tenant isolation is absolute by default
All runtime behavior must honor scope boundaries.

### 5. Runtime objects must remain explicit
Important concepts should not disappear into hidden prompt state.

### 6. Structured outputs matter
The system should produce executive value, not just fluent prose.

---

## Failure Modes Prevented

A strong runtime model helps prevent:

- prompt-chain drift
- unstructured reasoning behavior
- skipped governance checks
- overreliance on model improvisation
- diagnostic and reflex confusion
- weak persistence discipline
- poor auditability
- cross-tenant leakage
- fragile execution paths

---

## Near-Term Implementation Guidance

Phase 1  
Pin the runtime model as the synthesis layer above the Kernel, runtime objects, and scaffolding docs.

Phase 2  
Align service/module boundaries to the runtime model.

Phase 3  
Ensure major runtime objects have clean interfaces and persistence expectations.

Phase 4  
Connect runtime outputs more tightly to comparison flows, journaling, and authorization-controlled execution.

This document should remain stable enough to guide implementation even as individual modules evolve.

---

## Summary

The Execalc runtime model defines how the system actually operates at decision time.

It is a governed multi-layer runtime environment composed of:

- language handling
- deterministic judgment orchestration
- reflex activation
- strategic overlays
- governed knowledge activation
- active governance enforcement
- structured persistence

It operates on explicit runtime objects, produces structured executive outputs, and preserves authorization and audit discipline.

That is the runtime spine of a governed strategic operating system.

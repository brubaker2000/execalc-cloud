# Support Stack Implementation Map

## Purpose

This document translates the Support Stack from doctrine into implementation targets.

The Support Stack is not a separate reasoning engine.
It is the Operational Control Layer of the Strategic Mesh.

Its role is to ensure that Execalc behaves safely, consistently, and auditable at runtime.

This document maps each major Support Stack mechanism to:

- its function
- its runtime home
- its current implementation status
- its next build step

---

## 1. Reflex Gating System

### Function
Controls which reflexes may activate, in what order, and under what conditions.

### Runtime Home
- Reflex Layer
- Judgment Kernel
- Governance Layer

### Current Status
- Doctrinally defined
- Runtime concept present
- Not yet visibly implemented as a formal registry/gating engine

### Next Build Step
Create:
- Reflex
- ReflexRegistry
- ReflexGateDecision

Then wire one or two reflexes through deterministic activation logic.

---

## 2. PRP-01

### Function
Procedural routing discipline for selecting and sequencing runtime procedures.

### Runtime Home
- Judgment Kernel
- Procedure orchestration spine
- Governance Layer

### Current Status
- Directionally present through service-layer orchestration and decision loop logic
- Not yet formalized as a named procedural routing module

### Next Build Step
Create:
- ProcedureStep
- ProcedurePlan
- ProcedureExecutor

Then require the decision loop to generate an ordered execution plan before running procedures.

---

## 3. BDR-01

### Function
Boundary defense rule that blocks unauthorized scope crossing, policy bypass, tenant leakage, or prohibited runtime movement.

### Runtime Home
- Governance Layer
- Security Enforcement Layer
- Authorization checkpoints

### Current Status
- Spirit partially present through tenant checks, route gating, and scoped persistence
- Not yet formalized as an explicit runtime enforcement object

### Next Build Step
Create:
- BoundaryCheck
- BoundaryViolation
- BoundaryDecision

Then require sensitive retrieval, activation, and execution paths to pass a boundary check.

---

## 4. Heuristic Hygiene Layer

### Function
Ensures heuristics remain traceable, governable, non-corrupt, and non-contradictory over time.

### Runtime Home
- Knowledge Layer
- Governance Layer
- Persistence Layer

### Current Status
- Strong doctrinal relevance
- No visible implementation yet for heuristic provenance, contradiction management, or lifecycle handling

### Next Build Step
Create a governed heuristic schema including:
- source
- confidence
- domain
- activation context
- status
- supersedes / conflicts_with

Then add hygiene checks for admission and retrieval.

---

## 5. Memory Integrity Protocols

### Function
Ensures persistent memory is complete, structured, durable, and strategically usable.

### Runtime Home
- Persistence Layer
- Decision Artifact Builder
- Governance Layer

### Current Status
- Partially implemented through execution records and structured outputs
- Not yet fully upgraded into generalized governed artifact/event persistence

### Next Build Step
Expand persistence contracts to store:
- event_type
- schema_version
- artifact_class
- completeness validation results
- optional reason codes

This is one of the highest-priority Support Stack implementation targets.

---

## 6. Carat Conflict Interlocks

### Function
Prevents incompatible overlays, carats, or strategic instruments from activating simultaneously without governed resolution.

### Runtime Home
- Overlay Layer
- Judgment Kernel
- Governance Layer

### Current Status
- Clearly implied by runtime doctrine
- No visible implementation yet for overlay compatibility or conflict resolution

### Next Build Step
Create:
- OverlayActivationRequest
- OverlayConflictRule
- OverlayResolutionDecision

Then define a compatibility matrix for initial overlay pairings.

---

## 7. Recursive Reintegration Pathways

### Function
Feeds outcome signals and later evidence back into memory, heuristics, scenario framing, and future reasoning.

### Runtime Home
- Persistence Layer
- Knowledge Layer
- Judgment Layer
- Post-decision review pathways

### Current Status
- Doctrinally present through Recursive Analysis and persistence concepts
- Not yet visibly implemented as a post-outcome learning path

### Next Build Step
Create:
- OutcomeSignal
- DecisionArtifact linkage
- assumption delta / future warning update mechanism

Then implement a first path for revisiting prior artifacts after outcome observation.

---

## Summary

The Support Stack is the Operational Control Layer of the Strategic Mesh.

It governs runtime discipline across:

- reflex behavior
- procedural routing
- boundary defense
- heuristic health
- memory reliability
- overlay compatibility
- recursive learning

This document exists to ensure the Support Stack remains implementation-bound, not merely conceptual.


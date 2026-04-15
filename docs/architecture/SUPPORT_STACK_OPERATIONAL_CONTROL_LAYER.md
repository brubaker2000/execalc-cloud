# SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md

## Status
Draft v0.1

## Owner
Runtime / Architecture

## Purpose
This document specifies the Operational Control Layer — Layer 2 of the Strategic Mesh, internally called the Support Stack.

Its purpose is to ensure that what the Cognitive Engine (Core 7) was designed to do is what the system actually does — under real operating conditions, at scale, over time.

---

## The Problem This Layer Solves

A reasoning architecture that operates correctly in a controlled environment can degrade in production. Specifically:

- Reasoning may drift from governing logic over time
- Inputs may — intentionally or inadvertently — bias the system away from the operator's interests
- Outputs may appear logically sound while violating the governing framework at intermediate steps
- The Prime Directive and Core 7 may remain nominally active while being effectively bypassed

None of these failure modes are caught by the Cognitive Engine itself. The Cognitive Engine produces judgment. The Support Stack protects that judgment from being undermined before it reaches the operator.

---

## The Four Named Components

### 1. Recursive Audit Triggers

**Function:** Continuously verify that outputs are consistent with the governance frameworks that produced them.

**How it works:**
- At each reasoning step, the output is evaluated against the active governance frameworks
- If a reasoning path produces a recommendation that deviates from governing logic, the trigger fires before the output reaches the operator
- Deviation does not automatically block output — it surfaces the deviation explicitly so the operator can evaluate it with full awareness

**What it catches:** Outputs that are locally coherent but globally inconsistent with the Prime Directive or Core 7 framework constraints.

**Audit requirement:** Every trigger event — whether it results in a block, a flag, or a pass — must appear in the session audit trail.

---

### 2. Compromise-Awareness Reflexes

**Function:** Monitor the information environment for attempts — intentional or inadvertent — to introduce inputs that would bias the system's reasoning away from the operator's actual interests.

**How it works:**
- Continuously scan inputs for patterns that suggest manipulation: leading framing, false premises, authority appeals, contradictions with established operator context, inputs that selectively suppress relevant information
- Flag suspected compromise attempts before they enter the reasoning pipeline
- Distinguish between legitimate contextual updates (new information from the operator) and adversarial or inadvertent bias injection

**Threat model — intentional:**
- External parties attempting to use Execalc as a tool against the operator's interests
- Structured prompt injections designed to override governance logic
- Information designed to shift the system's framing toward a preferred conclusion

**Threat model — inadvertent:**
- Operator inputs that contain unstated assumptions that would distort analysis if accepted uncritically
- Incomplete context that, if processed as complete, would produce systematically biased output
- Internal organizational dynamics that bias the framing of a situation before it reaches Execalc

**Response:**
- Flag suspected compromise with an explicit description of the detected pattern
- Request operator confirmation before proceeding with potentially compromised input
- Log the event in the audit trail regardless of resolution

**Design note:** Compromise-awareness is not paranoia — it is governance. The system must be able to distinguish between what is being told to it and what is actually in the operator's interest. That distinction is the foundational requirement of a trustworthy advisory system.

---

### 3. Runtime Validation Protocols

**Function:** Confirm the logical integrity of the reasoning path at each step — not just at the output stage.

**How it works:**
- Each intermediate reasoning step is validated against the logical constraints established by the active scenario, active Carats, and Prime Directive frame
- Validation is not a re-run of the full reasoning process — it is a structural integrity check: does this step follow from the previous step within the governing constraints?
- A step that fails validation is flagged and does not automatically propagate to the next reasoning step

**What it catches:**
- Logical leaps that appear plausible but violate the governing framework
- Steps where a conclusion is drawn from evidence that does not actually support it
- Reasoning chains where intermediate conclusions contradict each other but the final output obscures the contradiction

**Relationship to Recursive Analysis (Core 7):** Runtime Validation Protocols operate at the step level. Recursive Analysis (Core 7 Framework 7) operates at the output level — re-evaluating the complete output after it is produced. These are complementary, not redundant.

---

### 4. Governance Enforcement Drivers

**Function:** Ensure the Prime Directive and Core 7 frameworks remain active and binding across every session, every tenant, and every operating context.

**How it works:**
- At session initialization, confirm all required governance frameworks are loaded and active
- Throughout the session, verify that no input, integration, or configuration has altered the active governance state without explicit operator authorization
- At session close, confirm that the governance state is preserved for the next session

**What it prevents:**
- Gradual erosion of governance constraints through configuration drift
- Integration inputs (from connected external systems) that would effectively modify governance behavior
- Session-specific exceptions that persist beyond their intended scope

**Enforcement hierarchy:**
1. Compliance cartridges (highest — cannot be overridden by anything in the session)
2. Prime Directive
3. Core 7 frameworks
4. Active Carats and cartridges
5. Operator preferences

Nothing below a given level in this hierarchy may override anything above it without explicit tenant admin authorization.

---

## Current Code State

The existing `src/service/decision_loop/support_stack.py` contains Phase 1 scaffolding:
- `ReflexRegistry` — in-memory, no persistence, no scenario association
- `ReflexGateDecision` — returns allow-all by default
- `BoundaryDecision` — always returns `allowed=True`
- `default_boundary_decision` — placeholder checks only

**Stage 8 replaces this scaffolding with the four components specified above.**

The data models (`Reflex`, `ReflexGateDecision`, `BoundaryDecision`) can be extended. The gate logic must be rebuilt. The compromise-awareness and runtime validation components do not yet exist in any form.

---

## Audit Requirements

Every Support Stack component event must appear in the session audit trail:

| Component | Auditable Events |
|---|---|
| Recursive Audit Triggers | Trigger fired, deviation detected, resolution (blocked / flagged / passed) |
| Compromise-Awareness Reflexes | Suspected compromise detected, pattern description, operator confirmation result |
| Runtime Validation Protocols | Step validation result, failure description if applicable |
| Governance Enforcement Drivers | Session initialization state, mid-session governance state changes, session close state |

---

## Design Principle

The Support Stack is not optional. It is the difference between a system that reasons correctly in a demo and a system that reasons correctly in production, under adversarial conditions, over time.

Governance that cannot protect itself from drift, manipulation, and silent degradation is not governance. It is the appearance of governance.

# Thin Chat Orchestration Layer

Status: Proposed architecture note  
Purpose: Define the missing runtime bridge between freeform executive chat input and the governed Execalc runtime, including Decision Loop, governed evidence invocation, Action Proposal generation, and Execution Boundary Engine v2 routing.

---

## Why this layer exists

The current Stage 8 branch now has:

- a Decision Loop Engine
- an Executive Rail display surface
- Execution Boundary Engine scaffolding
- an Execution Boundary Engine v2 runtime spec
- a synthesis register clarifying the next architectural center of gravity

What is still missing is the thin conversational runtime layer that sits above those systems and turns real chat turns into governed runtime behavior.

This layer is not the Decision Loop itself.  
It is not the Executive Rail itself.  
It is not EBE v2 itself.

It is the traffic-control layer between freeform conversation and governed machine-state transitions.

---

## Core role

The Thin Chat Orchestration Layer is responsible for:

1. accepting a freeform user turn
2. classifying what kind of turn it is
3. deciding whether the turn is:
   - conversational only
   - decision-seeking
   - action-proposing
   - execution-seeking
   - evidence-seeking
4. constructing or updating the scenario object
5. invoking the correct governed subsystem
6. returning:
   - conversational response text
   - machine-readable state payload
   - rail-ready state updates
   - action proposal objects when appropriate
   - EBE v2 outcomes when execution is implicated

---

## Canonical principle

The rail is not the source of truth.

The orchestration runtime is the source of truth.  
The rail is a window into governed runtime state.

---

## Initial turn classes

### 1. Conversational
Examples:
- “What do you think of this idea?”
- “Talk this through with me.”
- “Summarize what we know.”

Behavior:
- no execution path
- may produce structured notes
- may update working context
- does not create an Action Proposal by default

### 2. Decision-seeking
Examples:
- “Which option is better?”
- “Evaluate this under our objective.”
- “What should we do?”

Behavior:
- construct or refine scenario object
- invoke Decision Loop Engine
- return report payload plus conversational rendering
- may produce recommendations without creating execution intent

### 3. Action-proposing
Examples:
- “Draft the next move.”
- “Prepare the outreach.”
- “Generate the action we would take.”

Behavior:
- invoke Decision Loop Engine if needed
- create structured Action Proposal artifact
- do not execute
- mark result as pending EBE v2 review if execution is later requested

### 4. Execution-seeking
Examples:
- “Send it.”
- “Approve this.”
- “Run the next step.”
- “Go ahead.”

Behavior:
- require an existing Action Proposal or create one first
- route through EBE v2
- return one of:
  - ALLOW
  - BLOCK
  - RECOMPUTE
  - ESCALATE
  - CONTAIN
- never bypass execution review

### 5. Evidence-seeking
Examples:
- “What evidence supports this?”
- “Pull the relevant docs.”
- “What internal data are we relying on?”

Behavior:
- invoke governed evidence retrieval
- keep invocation legible to operator
- return evidence summary plus source handles where supported

---

## Minimum orchestration flow

`User Turn -> Turn Classifier -> Scenario Constructor -> Runtime Router -> Decision Loop / Evidence Retrieval / Action Proposal / EBE v2 -> Conversational Response + State Payload + Rail Update`

---

## Scenario constructor role

The orchestration layer should produce or update a normalized scenario object.

Minimum concept:

- scenario_id
- scenario_type
- governing_objective
- user_intent
- prompt
- relevant_constraints
- evidence_scope
- decision_state
- action_state
- created_at
- updated_at

This does not need to be perfect at first.  
It needs to be stable enough for runtime routing.

---

## Action Proposal handoff

When the turn implies action, the orchestration layer should emit a structured Action Proposal object rather than loose prose.

Minimum fields:

- proposal_id
- scenario_id
- decision_id
- action_type
- action_payload
- assumptions
- constraints
- approval_thresholds
- confidence
- created_at

This object is the handoff boundary between decision and execution control.

---

## Relationship to EBE v2

The orchestration layer does not decide whether execution is allowed.

Its role is to:

- detect execution-seeking intent
- ensure an Action Proposal exists
- pass that proposal to EBE v2
- present the resulting outcome clearly

EBE v2 remains the commit-time governor and may return:

- ALLOW
- BLOCK
- RECOMPUTE
- ESCALATE
- CONTAIN

If EBE v2 escalates to human judgment, the orchestration layer must preserve the returned state and ensure the UI/runtime can surface the resulting Authority Event or Human Judgment Ledger Entry path.

---

## Relationship to governed evidence

Connected data and internal sources should not be treated as silently ambient.

The orchestration layer should make evidence invocation selective and legible by:

- identifying what evidence domain is relevant
- invoking only the needed sources
- surfacing what was consulted when appropriate

This keeps the Executive Knowledge Engine governed rather than magical.

---

## Relationship to Organizational Objective Cartridges

Organizational Objective Cartridges may influence weighting and framing, but they do not determine execution authority.

The orchestration layer may pass cartridge-aware context into decision and revalidation paths, but final execution admissibility remains governed by EBE v2 and, where necessary, properly authorized human judgment.

---

## Non-goals for v1

The first version of this layer should NOT attempt to solve all of the following:

- full autonomous agent management
- broad multi-step workflow execution
- giant trigger forests
- universal memory design
- final production-grade natural language intent perfection

The goal of v1 is narrower:

- correctly route real chat turns into governed runtime paths
- preserve machine state
- make EBE v2 reachable from chat
- make the rail reflect real runtime state

---

## First implementation target

The first practical implementation target should be a small service module that:

1. accepts raw user text
2. assigns one of the initial turn classes
3. creates a normalized scenario envelope
4. routes into:
   - Decision Loop
   - Action Proposal generation
   - EBE v2 path
   - evidence retrieval path
5. returns a combined response object for API and UI use

Suggested initial output envelope:

- ok
- turn_class
- scenario
- decision_result
- action_proposal
- execution_boundary_result
- assistant_message
- rail_state

---

## Why this matters

Without this layer, Execalc has strong parts but no governed conversational spine connecting them.

With this layer, Execalc becomes able to accept natural executive turns and route them into structured, auditable, governed runtime behavior.

That makes it the real bridge between chat experience and enterprise-grade judgment.

---

## Current conclusion

The Thin Chat Orchestration Layer is now the next major missing bridge in the Execalc runtime architecture.

It should be treated as the next architecture center of gravity after the initial EBE v2 landing.

# Orchestration Sprint Sequence

Status: Active sequencing note  
Purpose: Translate the newly pinned architecture notes into a disciplined build sequence so the next implementation step is deliberate rather than improvised.

Related notes:

- `docs/product/CHAT_SYNTHESIS_REGISTER_AUDIT8_AUTONOMOUS_AGENTS.md`
- `docs/product/EXECUTION_BOUNDARY_ENGINE_V2_SPEC.md`
- `docs/product/THIN_CHAT_ORCHESTRATION_LAYER.md`

---

## Why this note exists

The branch now contains the major architectural truths needed to guide the next tranche of work:

- the synthesis of overlapping product and build ideation
- the formalized Execution Boundary Engine v2
- the missing thin chat orchestration bridge

The next task is not to build everything those notes imply.  
The next task is to convert them into a clear sequence.

---

## Build principle

Protect the spine.

That means:

- build the minimum orchestration layer the current runtime can actually support
- do not overbuild around unproven assumptions
- preserve insertion points for future features
- route real chat turns into governed paths before adding broader autonomy

---

## Now / Next / Later / Non-goals

## NOW

### 1. Orchestration skeleton
Build a minimal orchestration service module that:

- accepts raw user text
- assigns an initial turn class
- creates a normalized scenario envelope
- routes into one of the currently supported runtime paths
- returns a combined machine-readable response envelope

Target turn classes for v1:

- conversational
- decision-seeking
- action-proposing
- execution-seeking
- evidence-seeking

Success condition:
- chat input can reliably enter governed runtime flow without requiring the rail to invent state on its own

### 2. Scenario envelope normalization
Define the first stable scenario envelope shape used by the orchestration layer.

Minimum concept:

- scenario_id
- scenario_type
- governing_objective
- user_intent
- prompt
- relevant_constraints
- decision_state
- action_state
- created_at
- updated_at

Success condition:
- routing decisions no longer depend on loose prose alone

### 3. Combined response envelope
Define the first stable orchestration output envelope for API/UI consumption.

Minimum concept:

- ok
- turn_class
- scenario
- decision_result
- action_proposal
- execution_boundary_result
- assistant_message
- rail_state

Success condition:
- backend and UI can begin to converge on one runtime object contract

---

## NEXT

### 4. Action Proposal contract hardening
Make the Action Proposal object explicit and stable across Decision Loop, orchestration, and EBE v2.

Minimum concept:

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

Success condition:
- the handoff between decision and execution control is formal rather than implied

### 5. EBE v2 routing integration
Ensure execution-seeking turns flow through the real EBE path and return one of:

- ALLOW
- BLOCK
- RECOMPUTE
- ESCALATE
- CONTAIN

Success condition:
- orchestration becomes the real chat-facing bridge to execution governance

### 6. Rail reflection pass
Update the Executive Rail so it reflects orchestration/runtime state rather than being treated as an independent UI narrative surface.

Success condition:
- the rail becomes a window into actual runtime truth

---

## LATER

### 7. Governed evidence invocation path
Add selective internal-evidence invocation with legible evidence sourcing.

### 8. Trigger enrichment
Improve scenario-trigger precision and expand routing sophistication.

### 9. Human escalation ledger path
Surface Authority Events and Human Judgment Ledger Entries cleanly in UI/API flows.

### 10. Agent admission integration
Introduce certified bounded labor only after orchestration and EBE paths are stable.

### 11. Multi-step workflow control
Allow broader workflow execution only after action contracts and boundary logic prove stable.

---

## EXPLICIT NON-GOALS FOR THE NEXT TRANCHE

The next implementation tranche should NOT attempt to solve:

- full autonomous agent management
- generalized workflow automation
- giant scenario-trigger forests
- universal memory architecture
- final production-grade intent classification
- broad evidence fabric ingestion
- full bridge logic for all future modules

These are valid future directions, but they should not dilute the next build step.

---

## First implementation target

The first code target after this note should be a small orchestration service module with narrow responsibilities:

1. classify the turn
2. create the scenario envelope
3. route to the correct current subsystem
4. return a combined output envelope

This target should be intentionally modest.

The goal is not brilliance yet.  
The goal is runtime discipline.

---

## Recommended first code boundary

Suggested first module concept:

`src/service/orchestration/service.py`

Possible initial responsibilities:

- `classify_turn(...)`
- `build_scenario_envelope(...)`
- `route_turn(...)`
- `run_orchestration(...)`

Suggested first test target:

`src/service/orchestration/test_service.py`

The first tests should prove:

- decision-seeking turns route to Decision Loop
- action-proposing turns emit Action Proposal structure
- execution-seeking turns require EBE path
- conversational turns do not accidentally create execution state

---

## Current conclusion

The next code move should be small, governed, and structurally honest.

Build the orchestration skeleton first.  
Then harden the Action Proposal contract.  
Then connect execution-seeking turns to EBE v2.  
Then make the rail reflect runtime truth.

That is the disciplined sequence now.

# Execution Boundary Engine (EBE) Spec

## Purpose

The Execution Boundary Engine (EBE) is the control layer that sits between a computed decision and any attempted action.

Its job is to ensure that a decision produced at reasoning time is still valid at execution time.

Execalc is therefore not only a decision system. It is a decision-plus-execution-governance system.

---

## Core Principle

A decision that is correct at time T0 may be invalid at time T1.

Between reasoning and execution, any of the following may change:

- system state
- user authority
- available facts
- timing conditions
- policy constraints
- risk profile
- execution feasibility

Therefore, no action may execute without commit-time revalidation.

---

## Required Runtime Flow

Signal
↓
Decision Loop Engine
↓
Action Proposal
↓
Execution Boundary Engine
↓
ALLOW / BLOCK / RECOMPUTE / ESCALATE
↓
Execution OR Human Review

---

## Stage Scope

This stage implements:

- Stage 4C — Action Proposal Contract
- Stage 4D — Execution Boundary Engine
- Stage 4E — Execution Audit Trail

This stage does not rebuild the existing Decision Loop Engine or UI Executive Rail.

---

## Existing Components

The following already exist and must be reused rather than rebuilt:

- Decision Loop Engine
- `/api/decision/run`
- ExecutionRecord baseline persistence
- Workspace UI scaffold
- Executive Rail component

---

## New Models Required

### 1. ActionProposal

Represents a candidate action produced by the decision layer.

Suggested fields:

- `proposal_id`
- `tenant_id`
- `user_id`
- `action_type`
- `target_ref`
- `payload`
- `decision_envelope_id`
- `issued_at`
- `expires_at`
- `authority_context`
- `risk_level`
- `requires_human_review`

### 2. ExecutionSnapshot

Represents the world as seen at the moment execution is attempted.

Suggested fields:

- `snapshot_time`
- `tenant_id`
- `user_id`
- `current_authority`
- `current_state_hash`
- `constraint_flags`
- `policy_flags`
- `required_inputs_present`
- `risk_posture`
- `execution_window_open`

### 3. BoundaryDecision

Represents the result returned by the EBE.

Required outcomes:

- `ALLOW`
- `BLOCK`
- `RECOMPUTE`
- `ESCALATE`

Suggested fields:

- `status`
- `reasons`
- `blocking_checks`
- `requires_human_review`
- `audit_payload`

---

## Engine Responsibilities

File to create:

- `src/service/decision_loop/execution_boundary_engine.py`

Responsibilities:

1. Accept an `ActionProposal`
2. Accept an `ExecutionSnapshot`
3. Validate time validity
4. Validate authority at execution time
5. Validate required inputs
6. Validate policy and constraint posture
7. Validate risk posture
8. Return a deterministic `BoundaryDecision`

---

## Mandatory Governance Rules

1. No action executes without passing EBE
2. No inherited authority from reasoning phase
3. All decisions are time-bound
4. Fail closed if uncertain
5. Every execution attempt is logged

---

## Decision Logic Requirements

### ALLOW
Return `ALLOW` only if all required checks pass.

### BLOCK
Return `BLOCK` when execution is prohibited by missing authority, expired timing, policy restriction, or hard constraint failure.

### RECOMPUTE
Return `RECOMPUTE` when the decision may still be viable, but the reasoning is stale because material conditions changed.

### ESCALATE
Return `ESCALATE` when execution should not proceed automatically and requires human review.

Examples:

- risk increased above threshold
- contradictory signals exist
- ambiguous authority state
- action marked high impact
- policy requires manual approval

---

## Minimum Deterministic Checks

The first implementation must support deterministic checks for:

- proposal expiration
- missing current authority
- missing critical inputs
- execution window closed
- policy flag present
- hard constraint flag present
- elevated risk posture
- manual review flag on proposal

---

## Audit Trail Requirements

Every execution attempt must generate an audit record, whether successful or blocked.

This can be done by:

- extending `ExecutionRecord`, or
- introducing `ExecutionAuditRecord`

Audit data should capture:

- proposal identity
- tenant identity
- user identity
- execution timestamp
- snapshot summary
- boundary outcome
- reasons
- whether human review was required

---

## Testing Requirements

Deterministic unit tests must cover:

- valid proposal returns `ALLOW`
- expired proposal returns `BLOCK`
- missing authority returns `BLOCK`
- missing critical inputs returns `RECOMPUTE` or `BLOCK` depending on implementation choice
- elevated risk returns `ESCALATE`
- manual review flag returns `ESCALATE`
- policy block returns `BLOCK`

Tests must avoid non-deterministic runtime behavior.

---

## Product Meaning

- The Executive Rail shows the reasoning surface.
- The Decision Loop produces judgment.
- The EBE governs whether judgment may become action.

This is the boundary between intelligence and execution.

Execalc therefore becomes the system that makes judgment computable and action governable.

---

## Definition of Done

This stage is complete when:

- spec file exists in repo
- models are created
- EBE module is implemented
- audit trail path is defined
- unit tests cover all major branches
- local validation passes
- changes are committed and pushed

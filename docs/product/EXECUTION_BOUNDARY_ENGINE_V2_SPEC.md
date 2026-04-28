# Execution Boundary Engine v2 (EBE v2)

Status: Proposed runtime specification  
Purpose: Define the governed runtime authority and admissibility layer that sits between reasoning and real-world action.

---

## Purpose

The Execution Boundary Engine v2 is the runtime control layer that governs the transition from:

- reasoning
- to
- action

Its purpose is to ensure that no decision, recommendation, agent output, or workflow proposal is allowed to mutate real-world state unless it is revalidated at the exact moment execution becomes possible.

This module exists because a valid decision at T0 may become invalid, unauthorized, inadmissible, or strategically unsound by T1.

The engine turns governance from:

- documentation
- into
- architecture

---

## Core doctrine

No reasoning output inherits execution authority by default.

Execution authority must be resolved at the commit surface against:

- current mandate
- current delegation
- current system context
- current strategic validity

If that resolution fails, the action must not proceed.

---

## Why v2 exists

The first version of the Execution Boundary concept established that actions must be revalidated before execution.

Version 2 expands that idea with several stronger architectural truths:

- governance must resolve at execution, not just upstream
- authorization is time-bound
- trusted agents and admissible actions are separate problems
- proof must be more than a log
- human escalation requires its own ledger
- the system must fail closed under uncertainty
- organizational objective cartridges are directional influences, not final authority

---

## Architectural position

The Execution Boundary Engine v2 sits between all decision-capable logic and all state-changing actions.

Runtime flow:

`Signal / Prompt / Agent Proposal -> Decision Loop Engine -> Action Proposal -> Execution Boundary Engine v2 -> ALLOW / BLOCK / RECOMPUTE / ESCALATE / CONTAIN -> External action, deferred review, or recomputation`

This applies to:

- internal Execalc outputs
- agent-generated proposals
- cross-system workflow actions
- cross-tenant bridge proposals
- human-approved execution attempts

---

## Primary questions the engine must resolve

At the moment of commit, the engine must answer:

### 1. Is this action still valid?
Are the assumptions behind the proposal still true?

### 2. Is this action still authorized?
Does the actor still have legitimate authority right now?

### 3. Is this action still admissible?
Do mandate, delegation, and system context align at this moment?

### 4. Is this action still strategically correct?
Does the proposed action still satisfy the governing objective, Prime Directive, and current organizational priorities?

### 5. Is this action still defensible?
Can the system produce attributable evidence of why this action is permitted?

---

## Required inputs

The engine should resolve against five input classes.

### A. Action Proposal

Structured output from the Decision Loop or agent layer.

Minimum contents:

- proposal_id
- originating_decision_id
- initiating_actor
- scenario_type
- governing_objective
- action_type
- action_payload
- assumptions
- constraints
- approval_thresholds
- originating_timestamp
- tenant_id
- confidence
- proposed_execution_target

### B. Live Authority State

Current authority information at the moment of action.

Includes:

- actor_identity
- actor_role
- authorization_status
- delegation_chain
- allowed_action_classes
- expiry_or_revocation_state
- tenant_policy_overlays
- cartridge_influence_status

### C. Live System Context

Current world and system state relevant to the action.

Includes:

- current_relevant_facts
- operational_conditions
- policy_version
- threshold_values
- environmental_version
- related_state_changes_since_proposal_creation
- system_health
- action_path_readiness

### D. Strategic Context

Current decision-layer truth relevant to admissibility.

Includes:

- governing_objective
- active_organizational_objective_cartridges
- prime_directive_checks
- current_material_tradeoffs
- known_scenario_shifts
- active_risk_flags
- whether_original_decision_remains_aligned

### E. Human Escalation State

If the action is being escalated or overridden by a human, the system must ingest:

- who accepted, rejected, deferred, or overrode
- under what authority
- at what time
- with what rationale
- whether override authority was valid

---

## Resolution logic

The engine must resolve in this order.

### Step 1 — Identity and tenant resolution
Confirm the actor, tenant, and pathway are legitimate.

### Step 2 — Authority resolution
Confirm the actor is currently authorized for this class of action.

### Step 3 — Context admissibility
Confirm the live state still supports the action.

### Step 4 — Strategic revalidation
Confirm the action still satisfies the Prime Directive, governing objective, and material strategic conditions.

### Step 5 — Escalation / containment decision
If ambiguity remains, decide whether to:

- escalate
- contain
- block
- recompute

### Step 6 — Proof / ledger emission
Emit the required authority and judgment artifacts.

---

## Output states

Version 2 supports five output states.

### 1. ALLOW
The action is admissible, authorized, and strategically sound.

### 2. BLOCK
The action must not proceed.

Examples:
- authority revoked
- invalid actor
- out-of-scope action
- explicit policy conflict

### 3. RECOMPUTE
The action is stale because material context changed.

Examples:
- assumption broken
- market moved
- scenario shifted
- strategic tradeoff materially changed

### 4. ESCALATE
The action may still be possible, but requires human judgment.

Examples:
- threshold breach
- ambiguity
- elevated risk
- policy gray zone

### 5. CONTAIN
The action cannot proceed yet, but should be held in non-executable form pending resolution.

Examples:
- incomplete snapshot
- temporary uncertainty
- waiting for authoritative signal
- unresolved live-state dependency

This CONTAIN state is distinct from both BLOCK and ESCALATE.

---

## Hard runtime rules

### Rule 1
No action may execute without passing the boundary.

### Rule 2
Authority may not be inherited from earlier reasoning.

### Rule 3
Admissibility is time-bound.

### Rule 4
If live state cannot be resolved confidently, fail closed.

### Rule 5
Organizational Objective Cartridges are directional influences, not absolute directives. A cartridge may weight evaluation, but final override authority remains with a properly authorized human.

### Rule 6
Escalated human judgment must itself be recorded as a governed event.

---

## Proof objects and ledgers

Version 2 explicitly separates two artifacts.

### A. Authority Event

A durable runtime artifact proving why the action was considered legitimate or illegitimate at the moment of commit.

Contains:

- proposal_id
- authority_chain
- live_policy_state
- admissibility_result
- boundary_decision
- timestamp
- proof_reference

This leaves behind attributable evidence, not just generic logs.

### B. Human Judgment Ledger Entry

Required whenever the architecture deliberately hands the decision to a human.

Contains:

- escalation_id
- proposal_id
- human_decider
- role_or_authority_basis
- action_taken
- reason_entered
- override_category
- timestamp

This addresses the missing-ledger problem for human escalation and override.

---

## Relationship to agent certification

The Execution Boundary Engine v2 must explicitly recognize that:

- trusted agent status
- and
- admissible action status

are different things.

A certified agent may be eligible to propose work.  
It is not automatically eligible to execute work.

So:

### Upstream trust layer
Agent certification or admission determines whether an agent may participate.

### Runtime boundary layer
EBE v2 determines whether a specific action may happen now.

This is a permanent architectural distinction.

---

## Relationship to Execalc modules

### 1. Decision Loop Engine
Produces structured Action Proposals.

### 2. Support Stack
Supplies reflexes and runtime risk signals.

Examples:

- missing_critical_input
- stale_context_detected
- authority_mismatch
- execution_path_unresolved

### 3. Security Stack
Supplies tenant isolation, identity verification, and access policy.

### 4. Organizational Objective Cartridges
Provide directional weighting during strategic revalidation, but never replace human authority.

### 5. Governed Bridge
Any cross-client or cross-tenant proposal must pass through EBE v2 before action.

---

## Minimum test matrix for v2

### Test 1 — No drift
Proposal valid, live context unchanged.  
Expected: ALLOW

### Test 2 — Authority revoked
Proposal valid at creation, authority inactive at commit.  
Expected: BLOCK

### Test 3 — Threshold crossed
Proposal within threshold at T0, exceeds threshold at T1.  
Expected: ESCALATE

### Test 4 — Material state drift
Core assumption no longer true.  
Expected: RECOMPUTE

### Test 5 — Snapshot incomplete
Context cannot be resolved.  
Expected: CONTAIN or ESCALATE, never ALLOW

### Test 6 — Cartridge conflict
Objective cartridge favors action, but Prime Directive rejects it on value/risk grounds.  
Expected: BLOCK or RECOMPUTE; cartridge does not override reality

### Test 7 — Human override
Boundary escalates, authorized human approves.  
Expected: Human Judgment Ledger Entry required before ALLOW

### Test 8 — Unauthorized human override
Escalation accepted by human lacking proper authority.  
Expected: BLOCK

### Test 9 — Certified agent, inadmissible action
Trusted agent proposes action outside current live scope.  
Expected: BLOCK

### Test 10 — Re-entry after stale signal
Old proposal reappears under new valid conditions.  
Expected: treat as new decision event; no inherited authority

---

## Design philosophy

The engine is not merely a safety check.

It is the place where:

- judgment
- authority
- context
- admissibility
- accountability

converge.

Its purpose is not just to explain actions later.  
Its purpose is to make illegitimate actions impossible now.

---

## Strategic significance

EBE v2 upgrades Execalc from:

- governed decision support

to:

- governed decision-to-action control

That is a much stronger category.

It means Execalc does not merely help organizations think better.  
It controls whether proposed machine-supported actions deserve to become real.

---

## One-paragraph canonical summary

The Execution Boundary Engine v2 is Execalc’s runtime authority and admissibility layer. It sits between reasoning and real-world action and ensures that no proposal—whether produced by Execalc, an agent, or a cross-system workflow—can mutate operational state without commit-time revalidation against current authority, delegation, system context, and strategic truth. It returns one of five outcomes: ALLOW, BLOCK, RECOMPUTE, ESCALATE, or CONTAIN, and emits both Authority Events and Human Judgment Ledger Entries where required. This module makes governance architectural rather than documentary.

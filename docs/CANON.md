# Execalc Canon

## Purpose

This document is the top-level index of Execalc's durable operating canon.

Its role is to identify the repo artifacts that define the constitutional spine of the system and to clarify how doctrine, invariants, architecture, governance, product behavior, and implementation-facing specs relate to one another.

If a principle, model, or rule is meant to matter tomorrow, it should either live here or be referenced here.

---

## Core Rule

If it matters tomorrow, it must be written here today.

Chat is ideation.  
Repo is doctrine.  
Code is enforcement.

If an idea is not committed to the repository in structured form, it is not part of Execalc's operating canon.

---

## What "Canon" Means Here

In Execalc, canon means durable, versioned system doctrine that is intended to guide:

- architecture
- governance
- product behavior
- runtime design
- implementation sequencing
- drift prevention
- build review
- future dev chat rehydration

Canon is not just documentation.
It is the constitutional layer of the build.

---

## Canon Hierarchy

The repo canon should be understood in the following order of authority:

### 1. Invariants
Non-negotiable build contracts and hard requirements.

If anything conflicts with invariants, the invariant wins.

Primary anchor:
- `docs/EXECALC_INVARIANTS.md`

Supporting anchors:
- `docs/invariants/README.md`
- `docs/invariants/INV-001_ai_is_subroutine.md`

### 2. Vision / True North
Defines what Execalc is trying to become and what must not be precluded.

Primary anchors:
- `docs/vision/TRUE_NORTH.md`
- `docs/vision/STAGE_MAP.md`
- `docs/vision/SPINE_NON_PRECLUSION_CHECKLIST.md`
- `docs/vision/GAQP_FOUNDING_CHARTER.md`
- `docs/vision/ENTERPRISE_QUALITATIVE_SYNTHESIS_THESIS.md`

Supporting anchor:
- `docs/architecture/EXECALC_TRUE_NORTH.md`

### 3. Canonization Rules
Define how ideas move from chat into structured doctrine and then into code.

Primary anchor:
- `docs/vision/CANONIZATION_PROTOCOL.md`

### 4. Governance Canon
Defines the governing rules, enforcement layers, and runtime safety logic.

Primary anchors:
- `docs/governance/SYSTEM_GOVERNANCE_CHARTER.md`
- `docs/governance/STRATEGIC_MESH_GOVERNANCE_MAPPING.md`
- `docs/governance/GOVERNANCE_ENFORCEMENT_REGISTER.md`

Supporting anchors:
- `docs/governance/FREE_AGENT_REFLEX.md`
- `docs/governance/FUTURE_GOVERNANCE_EXPANSIONS.md`
- `docs/governance/STAGE_SLOT_MAP_GOVERNANCE_UPGRADES.md`

### 5. Core Architecture Canon
Defines the major system models that explain how Execalc works.

Primary anchors:
- `docs/architecture/EXECALC_STRATEGIC_OPERATING_SYSTEM_MODEL.md`
- `docs/architecture/EXECALC_REASONING_STACK.md`
- `docs/architecture/EXECALC_RUNTIME_MODEL.md`
- `docs/architecture/JUDGMENT_KERNEL_ARCHITECTURE.md`
- `docs/architecture/EXECALC_RUNTIME_OBJECT_MODEL.md`

Supporting anchors:
- `docs/architecture/EXECALC_LAYER_MODEL.md`
- `docs/architecture/ORGANIZATIONAL_COGNITION_MODEL.md`
- `docs/architecture/INTER_ORG_INTERACTION_MODEL.md`
- `docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_STRATA.md`
- `docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_ACTIVATION_AND_SIGNALING_MODEL.md`
- `docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_DIAGNOSTIC_COMMANDS.md`
- `docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_CORPUS_SCHEMA.md`
- `docs/architecture/PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md`
- `docs/architecture/SUBSTRATE_ROUTING_AND_MODEL_TIERING_DOCTRINE.md`
- `docs/architecture/NETWORK_HEURISTIC_PROMOTION_MODEL.md`
- `docs/architecture/EXECALC_CATEGORY_ARCHITECTURE_MAP.md`

### 6. Runtime / Product Surface Canon
Defines how governed cognition appears to the operator.

Primary anchors:
- `docs/runtime/EXECUTIVE_KNOWLEDGE_ENGINE_RUNTIME_SCAFFOLDING.md`
- `docs/product/EXECALC_CHAT_BEHAVIOR_SPEC.md`
- `docs/product/EXECALC_USER_INTERFACE_ARCHITECTURE.md`

Supporting anchors:
- `docs/product/EXECALC_CUSTOMER_EXPERIENCE_CHARTER.md`
- `docs/product/DECISION_LOOP_ENGINE_SPEC.md`
- `docs/product/COMPARATIVE_DECISION_MEMORY_SPEC.md`
- `docs/product/INTELLIGENT_FRONT_DOOR_SPEC.md`
- `docs/product/EXECALC_QUALITATIVE_FORMULA_LIBRARY_V0_1.md`
- `docs/product/SIGNAL_ELEVATION_AND_RAIL_CANDIDACY.md`
- `docs/product/GAQP_VS_CONSULTING_CRAFT_POSITIONING.md`

### 7. Build / State / Rehydration Canon
Defines where the build is, how it is resumed, and how dev work remains disciplined.

Primary anchors:
- `docs/BUILD_STATE.md`
- `docs/NEXT_ACTIONS.md`
- `docs/BUILD_COCKPIT.md`
- `docs/process/DEV_CHAT_REHYDRATION_PROTOCOL.md`

Supporting anchors:
- `docs/STAGE_MAP.md`
- `docs/build_plan/BUILD_DOCTRINE.md`
- `docs/product/STAGE_STATUS.md`

---

## Canonical Operating Rules

### Rule 1: Repo outranks chat
If chat conflicts with repo doctrine, the repo wins.

### Rule 2: Invariants outrank ordinary docs
If a normal architecture or product doc conflicts with invariants, the invariant wins.

### Rule 3: Code must converge to canon
Implementation is not the source of truth when it drifts from explicit doctrine.

### Rule 4: Major ideas need explicit homes
No major concept should remain trapped in ephemeral chat once it is treated as durable.

### Rule 5: Canon should be navigable
A doctrine set that cannot be found or traversed is only partially useful.

---

## What Belongs in Canon

Material belongs in canon when it is:

- durable
- operationally meaningful
- likely to matter across future chats or implementation phases
- likely to affect architecture, governance, or product behavior
- something we want future developers or future chats to treat as authoritative

Examples:
- invariants
- runtime models
- governance rules
- object models
- operating principles
- product behavior contracts
- boundary models
- build protocols

---

## What Does Not Automatically Belong in Canon

Not every useful idea belongs in top-level canon.

Examples of things that may remain outside top-level canon unless elevated:
- temporary notes
- rough brainstorms
- local implementation details
- exploratory wording
- abandoned concepts
- chat-only thought experiments

These may still live in the repo, but they are not automatically constitutional.

---

## Canon and Enforcement

Canon by itself is not enough.

The repo structure assumes three linked layers:

1. Doctrine  
   Written in markdown and versioned in the repo

2. Enforcement  
   Implemented in deterministic code, middleware, policies, schemas, and tests

3. Auditability  
   Verified through logs, decision artifacts, CI checks, and reviewable history

A healthy system keeps these three aligned.

---

## Required Anchor Files for New Dev Chats

At minimum, the following files should anchor future dev chat rehydration:

- `docs/vision/TRUE_NORTH.md`
- `docs/vision/STAGE_MAP.md`
- `docs/EXECALC_INVARIANTS.md`
- `docs/vision/CANONIZATION_PROTOCOL.md`
- `docs/BUILD_STATE.md`
- `docs/NEXT_ACTIONS.md`

For architecture-heavy work, future chats should also hydrate from:
- `docs/architecture/EXECALC_RUNTIME_MODEL.md`
- `docs/architecture/JUDGMENT_KERNEL_ARCHITECTURE.md`
- `docs/architecture/EXECALC_RUNTIME_OBJECT_MODEL.md`

---

## Canon Maintenance Rules

### 1. Canon must be updated deliberately
Major doctrine changes should not be left implicit.

### 2. Canon should prefer clear indexing over hidden sprawl
If a concept becomes important enough, it should be easy to find from this file.

### 3. Canon should preserve lineage
New doctrine should extend or refine existing models rather than fragment them casually.

### 4. Canon should reduce drift
The point of canon is to stabilize future work, not merely to archive thoughts.

### 5. Canon should remain implementation-relevant
Canonical docs should help guide real code, real surfaces, and real governance.

---

## Current Canon Highlights

As of the current repo state, the most important hardened areas are:

- Strategic Mesh governance
- seven-layer reasoning stack
- runtime object model
- runtime model
- Judgment Kernel architecture
- Executive Knowledge Engine strata and activation logic
- diagnostic command doctrine
- runtime scaffolding
- chat behavior contract
- user interface architecture
- organizational cognition model
- inter-organization interaction model
- Free Agent Reflex doctrine

This means the repo now contains a materially stronger constitutional and architectural spine than before.

---

## Summary

This file is the top-level map of Execalc's durable operating canon.

Its function is to make the constitutional spine of the system easy to find, easy to navigate, and harder to lose.

If a future chat needs to know what is authoritative, this file should be one of the first places it looks.

# EXECALC RECURSIVE REBUILD PLAN

## Purpose
This document defines the controlled rebuild plan for Execalc. It exists to convert architectural audit findings into a deterministic remediation program that strengthens the system without degrading working behavior.

## Rebuild Standard
This rebuild operates under Huang-level engineering discipline by default:
- architecture first
- deterministic execution
- verification before trust
- repo as source of truth
- no silent drift
- no casual protected-branch work
- no architecture counted as real until it is represented, enforced, observable, and testable

## Governing Repo Artifacts
The rebuild is governed by the following repository artifacts:
- `docs/dev/EXECALC_LLM_BUILD_PROTOCOL.md`
- `docs/dev/EXECALC_BUILD_DISCIPLINE.md`
- `docs/dev/EXECALC_CHAT_REHYDRATION_PROTOCOL.md`
- `docs/architecture/EXECALC_RUNTIME_ENFORCEMENT_MATRIX.md`

## Core Rebuild Principle
The rebuild does not proceed by random file editing. It proceeds by closing enforcement gaps.

Each meaningful rebuild move must identify:
- target capability or enforcement row
- enforcement location
- preserved behavior
- verification method
- remaining open questions

## Rebuild Workflow
Each rebuild session should follow this sequence:

1. Rehydrate the chat from repo artifacts
2. Inspect the current repository state
3. Select one enforcement target
4. Make one controlled architectural change
5. Verify the result
6. Commit and push only after verification
7. Record what changed and what remains open

## Major Rebuild Phases

### Phase 1 — Governance and Build Discipline
Status: In progress / largely established

Objectives:
- install repo-level build protocol
- install build discipline standard
- install chat rehydration protocol
- install runtime enforcement matrix
- install GitHub governance guardrails

### Phase 2 — Engine Hardening
Status: In progress / materially advanced

Objectives:
- strengthen `DecisionArtifact` into the canonical governed judgment object
- add structured Prime Directive fields
- add structured Polymorphia fields
- add execution trace / support metadata
- preserve current report behavior while strengthening the runtime contract

Completed in current rebuild segment:
- strengthened decision runtime contract in `src/service/decision_loop/models.py`
- strengthened decision engine behavior in `src/service/decision_loop/engine.py`
- added direct orchestration layer in `src/service/decision_loop/service.py`
- thinned `/decision/run` in `src/service/api.py` by delegating orchestration
- added route-level decision API coverage in `src/service/test_decision_api.py`
- verified broader `src/service` suite green in `.venv`

### Phase 3 — Core 7 Runtime Enforcement
Status: Planned

Objectives:
- close Prime Directive enforcement gaps
- define and enforce Persistent Memory structures
- define and enforce Heuristic Coding structures
- define and enforce Recursive Reintegration structures
- strengthen Executive Knowledge Engine runtime linkage
- define initial Proactive Solutions runtime structures

### Phase 4 — Support Stack Runtime Enforcement
Status: Planned

Objectives:
- formalize ingress discipline
- formalize routing discipline
- formalize fallback behavior
- formalize recursive audit triggers
- formalize observability surfaces

### Phase 5 — Security Stack Runtime Enforcement
Status: Planned

Objectives:
- enforce tenant isolation boundaries
- strengthen authorization controls
- define data classification handling surfaces
- strengthen audit logging
- define connector and bridge boundary expectations

### Phase 6 — CI / Test / Branch Enforcement Completion
Status: Planned

Objectives:
- complete CI detection in GitHub
- require status checks on `main`
- expand test coverage around runtime enforcement rows
- ensure governance rules are mechanically enforced

## Immediate Next Architectural Move
The next active target is:

**Direct service-layer hardening and adjacent decision route alignment**

Initial focus:
- add direct unit coverage for `src/service/decision_loop/service.py`
- inspect `/decision/<envelope_id>` and `/decision/recent` for architectural drift
- continue closing enforcement gaps between runtime objects, orchestration, and route behavior

Goal:
- ensure the decision service boundary is directly tested and the adjacent decision routes are aligned to the normalized architecture

## Session Closure Standard
A rebuild session is only considered complete when:
- the change was verified
- the repo state is known
- the next target is clear
- the rebuild remains aligned to the Runtime Enforcement Matrix

## Intended Use
This file should be loaded into every rebuild chat and used as the navigation chart for the recursive rebuild.

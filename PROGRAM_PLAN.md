# PROGRAM_PLAN.md
## Executive Calculus (Execalc) — Program Requirements and Architecture Plan

---

## 1. Program Purpose

Execalc is being built as governed intelligence infrastructure for organizations. Its purpose is to transform how institutions perceive signals, synthesize qualitative information, form judgments, route decisions, and preserve institutional reasoning over time.

The system is designed to help organizations move from legacy information workflows to governed cognitive workflows.

Legacy information workflows were built for a world in which humans were the only available synthesis engine. Large language models change that condition. Execalc exists to govern that new capability so it becomes reliable enough for executive use.

---

## 2. Program Thesis

The full thesis of Execalc is built on six linked beliefs:

1. Large language models now do for qualitative information what spreadsheets did for quantitative information.
2. Most enterprise workflows are still designed around early-2000s information technology.
3. The biggest organizational bottlenecks are signal fragmentation, manual synthesis, hierarchical translation, and institutional amnesia.
4. The next great enterprise advantage is decision-cycle compression.
5. The end state is to compress the decision cycle until the only remaining bottleneck is human judgment.
6. Governed AI may ultimately create advantage not only by speed, but by revealing patterns previously invisible to human cognition.

---

## 3. Product Category

Execalc is not an AI application in the ordinary sense. It is a new infrastructure layer.

**Category definition:**

> Execalc is governed intelligence infrastructure — the system that converts machine prediction into disciplined organizational judgment.

---

## 4. Strategic Mesh Architecture

Execalc is governed by a permanent architecture called the Strategic Mesh.

### 4.1 Cognitive Engine
The immutable reasoning core composed of the Core 7 Frameworks.

### 4.2 Operational Control Layer
The Support Stack / Fusebox containing QA logic, reflexes, drift protection, and runtime guardrails.

### 4.3 Security Enforcement Layer
The trust and isolation layer governing tenant separation, auditability, access control, and breach prevention.

Design goals:
- separate cognition from runtime protection
- separate runtime protection from security enforcement
- permit independent auditing of each layer
- prevent logic bleed between layers
- maintain enterprise-grade integrity under scale

---

## 5. The Core 7 Frameworks

These frameworks form the cognitive constitution of Execalc. They are permanent system law and must remain visible in the architecture.

### 5.1 Prime Directive
All reasoning must be evaluated through:
- Value Creation
- Risk/Reward Asymmetry
- Supply/Demand Imbalance
- Assets/Liabilities (Balance Sheet)

All four lenses must be evaluated. The sin is not imbalance — it is blindness. A decision where any lens was never evaluated is a governance failure.

### 5.2 Persistent Memory
A governed memory layer preserving prior decisions, constraints, operator context, and strategic continuity across sessions and over time.

### 5.3 Multi-Dimensional Logic (Polymorphia)
Reasoning across multiple simultaneous dimensions: financial, strategic, reputational, organizational, temporal, relational, regulatory.

### 5.4 Heuristic Coding System
Detection, encoding, storage, and activation of reusable strategic instincts and judgment fragments.

### 5.5 Recursive Analysis
Post-decision and runtime self-audit for drift detection, assumption failure, reasoning quality evaluation, and continuous improvement.

### 5.6 Proactive Solutions Architecture
Anticipatory scanning and surfacing of unseen opportunities, unresolved tensions, emerging risks, and latent asymmetries — before the operator asks.

### 5.7 Executive Knowledge Engine
Runtime fusion of scenarios, thinkers, overlays, heuristics, reflexes, and organizational context into governed executive output.

---

## 6. Support Stack Requirements

The Support Stack is the operational immune system of Execalc. It is mutable and should improve through use, testing, and documented refinement.

Expected functions include:
- reflex gating
- complaint-triggered recursive audits
- contradiction checks
- heuristic hygiene
- drift detection
- memory integrity enforcement
- reintegration paths after errors
- soup-vs-signal discrimination
- latent strategic value promotion

The Support Stack is mandatory, not optional. It is not a governance feature layer — it is the operational law of the system.

---

## 7. Security Enforcement Requirements

Execalc must be built from the outset with a security-first enterprise posture.

Requirements:
- strict tenant isolation
- namespace enforcement
- auditable reasoning trails
- role-aware behavior
- breach prevention assumptions
- secure memory access
- traceable state transitions
- zero-trust-compatible posture
- no shared hidden context across tenants

Security is not an add-on. It is architectural. The system should be capable of growing into Fortune-500 and enterprise scrutiny without rewrite.

---

## 8. Runtime Model

Execalc reasons through governed runtime pathways, not raw LLM calls.

Canonical pattern:

```
Scenario → Activation Pathway → Heuristics / Thinkers / Reflexes → Prime Directive → Decision Artifact
```

The system must support:
- scenario detection
- structured decision reports
- comparable decision artifacts
- execution boundary checks
- memory admission and retrieval
- observe-only stability and drift instrumentation
- action proposal generation
- audit-friendly traceability

---

## 9. Workflow Redesign Thesis

The system exists to redesign modern organizational information workflows.

**Legacy workflow:**
```
email → document → meeting → spreadsheet → deck → meeting → decision
```

**Target workflow:**
```
signal → synthesis → decision artifact → action → memory
```

Every build decision should ask:
- Does this reduce cognitive friction?
- Does this improve signal fidelity?
- Does this reduce translation overhead?
- Does this preserve institutional reasoning?

---

## 10. Atomic Operations of Organizational Cognition

Execalc formalizes and accelerates the primitive verbs of organizational thinking:

1. signal detection
2. signal capture
3. signal classification
4. signal synthesis
5. signal prioritization
6. decision formation
7. action routing
8. execution
9. outcome observation
10. institutional memory

These atomic operations are more fundamental than department labels or software categories. The system should be understood as infrastructure for these operations.

---

## 11. Product Surfaces

Expected product surfaces:
- executive chat
- decision workspace
- live executive brief / right rail
- personal and team dashboards
- organizational front door (Intelligent Front Door)
- email-connected reasoning surfaces
- calendar-connected preparation surfaces
- internal team communication surfaces
- deal / account intelligence views
- bridge surfaces between consenting organizations

All surfaces must connect to the same governed reasoning architecture.

---

## 12. UX Requirements

Execalc should feel like executive instrumentation — a cockpit, not a consumer app.

Principles:
- high signal, low noise
- explicit confidence and uncertainty signals
- structured decision artifacts over loose prose
- contextual side intelligence (right rail)
- calm, serious presentation
- explainable outputs
- no novelty-first design decisions

---

## 13. Engineering Requirements

Code must be enterprise-readable and maintainable.

Required qualities:
- explicit contracts
- typed models where appropriate
- modular boundaries
- inspectable reasoning seams
- isolated side effects
- no hidden behavior
- no undocumented shortcuts
- no "magic" AI logic without structural explanation

Important reasoning paths must be inspectable in code.

---

## 14. Multi-Tenant Requirements

The system must remain future-safe for serious SaaS deployment.

Requirements:
- tenant-scoped data everywhere
- `tenant_id` enforcement at persistence and query boundaries
- namespaced storage
- no cross-tenant bleed
- role-aware permissions
- secure memory design
- no convenience shortcuts that force later rewrites

Do not build prototype patterns that require architectural surgery to harden.

---

## 15. Memory and Governance Rules

Memory must be governed, not merely stored.

Rules:
- store signal, not soup
- preserve provenance
- preserve confidence levels
- preserve activation context
- support audit and suppression
- support dormant memory classes
- separate reference-only from active logic
- preserve reasoning trails behind decisions

Memory is part of the cognition engine, not a convenience layer.

---

## 16. Documentation Requirements

Documentation is a first-class artifact of the build.

Required doc categories:
- architecture
- product specs
- build discipline
- stage status
- traceability
- next actions
- plain-English summaries for leadership

Every meaningful architectural choice should explain:
- what was built
- why it exists
- what it governs
- what assumptions it makes
- what remains next

The system must remain explainable to non-technical leadership at all times.

---

## 17. Testing Requirements

The build must enforce:
- endpoint shape tests
- contract tests
- uncertainty behavior tests
- tenant-scoping tests
- audit field tests
- drift / stability scaffolding tests
- memory contract tests
- regression capture where possible

Unknowns must be represented honestly. Confidence must never be fabricated.

---

## 18. Near-Term Build Priorities

Current priorities:
1. Support Stack Phase 4 — condition-aware boundary decisions
2. Service layer extraction for GET /decision/ endpoints
3. Stage 7A DB integration-test slice
4. Memory runtime scaffolding (Stage 8B.8)
5. Persistent Memory Phase 1 runtime — EKE corpus schema + admission endpoint

---

## 19. Long-Term Program Vision

The long-term vision is an enterprise cognition platform where:

- every organization has an intelligent front door
- signals are continuously synthesized across the org
- executive judgment is governed and accelerated
- organizational memory compounds over time
- governed bridges can exist between consenting organizations
- every seat receives governed intelligence calibrated to its role
- decision latency collapses to the natural limit of human judgment
- the organization operates as an intelligent institution

This is the future operating environment the codebase should be quietly shaping toward from the first line of code.

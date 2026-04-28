# Stage 8B — Stability & Drift Foundations

Status: In progress — observe-only foundation implemented at the decision service seam, with executive-rail anomaly/signal surfacing, split stability/drift nuggets, and anomaly-priority signal suppression now live on `/execalc` and `/decisions`  
Purpose: Capture the next governance hardening layer for Execalc without derailing the newly established orchestration spine.

Current implementation checkpoint:
- Observe-only Stage 8B instrumentation now exists at `src/service/decision_loop/service.py`
- `audit.stability` and `audit.drift` are attached at the canonical decision-service seam
- Stability registry version `stage8b.2` tracks invariants for `decision_result`, `action_proposal`, and `execution_snapshot`
- Drift contract version `stage8b.3` tracks expected signals for `boundary_status`, `scenario_type`, and `governing_objective`
- `audit.stability.anomalies` and `audit.drift.anomalies` now exist as canonical observe-only anomaly arrays
- Both layers now emit live observe-only signals and report `status: signals_recorded`
- Runtime now records non-blocking anomalies for missing navigation context, unspecified governing objective, and non-ALLOW boundary outcomes
- The executive rail now surfaces:
  - anomaly strings
  - decision boundary state
  - structured runtime nuggets
  - observe-only stability/drift signals
  - distinct stability and drift signal nuggets
  - anomaly-priority suppression of matching sibling signals
- `/execalc` and `/decisions` now both surface Stage 8B signals through `LiveExecutiveBrief`
- Tests lock the current observe-only behavior for both anomaly-free and anomaly-present paths
- No blocking behavior has been introduced; this remains visibility-first scaffolding

Related context:
- `docs/product/EXECUTION_BOUNDARY_ENGINE_V2_SPEC.md`
- `docs/product/THIN_CHAT_ORCHESTRATION_LAYER.md`
- `docs/product/ORCHESTRATION_SPRINT_SEQUENCE.md`

---

## Why this stage exists

Execalc now has a stronger governed runtime spine:

- Decision Loop Engine
- Action Proposal contract
- Execution Boundary Engine v2 specification
- Thin Chat Orchestration Layer
- Narrow orchestration API bridge
- Narrow UI proof surface

That spine solved the immediate bridge problem between executive chat input and governed runtime behavior.

But the recent governance discussion surfaced the next maturity layer:

1. system stability must become an explicit invariant layer  
2. runtime drift must become a tracked phenomenon  
3. decision formation quality must become a governed pre-boundary concern  

This is not a sign that the current architecture is broken.

It is a sign that Execalc must evolve from:
- conceptually correct governance
to:
- architecturally explicit governance

---

## Core synthesis

Execalc already governs whether actions are allowed.

Now it must also begin to guarantee that:

- the system remains structurally stable as it evolves
- runtime drift becomes visible before it creates hidden risk
- decisions are properly formed before they ever reach execution review

---

## This stage is NOT

This stage is not:

- a rewrite of the Decision Loop
- a replacement for EBE v2
- a broad enforcement pass
- a new blocking layer inserted everywhere immediately

This stage is additive scaffolding.

Its first job is to make these concerns explicit, measurable, and attachable to real runtime objects.

---

## The three new concerns

## 1. Stability Layer

### Definition
A formal invariant layer that defines what must remain true about key runtime objects and system pathways.

### Why it matters
Right now many of these conditions are present in spirit, but not all are named, testable, or enforced.

### Early examples
Depending on object type, stability checks may verify:

- required identifiers are present
- governing objective is explicit
- assumptions and constraints are visible
- scenario context is not missing
- runtime object structure remains coherent
- critical handoff artifacts do not degrade into loose soup

### Important rule
Stability checks must be defined against real shared runtime objects, not imagined future payloads.

---

## 2. Runtime Drift Monitor

### Definition
A layer that tracks when the system context, runtime environment, or governing conditions have changed in ways that should trigger caution, revalidation, or alerting.

### Why it matters
The governance discussion correctly identified that drift is not only a commit-surface issue.
The system itself evolves over time:

- permissions change
- integrations change
- thresholds change
- capabilities change
- environment snapshots age
- prior assumptions decay

### Early examples
First-generation drift signals may include:

- missing freshness timestamps
- missing environment version metadata
- stale execution snapshots
- authority changes
- policy version changes
- state mismatch between proposal time and current time

### Important rule
Drift monitoring should begin as instrumentation before it becomes a hard gate.

---

## 3. Decision Environment Guardrails

### Definition
Pre-boundary structural requirements that help ensure decisions are properly formed before they are ever evaluated for execution.

### Why it matters
Execution governance is not enough if the underlying decision is weakly formed.

The recent discussion correctly surfaced that a decision should not count as structurally adequate if key framing elements are invisible.

### Early examples
Depending on the runtime object, guardrails may eventually require visibility of:

- tradeoffs
- alternatives
- risk assessment
- assumptions
- option set clarity
- major downside exposure

### Important rule
Guardrails should be aligned to real decision outputs and proposal objects already in the system.
Do not impose invented schema requirements that current runtime objects do not yet support.

---

## Why this should not be wired directly into the live path yet

The recently proposed packet suggested adding direct hooks into the decision loop engine and checking generic `action_payload` structures.

That is directionally useful, but premature in its current form.

Why:

1. current shared runtime objects are still being normalized  
2. orchestration-to-decision-to-boundary integration was only just established  
3. forced enforcement against imagined payload shapes would create false violations  
4. instrumentation needs to precede hard blocking logic  

So Stage 8B should begin with:

- architecture note
- sequencing note
- object mapping
- instrumentation-first scaffolding

Then later:

- warning surfaces
- audit surfaces
- optional enforcement
- eventual blocking semantics where appropriate

---

## Relationship to existing modules

### Decision Loop Engine
Stage 8B does not replace it.  
It evaluates how structurally well-formed its outputs are.

### Thin Chat Orchestration Layer
Stage 8B may later annotate or surface drift / guardrail conditions through orchestration outputs.

### Execution Boundary Engine v2
Stage 8B does not replace commit-time admissibility review.  
It strengthens what arrives there and how runtime drift is understood upstream.

### Support Stack
Stage 8B should likely become a future contributor of reflex signals such as:

- stale_context_detected
- missing_critical_input
- decision_shape_incomplete
- drift_signal_present

### Security Stack
Stage 8B may later consume authority / policy / version metadata from the security layer.

---

## The correct implementation philosophy

### Instrument first
First make the new concerns visible and attachable.

### Enforce later
Only add blocking or fail-closed behavior once object contracts are truly stable and false positives are unlikely.

### Build against real objects
Use actual runtime contracts already present in the repo:

- ScenarioEnvelope
- shared ActionProposal
- decision outputs
- EBE-related artifacts

### Avoid parallel truths
Do not create a new abstract payload universe that competes with the live runtime model.

---

## Proposed Stage 8B sequence

### 8B.1 — Object Mapping
Identify the actual runtime objects Stage 8B will evaluate.

Candidate targets:
- decision report output
- shared ActionProposal
- execution-boundary input snapshot
- orchestration scenario envelope

### 8B.2 — Stability Note / Invariant Registry
Define the first explicit invariants against real runtime objects.

### 8B.3 — Drift Signal Stub
Create non-blocking drift detection stubs tied to actual metadata available in runtime objects.

### 8B.4 — Decision Guardrail Stub
Create non-blocking structural quality checks against decision and proposal outputs.

### 8B.5 — Visibility Only
Surface warnings in audit or debug output first.

### 8B.6 — Graduated Enforcement
Only after signal quality is good should these checks become gating or escalation inputs.

### 8B.7 — Observe-Only Anomaly Detection
Use canonical anomaly arrays under audit.stability and audit.drift to surface non-blocking runtime findings before any warning or enforcement semantics are introduced.

---

## Non-goals for the first Stage 8B pass

Do not attempt all of the following immediately:

- hard blocking in the live decision path
- broad engine rewrites
- universal topology tracking
- deep environment simulation
- full enforcement across all modules
- fully mature drift intelligence

The first pass is about making the concerns explicit and structurally present.

---

## Current conclusion

Stage 8B should be treated as the next governance-hardening tranche after the first orchestration milestone.

It should be built in a disciplined way:

- capture the concerns
- map them to real runtime objects
- instrument first
- enforce later

This preserves the integrity of the current spine while preparing Execalc for a more mature stability and drift governance layer.

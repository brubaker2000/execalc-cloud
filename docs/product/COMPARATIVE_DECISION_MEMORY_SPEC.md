# Comparative Decision Memory Specification (Stage 7)

Purpose:
- Turn Execalc from a single-run decision engine into a system that can compare, refine, and revisit prior decisions.
- Build the first real layer of executive memory on top of hardened decision envelopes and persistence.
- Expand cognition only where operational rails already exist.

Non-Goals (Stage 7):
- No Intelligent Front Door implementation yet.
- No broad UI work.
- No free-form historical chat memory as a substitute for governed decision artifacts.
- No uncontrolled cartridge explosion.
- No cross-tenant bridges or inter-subscriber operability yet.

---

## 1) Stage 7 Scope

Stage 7 is divided into three sub-stages:

### 7A) Journal Hardening in Real Use
Purpose:
- Validate that decision envelopes function as durable executive memory artifacts in realistic workflows.

Goals:
- Confirm stored decisions can be reliably retrieved by envelope_id
- Confirm recent decision timelines are stable and tenant-scoped
- Confirm persistence-off, persistence-requested, and persistence-enabled behavior remains coherent
- Confirm the journal is usable as a comparison substrate, not merely storage

### 7B) `/decision/compare`
Purpose:
- Compare two or more decision artifacts and produce an executive-grade comparison report.

### 7C) Multi-Objective Comparison Logic
Purpose:
- Evaluate how judgment changes when the same scenario is run under different governing objectives.

---

## 2) Stage 7A — Journal Hardening Requirements

The journal layer must support:

- retrieval by envelope_id
- recent-decision listing by tenant
- stable audit metadata
- repeatable comparison input selection
- safe operation when persistence is disabled

Stage 7A should confirm that a decision artifact is usable as a durable memory unit with:
- scenario context
- governing objective
- report payload
- audit metadata
- retrieval handle

---

## 3) Stage 7B — `/decision/compare` Input Contract

A comparison request MUST provide:

- tenant_id (resolved via claims/request context; never trusted from body alone)
- one of:
  - envelope_ids: list of 2..N prior decision envelope IDs
  - OR a combination of:
    - one live scenario
    - one or more prior envelope IDs

Optional:
- comparison_objective: string
  - e.g. "best_current_option", "downside_control", "objective_drift"
- requested_depth: "brief" | "standard" | "deep" (default: standard)

Rules:
- all compared artifacts must belong to the same tenant
- comparison must fail closed on tenant mismatch
- envelope IDs must be validated before comparison proceeds
- comparison must not require persistence to be globally enabled if sufficient live inputs are supplied

---

## 4) Stage 7B — `/decision/compare` Output Contract

Execalc returns a structured Comparison Report containing:

A) Comparison Summary
- one-paragraph executive judgment comparing the candidate decisions

B) Decision Set
- identifiers of compared artifacts
- brief label for each option

C) What Changed
- key differences in facts, assumptions, or structure across compared decisions

D) What Stayed Constant
- stable factors across compared decisions

E) Trade-Off Shift Analysis
- how upside, downside, asymmetry, and key trade-offs differ by option

F) Governing Objective Alignment
- how well each option fits the stated comparison objective

G) Sensitivity and Fragility
- which decision is most sensitive to uncertain inputs
- which decision is most robust if assumptions break

H) Recommendation
- preferred option
- rationale
- conditions that would change the recommendation

I) Next Actions
- 3–7 sequenced next steps

J) Audit Metadata
- tenant_id
- compared_envelope_ids
- comparison_objective
- timestamp
- version

---

## 5) Stage 7C — Multi-Objective Comparison Rule

If the same scenario is compared across different governing objectives, Execalc must:

- preserve the original objective attached to each decision artifact
- avoid blending objectives unless explicitly instructed
- explain how recommendation shifts under each objective
- identify where objectives are compatible vs conflicting

Examples:
- cut_payroll
- maximize_upside
- downside_control
- preserve_optionality

The system should make objective drift visible rather than hiding it inside prose.

---

## 6) Decision Artifact Rule (Stage 7)

For Stage 7 purposes, a decision artifact is defined as:

- scenario context
- governing objective
- executive report
- audit metadata
- retrieval handle (envelope_id)

Comparative reasoning must operate on decision artifacts, not raw chat turns.

---

## 7) Stage 7 Implementation Rule

Stage 7 may begin with deterministic comparison logic, but MUST:

- preserve tenant isolation
- preserve stable response schema
- never invent missing prior-decision facts
- clearly distinguish known differences from inferred differences
- remain CI-safe without requiring live DB configuration for unit tests

---

## 8) Success Criteria

Stage 7 is successful when:

- the journal behaves like real executive memory
- `/decision/compare` produces stable structured output
- multi-objective comparisons visibly change judgment when objectives differ
- comparison artifacts are audit-safe and tenant-scoped
- the system becomes more cognitively useful without weakening operational rigor

# Decision Loop Engine Specification (Stage 4)

Purpose:
- Convert time-compressed scenario input into a repeatable executive-grade output structure.
- Enforce clarity, sensitivity disclosure, and constraint-driven reweighting (Polymorphia lens switch) without exposing internal mechanics.

Non-Goals (Stage 4A):
- No UI.
- No league-specific draft engine yet.
- No agent swarms.
- No “perfect” scoring. Stage 4A locks the interface + report shape.

---

## 1) Input Contract (Scenario Envelope)

A Decision Loop request MUST provide:

- tenant_id (resolved via claims/request context; never trusted from body alone)
- scenario:
  - scenario_type: string (e.g., "draft_trade", "cap_cut", "feasibility")
  - governing_objective: string (lens) (e.g., "maximize_WAR", "cut_payroll", "risk_reduction")
  - prompt: string (15-second natural language summary)
  - facts: object (optional structured facts)

Optional:
- constraints: object (caps, budgets, deadlines, guardrails)
- attachments: list (future)
- requested_depth: "brief" | "standard" | "deep" (default: standard)

---

## 2) Output Contract (Executive Report)

Execalc returns:

A) Executive Summary
- One-paragraph decision statement, no mechanics.

B) Confidence
- One of: "high", "medium", "low", "unknown"
- Rationale: short bullet list (why confidence is what it is)

C) Governing Objective
- Restated plainly (may be brief/implicit in language; but present in structure)

D) Trade-Off Table (structured bullets)
- Upside
- Downside
- Key trade-offs (2–5)
- Asymmetry notes (if any)

E) Sensitivity Variables (Missing or Uncertain Inputs)
- List of variables that could change the calculus
- For each: likely directional impact (e.g., "would increase downside risk", "could flip recommendation")

F) Next Actions
- 3–7 operational actions, sequenced

G) Audit Metadata (non-sensitive)
- tenant_id
- scenario_type
- governing_objective
- timestamp
- version
- envelope_id (request trace id)
- persist (best-effort persistence status + error detail when applicable)

---

## 3) Polymorphic Lens Switch Rule (Stage 4)

If governing_objective changes, Execalc must:
- Reweight trade-offs under the new objective
- Update confidence and sensitivity disclosure accordingly
- Avoid blending conflicting objectives unless explicitly instructed

---

## 4) Stage 4A Implementation Rule

Stage 4A may use deterministic placeholder logic, but MUST:
- Produce valid output structure every time
- Declare missing critical inputs
- Never hallucinate missing facts as known

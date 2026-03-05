# Intelligent Front Door (IFD) — Decision Logic Architecture (Spec)

Last updated: 2026-03-05
Status: SPEC ONLY (no runtime activation; no API surface yet)
Purpose: Preserve IFD architecture so current build work does not preclude viability.

## Positioning
IFD and Execalc are separate but interlocking products.

- IFD: perimeter triage for inbound submissions (porch → door → routed inside).
- Execalc: internal governed cognition and decision journal (house interior).

Interlock principle:
- IFD produces structured, auditable intake decisions.
- Execalc provides the governed intent (goals/risk/routing maps) and learns from outcomes over time.

## Governance Invariants
1. House isolation: no cross-tenant leakage.
2. Porch sovereignty: no duty to respond; default is ignore unless threshold clears.
3. Auditability: decisions must be explainable via controlled reason codes.
4. Fail-safe: uncertainty routes to intake steward / hold queue, not the 4th floor by default.

## Canonical Objects
IFD should be buildable around four canonical objects:

1) NormalizedPackage
2) ValueDecision
3) RoutingDecision
4) ActionBrief

These objects are designed to be journaled and later correlated with outcomes.

## Stage 1 — Package Normalization
Goal: Convert any inbound artifact into a standard internal representation.

Key steps:
- Channel normalization (email/web/API/etc.)
- Identity resolution (claimed vs best-effort verified signals)
- Content extraction (text + attachment index)
- Summarization (one-liner + short bullets)
- Coarse intent classification (Partnership / Sales / Investor / Hiring / Support / PR / Legal / Other)

Deliverable: NormalizedPackage

## Stage 2 — Value Detection (Fork)
Goal: Decide whether it is worth attention, and why.

Composite evaluation:
- Policy gate (hard reject rules)
- Goal alignment match (against house goals / initiatives)
- Credibility & quality signals
- Value hypothesis (explicit “why this might matter”)
- Composite signal score and fork:
  - Reject / Hold / Route / Escalate

Deliverable: ValueDecision

## Stage 3 — Organizational Routing
Goal: Route to correct ownership and floor.

Mechanism:
- Domain ownership resolver (CorpDev/Finance/Ops/Sales/HR/Legal/Comms/Support/General Intake)
- Floor selector (1–4) with escalation justifications
- Recipient selector + fallback

Deliverable: RoutingDecision

## Stage 4 — Executive Framing
Goal: Present the package so the recipient sees value quickly and can act.

Mechanism:
- Load recipient context (role/floor)
- Dovetail matcher (link to active initiatives and similar past cases)
- Floor-specific brief formatting:
  - 4th floor: 6-line max (summary, why it matters, risk flags, next step)
  - lower floors: more detail + taskability
- Suggested next action + optional draft reply

Deliverable: ActionBrief

## Decision Journal Integration (Future-Compatible)
Journal event types should allow (at minimum):
- decision_run (existing)
- front_door_intake (future)

Every meaningful triage action should be loggable:
- normalized intent
- signal score
- decision (Reject/Hold/Route/Escalate)
- reasons[]
- routing owner + floor
- brief format
- later: outcome codes (true/false positive/negative, meeting set, deal won/lost)

## Reason-Code Taxonomy (Controlled Vocabulary)
Format: IFD.<STAGE>.<GROUP>.<CODE>

Required usage rules:
- Every triage decision includes at least 1 value reason OR 1 reject reason.
- Routing includes exactly 1 owner reason.
- Escalations include 1 value reason + 1 urgency/impact reason.

Core groups:

Normalization (NORM)
- sender identity signals, extraction quality, intent classification

Value (VAL)
- goal match, value type, magnitude indicators, specificity/quality, credibility, timing, dovetail fit

Reject/Hold (REJ/HOLD)
- policy hard rejects, low-value/irrelevant, not-our-lane redirect, needs-more-info

Routing (ROUTE)
- owner selection, floor selection, escalation justifications

Brief (BRIEF)
- brief format, dovetail framing, suggested action

Outcome (OUTCOME)
- ignored/declined/responded/meeting-set/opportunity/deal-won/lost/false-positive/false-negative

## Build Accommodation (Do Not Preclude)
To keep IFD viable while continuing Stage 6:
- Do not hard-code “decision journal == only decision_run” anywhere.
- Keep persistence interfaces capable of storing generic “event_type + payload”.
- Avoid routing logic that assumes only internal decision endpoints.
- Prefer schema/design choices that can accept an additional event class later.

## Implementation Note
This document is intentionally non-code. It preserves architecture and vocabulary for later activation.

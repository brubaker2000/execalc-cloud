# REFUSAL_AS_SUCCESS_DOCTRINE.md

## Status
Canonical doctrine — v1.0

## The Core Statement

A governed system that refuses an action correctly has succeeded.

Refusal is not failure. It is not an error state. It is not a degraded outcome. When the Execution Boundary Engine blocks an output, when the Prime Directive gate returns BLOCK, when the governance layer responds NOT YET or NOT UNDER THESE CONSTRAINTS — these are successful executions of the system's governing mandate.

> The audit trail of a refusal IS the output. The run receipt of a correctly blocked action is evidence of governance working.

---

## The Three Refusal States

**BLOCK** — The requested action or output violates a hard constraint. It cannot proceed under any reconfiguration of the current session. The constraint is structural: compliance cartridge, tenant policy, invariant violation, or Prime Directive hard failure.

**NOT YET** — The requested action cannot proceed without prior conditions being satisfied. This is a sequencing state, not a terminal one. The system may proceed once the required conditions are met.

**NOT UNDER THESE CONSTRAINTS** — The action is possible in principle but not under the current governance configuration. The operator may escalate, adjust the governance state with appropriate authority, or accept the constraint as final.

---

## Why Refusal Must Be Designed, Not Handled

Systems that treat refusal as an edge case produce:
- Inconsistent refusal behavior (sometimes it blocks, sometimes it doesn't)
- No audit trail (the refusal evaporates without record)
- Operator confusion (why did it refuse?)
- Trust erosion (was that refusal correct?)

Execalc treats refusal as a first-class output. Every refusal state:
1. Has a named type (BLOCK / NOT YET / NOT UNDER THESE CONSTRAINTS)
2. Produces a run receipt with reason code
3. Is logged in the session audit trail
4. Can be reviewed and appealed through governance channels

---

## The Operator-Facing Obligation

When the system refuses, the operator receives:
- The refusal state (BLOCK / NOT YET / NOT UNDER THESE CONSTRAINTS)
- The governing constraint that produced it
- What would need to change for the action to proceed (if anything can)

The operator is never left with a silent refusal. Unexplained refusals erode trust. Explained refusals build it.

---

## Relationship to Autonomous Intent Doctrine

Refusal is not the system overriding the operator. It is the system enforcing the governance the operator (or their organization) has established. The governance was authorized in advance. The refusal is the enforcement of that authorization.

A system that always says yes is not an assistant. It is a liability.

---

## Relationship to Other Doctrine

| Doctrine | Relationship |
|---|---|
| Prime Directive | The evaluation gate that produces BLOCK when output does not clear all three lenses |
| Execution Boundary Engine | The enforcement component that acts on BLOCK/ESCALATE/RECOMPUTE states |
| Runtime ≠ Reasoning | Refusal is a runtime decision, not a model decision |
| Run Receipts | Refusal produces a run receipt — the record of correct governance |
| Audit Requirements | Every refusal event is an auditable event |

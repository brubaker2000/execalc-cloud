# RUNTIME_REASONING_SEPARATION.md

## Status
Canonical doctrine — v1.0

## The Distinction

**Reasoning** is what the LLM does. It is probabilistic, non-deterministic, and not directly auditable at the step level. Given identical inputs, it may produce different outputs. It is not a machine — it is an inference engine operating over language.

**Runtime** is what Execalc does. It is deterministic, governed, and auditable by construction. Given the same inputs under the same governance state, it produces the same structural outcome. It is a machine.

These two layers must never be confused or collapsed into each other.

> The LLM reasons. Execalc executes. Execution governs reasoning. Reasoning does not govern execution.

---

## Why This Matters

Systems that treat reasoning and execution as the same layer produce outputs that:
- Cannot be audited (the reasoning path is not traceable)
- Cannot be refused structurally (the model can always produce something)
- Cannot be trusted in regulated environments (no run receipt)
- Blur accountability (did the model decide, or did the system?)

Execalc is built on the separation. The runtime makes deterministic decisions about what the model is allowed to do, what context it receives, what it may output, and whether the output is allowed to proceed. The model reasons within that structure. It does not define the structure.

---

## The Four Enforcement Points

**1. Gates before reasoning**  
Deterministic checks fire before any LLM call: Is this operator authenticated? Is this tenant valid? Is this action permitted under current governance state? Is this input clear of compromise signals? Only after these gates clear does the model receive input.

**2. Context assembly**  
The runtime assembles what the model receives — scenario context, active carats, compliance constraints, operator memory, Prime Directive frame. The model does not self-navigate. It reasons within a prepared context.

**3. Output evaluation**  
The model's output does not reach the operator directly. The Prime Directive evaluation gate, the execution boundary engine, and the support stack operate on the output before delivery. BLOCK, ESCALATE, and RECOMPUTE are runtime states — not model states.

**4. Run receipts**  
Every governed request produces a run receipt: what logic fired, under what constraints, with what result. This is not logging for debugging. It is provability. Explainability is a narrative. Traceability is a record. Execalc commits to traceability.

---

## Corollary: Nothing Happens Because the Model Felt Like It

The model is invited to reason under constraints. It does not decide to act. It does not initiate. It does not choose what context it receives. It does not determine what is permitted.

Any behavior in Execalc that appears to originate from the model's autonomous judgment is a failure of the runtime layer to enforce its authority. The runtime controls the model. Not the reverse.

---

## Relationship to Other Doctrine

| Doctrine | Relationship |
|---|---|
| Prime Directive | The governance frame the runtime enforces before and after reasoning |
| Execution Boundary Engine | The component that applies runtime authority to model outputs |
| Run Receipts | The audit artifact that proves the runtime operated correctly |
| Refusal-as-Success | Runtime refusing is a valid successful outcome — not a model failure |
| Null Pathway | No reasoning is invoked when the situation does not call for it |

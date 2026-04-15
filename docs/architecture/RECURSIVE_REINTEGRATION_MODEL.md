# RECURSIVE_REINTEGRATION_MODEL.md

## Status
Draft v0.1

## Owner
Architecture / Core 7

## Position in Core 7
Framework 7 — The final framework; operates on the complete output after judgment, before delivery to the operator.

---

## What Recursive Reintegration Is

Recursive Reintegration is the Core 7 component that evaluates the system's own outputs against the governing logic that produced them — before those outputs reach the operator.

It is Framework 7 because it requires all preceding frameworks to have completed. It cannot evaluate whether an output is consistent with Polymorphia, the Prime Directive, and the EKE corpus until those frameworks have run. Framework 7 is the closing of the loop.

The question Recursive Reintegration answers is:

> **Does this output actually follow from the governing logic that produced it?**

---

## Why This Exists

An LLM can produce a fluent, confident, internally coherent recommendation that violates the governing framework at one or more points. The violation may be subtle — a conclusion that assumes an unexamined premise, a recommendation that favors one Prime Directive lens while ignoring another, a claim that contradicts an admitted memory unit without acknowledging the contradiction.

The system does not catch these violations at the judgment call stage because the model is reasoning forward, not looking back at its own output from the outside.

Recursive Reintegration is that external look. After the judgment call completes, a second evaluation pass reviews the complete output against:

1. The Prime Directive lenses that were active
2. The Polymorphia dimensional map that was generated
3. The EKE corpus entries that were loaded
4. The admitted memory units that were active
5. The active Carats and their constraints
6. The compliance cartridge constraints (if any)

Any output that passes judgment but fails reintegration does not reach the operator.

---

## Distinction from Runtime Validation Protocols

This distinction is critical and must not be blurred:

| Component | Where it operates | What it checks |
|---|---|---|
| Runtime Validation Protocols (Support Stack) | At each intermediate reasoning step | Does each step follow from the previous step within governing constraints? |
| Recursive Reintegration (Core 7, F7) | On the complete output | Does the final output follow from the full governing framework as a whole? |

Runtime Validation Protocols catch step-level errors during reasoning. Recursive Reintegration catches output-level errors after reasoning is complete. These are complementary, not redundant — a reasoning chain can have individually valid steps that produce an output that contradicts the governing framework when evaluated holistically.

---

## What Reintegration Checks

### Check 1: Prime Directive Alignment

All three Prime Directive lenses must be present and evaluated in the output. If the output makes a recommendation that implicitly evaluates one lens but omits the others, reintegration flags the omission.

- **Pass:** All three lenses appear; each is evaluated; the recommendation follows from their combined assessment.
- **Flag:** One or more lenses were loaded but do not appear in the output reasoning.
- **Block:** Recommendation contradicts an evaluated lens without acknowledging the contradiction.

---

### Check 2: Polymorphia Consistency

If Polymorphia identified multiple valid dimensions, the output must acknowledge the dominant dimension designation and not silently suppress the secondary dimensions.

- **Pass:** Dominant dimension reflected in output; secondary dimensions acknowledged or explicitly set aside with stated reasoning.
- **Flag:** Secondary dimensions identified by Polymorphia do not appear anywhere in the output.
- **Block:** Output makes claims inconsistent with the dominant dimension without explanation.

---

### Check 3: Memory Consistency

Active admitted memory units may contain governed claims that constrain what the output can validly assert. Reintegration checks whether the output contradicts any active memory unit.

- **Pass:** Output is consistent with all active admitted memory.
- **Flag:** Output asserts a claim that tensions an admitted memory unit without acknowledging the tension.
- **Block:** Output directly contradicts a Canonical-tier memory unit.

---

### Check 4: Corpus Anchor Integrity

EKE corpus entries loaded for this session make specific claims and set specific frameworks. If the output cites a corpus entry, that citation must be accurate. If the output draws a conclusion that conflicts with a loaded corpus entry without explaining why the framework was set aside, reintegration flags it.

---

### Check 5: Compliance Constraint Adherence

If compliance cartridges were active, every recommendation must be evaluated against their constraints. A recommendation that would pass Prime Directive but violate an active compliance cartridge is blocked.

---

## Reintegration Output

Recursive Reintegration does not rewrite the output. It produces a **reintegration verdict** that determines what happens next.

```
{
  "verdict": "pass" | "flag" | "block",
  "checks": {
    "prime_directive": { "result": "pass", "notes": null },
    "polymorphia": { "result": "flag", "notes": "Secondary dimension D2 not addressed in output" },
    "memory_consistency": { "result": "pass", "notes": null },
    "corpus_integrity": { "result": "pass", "notes": null },
    "compliance": { "result": "pass", "notes": null }
  },
  "required_revision": "Address or explicitly set aside secondary dimension D2 before delivery.",
  "operator_disclosure": true
}
```

**Verdict definitions:**
- **Pass** — output proceeds to operator as-is
- **Flag** — output proceeds to operator but the flag is disclosed; operator sees both the output and the reintegration note
- **Block** — output does not proceed; system surfaces the blocking issue and requests a revised judgment call

---

## Operator Disclosure

When reintegration returns `operator_disclosure: true`, the operator receives:

```
[REINTEGRATION NOTE]
This output was reviewed against governing logic and one item was flagged:
Secondary dimension (Market Maturation Reading, 61% confidence) was identified 
but not addressed in the recommendation.

The recommendation stands. You may wish to consider whether this alternative 
framing changes your read.
```

This is not a correction. It is governance transparency — the operator sees that the system reviewed its own output and what it found.

---

## What Reintegration Is Not

Reintegration is not a second opinion on the substance of the recommendation. It does not evaluate whether the recommendation is correct in the world. It evaluates whether the recommendation is consistent with the governing logic that was applied.

A recommendation can be incorrect and still pass reintegration. A recommendation can be correct and still fail reintegration if the governance framework was not properly applied.

**Reintegration governs process fidelity, not outcome accuracy.**

---

## Audit Requirements

Every reintegration cycle must produce an audit record containing:
- Session and judgment call reference
- All five check results with notes
- Overall verdict
- Whether operator disclosure was triggered
- Whether a block caused a revised judgment call and the result of that revision

---

## Design Principle

> Recursive Reintegration is the moment the system holds itself accountable.

Every other Core 7 framework operates on external input — it receives information and applies logic to it. Recursive Reintegration is the only framework that operates on the system's own output. It is the mechanism through which the system can be wrong in a governed way — catching its own drift before the operator ever sees it.

A system without Recursive Reintegration can only be wrong silently. A system with Recursive Reintegration is wrong visibly — and therefore correctable.

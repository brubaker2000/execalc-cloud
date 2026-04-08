# Execalc Qualitative Formula Library v0.1

## Purpose

This document defines the conceptual framework for a formula language for qualitative judgment.

It is a foundational design concept, not yet implemented at runtime.

---

## The Excel Analogy

Excel did not invent accounting or mathematics.

What Excel did was give business a **formula language** for quantitative analysis — a common vocabulary for expressing, combining, and applying numerical operations.

Before spreadsheets, quantitative analysis required specialized knowledge and manual calculation. After Excel, any business analyst could apply compound interest, pivot data, or model a financial scenario.

Execalc is building the equivalent for qualitative judgment.

> **Excel gave business a formula language for numbers.  
> Execalc aims to give business a formula language for judgment.**

---

## Core Thesis

Qualitative reasoning is not intrinsically unstructured. It is currently **unformalized**.

The operations performed by skilled executive thinkers — framing, weighing, corroborating, tracing assumptions, checking for conflict, synthesizing signal — are repeatable cognitive operations.

A formula library makes those operations nameable, callable, and composable.

---

## Formula Taxonomy

The library is organized into seven families.

### Signal Family
Operations that detect and count qualifying signal.

| Formula | Description |
|---|---|
| `NUGGET()` | Captures and classifies an atomic insight for potential admission |
| `SIGNAL()` | Identifies a material signal within a body of text or reasoning |
| `COUNT_SIGNAL()` | Counts distinct qualifying signals within a defined scope |
| `RECURRENCE()` | Detects how often a signal has appeared across sources or time |
| `ASYMMETRY()` | Surfaces a structural asymmetry in a signal or claim set |

### Interpretation Family
Operations that apply framing and examine assumptions.

| Formula | Description |
|---|---|
| `FRAME()` | Selects and activates a reasoning framework for a given situation |
| `ASSUME()` | Surfaces and labels assumptions embedded in a claim or analysis |
| `CLARIFY()` | Resolves ambiguity in a claim or scenario through structured questioning |

### Validation Family
Operations that test, challenge, and bound claims.

| Formula | Description |
|---|---|
| `CORROBORATE()` | Checks for independent confirmation of a claim |
| `CONFLICT()` | Detects contradiction between claims or between a claim and existing memory |
| `BOUNDARY()` | Defines the scope and limits within which a claim or conclusion applies |

### Retrieval Family
Operations that recall and compare from governed memory.

| Formula | Description |
|---|---|
| `MEMORY_LOOKUP()` | Retrieves relevant admitted memory for a given context or scenario |
| `PRECEDENT()` | Connects the current case to historical or analogous cases |
| `MAX_SIGNAL()` | Surfaces the highest-weight signal in a set |
| `MIN_SIGNAL()` | Surfaces the lowest-weight or weakest signal in a set |
| `MEDIAN_READ()` | Returns the central tendency signal from a weighted set |

### Decision Family
Operations that weigh options and produce decision-grade outputs.

| Formula | Description |
|---|---|
| `WEIGH()` | Applies structured weighting to competing claims or options |
| `TRADEOFF()` | Surfaces explicit tradeoffs between competing values or objectives |
| `DECIDE()` | Produces a governed, traceable decision output from available claims and frameworks |

### Governance Family
Operations that enforce admission, traceability, and escalation.

| Formula | Description |
|---|---|
| `ADMIT_MEMORY()` | Governs the admission of a candidate into persistent memory |
| `REVISE()` | Updates an existing claim with lineage preserved |
| `TRACE()` | Reconstructs the decision lineage from output back to admitted claims and frameworks |
| `ESCALATE()` | Flags an issue, decision, or claim for elevated review |

### Synthesis Family
Operations that combine signal into executive-grade output.

| Formula | Description |
|---|---|
| `SYNTHESIZE()` | Combines admitted claims, activated frameworks, and governing logic into structured executive output |

---

## Composability

The power of a formula library is not in individual operations — it is in composition.

Example chains:

**Signal-to-Decision path:**
```
SIGNAL() → CORROBORATE() → WEIGH() → DECIDE() → TRACE()
```

**Memory-to-Frame path:**
```
MEMORY_LOOKUP() → PRECEDENT() → FRAME() → SYNTHESIZE()
```

**Admission path:**
```
NUGGET() → CONFLICT() → ASSUME() → ADMIT_MEMORY()
```

**Governance path:**
```
DECIDE() → TRACE() → ESCALATE() → REVISE()
```

---

## Design Principles

1. **Every formula should be expressible as a governed cognitive operation.**  
   If it cannot be described as a discrete, repeatable act, it does not belong in the library.

2. **Formulas should be composable.**  
   The output of one formula should be usable as input to another.

3. **Formulas should carry traceability.**  
   Every formula invocation should record what inputs it used, what logic it applied, and what output it produced.

4. **The library is not closed.**  
   v0.1 is a founding set. New formulas may be added through deliberate versioned addition — not ad hoc expansion.

5. **Formula names should be self-describing.**  
   A formula should communicate its purpose clearly to any reader without requiring documentation.

---

## Implementation Status

v0.1 is a **conceptual framework**, not yet implemented at runtime.

The formula library represents a future build stage. It will require:
- a formula execution engine
- integration with the memory system
- integration with the EKE corpus
- integration with the decision loop
- a governed formula registry

Current build work (Stages 4–8) is building the substrate on which the formula library will operate.

---

## Relationship to GAQP

The formula library is the operational expression of GAQP principles.

| GAQP Principle | Primary Formula(s) |
|---|---|
| Materiality | `SIGNAL()`, `NUGGET()`, `WEIGH()` |
| Traceability | `TRACE()`, `ADMIT_MEMORY()` |
| Authenticity | `CLARIFY()`, `ASSUME()` |
| Context | `FRAME()`, `MEMORY_LOOKUP()` |
| Separation of Observation/Interpretation | `NUGGET()`, `SIGNAL()` |
| Corroboration | `CORROBORATE()`, `RECURRENCE()` |
| Explicit Assumptions | `ASSUME()`, `BOUNDARY()` |
| Revision | `REVISE()` |
| Governed Memory Admission | `ADMIT_MEMORY()` |
| Reconstructable Decision Lineage | `TRACE()`, `DECIDE()` |

---

## Thesis

The formula library is the interface layer between governed reasoning doctrine and executable cognition.

It makes qualitative operations as nameable and repeatable as quantitative ones.

That is not a minor improvement to how organizations think. It is a structural shift in what is possible.

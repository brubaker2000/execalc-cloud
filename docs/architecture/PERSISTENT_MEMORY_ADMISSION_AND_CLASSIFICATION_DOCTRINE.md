# Persistent Memory Admission and Classification Doctrine

## Purpose

This doctrine defines the governed rules by which qualitative findings become durable memory inside Execalc and how admitted memory is classified for future retrieval, activation, and use.

This doctrine begins from a critical separation:

> **Journaling is not memory.**

The existence of a runtime artifact, decision record, conversation, or document does not automatically justify durable memory admission. Memory admission is a separate governed act.

---

## Why This Doctrine Exists

Without an admission doctrine, systems drift toward one of two failures:

1. **Hoarding everything** — losing signal in the mass
2. **Remembering too little** — repeatedly relearning what was once known

Execalc must avoid both.

The goal is to preserve only what is materially useful to future judgment while keeping provenance, scope, activation, and sensitivity explicit.

---

## Admission Standard

A qualitative finding should be admitted into persistent memory only when it clears a minimum threshold across these dimensions:

### 1. Materiality
Does this matter to future judgment, decision framing, constraint handling, or strategic understanding?

### 2. Durability
Is this likely to remain useful beyond the immediate moment, or is it ephemeral?

### 3. Provenance Strength
Can we say where it came from, under what conditions it was produced, and why it was admitted?

### 4. Decision Relevance
Would future executive judgment improve if this were available at the right moment?

### 5. Corroboration or Recurrence
Is this a one-off remark, or a supported pattern?

### 6. Distinctiveness
Does this add new intelligence, or merely repeat existing stored memory?

### 7. Admissible Source Path
Did this arise through an allowed governed path such as operator-directed admission, a validated decision artifact, a curated framework-derived synthesis, or another approved source?

---

## Memory Admission Rule

A finding should be remembered when it is:
- material
- durable
- traceable
- decision-relevant

Corroboration, recurrence, and distinctiveness strengthen the case for admission but do not replace the core threshold.

---

## Memory Promotion Ladder

Not all memory enters the system at the same level.

Execalc should recognize a progression:

```
Observed → Candidate → Admitted → Weighted → Canonical
```

### Observed
A signal has been seen but not admitted.

### Candidate
A signal appears memory-worthy and awaits governed review.

### Admitted
The finding is accepted into persistent memory.

### Weighted
The finding has been assigned confidence, activation posture, and possible scope.

### Canonical
The finding is so durable and consequential that it becomes part of the operating intelligence of the system or tenant.

---

## Classification Taxonomy

Once admitted, memory must be classified explicitly.

### A. Memory Family

What kind of memory is this?

- conversational
- strategic
- decision
- knowledge
- organizational
- heuristic
- clarity
- constraint
- relationship

`precedent memory` maps to the `decision` family with appropriate provenance. `dissent or conflict memory` maps to `strategic` or `organizational` with conflict-flagged content. The runtime canonical family list is defined in `PERSISTENT_MEMORY_PHASE_1_RUNTIME_SPEC.md`.

### B. Source Kind

Where did it originate?

- operator input
- decision artifact
- framework-derived synthesis
- imported document
- observed pattern
- curated doctrine
- future approved source path

### C. Activation State

How live should this memory be?

- active
- dormant
- reference_only
- deferred
- disabled

The canonical activation state vocabulary and Phase 1 minimum lifecycle states are defined in `PERSISTENT_MEMORY_PHASE_1_RUNTIME_SPEC.md`.

### D. Scope

Who may use or be influenced by this memory?

- operator-only
- team
- tenant-wide
- restricted sub-scope
- cross-tenant prohibited by default

### E. Confidence

How strongly should it be trusted?

- unknown
- low
- medium
- high

### F. Time Horizon

How long should it matter?

- short-term
- medium-term
- long-lived
- canonical

### G. Sensitivity

How tightly controlled should it be?

- normal
- restricted
- highly sensitive

---

## Admission Output Requirements

Every admitted memory object should carry:

| Field | Description |
|---|---|
| `memory_id` | Unique identifier |
| `tenant_id` | Owning tenant namespace |
| `memory_family` | Classification from taxonomy above |
| `activation_state` | Current activation posture |
| `content` | The memory itself |
| `summary` | One-line summary |
| `provenance` | Source and admission path |
| `created_at` | Admission timestamp |
| `updated_at` | Last modification |
| `admission_reason` | Why this was admitted |

Where possible, also include:

- confidence
- distinctiveness notes
- revision triggers
- related memory links
- supersession status

---

## Governing Warnings

Execalc should explicitly avoid:

- automatic promotion of all runtime artifacts into memory
- memory admission without provenance
- collapsing journaling and memory into one concept
- letting stale memory remain active without review
- allowing low-confidence memory to behave like canon

---

## Relationship to the Six-Test Admission Filter

Memory admission at the Execalc level applies the Six-Test Admission Filter originally defined for governed claims:

1. Stand-alone — can it be understood without its originating conversation?
2. Disputability — is it a real claim, not a truism?
3. Governance — does it fall within a recognized claim type?
4. Activation — would it change a future decision?
5. Durability — will it remain relevant beyond this session?
6. Composability — can it combine with other memory to form higher-order reasoning?

All six tests strengthen the admission case. Memory that fails multiple tests should not be admitted.

---

## Relationship to Runtime Spec

This doctrine defines the governance philosophy and admission criteria. The runtime implementation contract — object model, service seam, storage table, lifecycle rules, and TypeScript types — is defined in `PERSISTENT_MEMORY_PHASE_1_RUNTIME_SPEC.md`.

---

## Thesis

Memory should not be treated as storage. It should be treated as governed future utility.

The admission question is: **Should this live?**

The classification question is: **What kind of memory is it, how live is it, and how should it behave later?**

These are separate questions and must be answered separately.

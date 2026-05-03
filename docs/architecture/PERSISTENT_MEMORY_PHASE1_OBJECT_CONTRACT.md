# Persistent Memory Phase 1 Object Contract

Status: Canonical phase-1 contract draft  
Purpose: Define the first governed memory object for Phase 1 implementation without widening into runtime memory behavior.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md`
- `src/service/execution_record.py`

---

## Why this document exists

The broad memory architecture now defines what governed persistent memory is.
The Phase 1 attachment map now defines where the first memory layer should attach.

The next smallest useful artifact is the first explicit object contract that sits between those two documents.

This document exists to define the first Phase 1 memory object clearly enough that:
- developers do not stretch `ExecutionRecord` into informal memory
- a later memory service seam has a stable object to work with
- Phase 1 stays narrow, auditable, and tenant-scoped

---

## Phase 1 contract intent

Phase 1 does not need every future memory family or lifecycle feature.
It needs one clear governed object that can be admitted beside the current decision journal.

This object is the first canonical persistent-memory unit for Phase 1.

It is:
- separate from `ExecutionRecord`
- tenant-scoped
- provenance-carrying
- activation-state-aware
- suitable for explicit admission and narrow retrieval

It is not:
- the full future memory system
- an automatic promotion of every journaled artifact
- a search/ranking object
- an excuse for ad hoc runtime writes

---

## Canonical Phase 1 object shape

A Phase 1 memory object should include these required fields:

- `memory_id`
  - stable identifier for the admitted memory object

- `tenant_id`
  - ownership boundary for storage and retrieval

- `memory_family`
  - governed memory category for the object
  - **GAQP alignment required before implementation:** the current family list (conversational, strategic, decision, knowledge, organizational, heuristic, clarity, constraint, relationship) was designed before GAQP was canonized. This field must be reconciled with the 24 GAQP canonical claim types before any implementation begins. A memory object admitted to the corpus is a governed claim; its classification must come from the GAQP taxonomy, not from a parallel memory-specific hierarchy. The two taxonomies must not coexist — one must subsume the other. Resolution: Stage 9 GAQP data model work should produce a `claim_type` field that replaces or governs `memory_family` here.

- `activation_state`
  - governed state controlling retrieval eligibility and runtime influence posture

- `content`
  - substantive memory payload

- `summary`
  - short executive-readable description of why the memory matters

- `provenance`
  - source, admission context, and attribution data

- `created_at`
  - admission timestamp

- `updated_at`
  - latest governed modification timestamp

---

## Phase 1 provenance minimum

For Phase 1, provenance should be explicit enough to answer:

- who or what originated this memory
- from which surface or path it came
- when it was admitted
- whether it came from a decision artifact, operator input, or another governed source

At minimum, the provenance structure should be able to carry:

- `source_kind`
- `source_ref`
- `actor_id`
- `origin_surface`
- `admitted_by`
- `admission_reason`

When the source is a decision artifact, `source_ref` should be able to point back to the journaled source object, such as an envelope identifier.

---

## Optional Phase 1 fields

Phase 1 may also include optional fields when they add clarity without widening scope:

- `confidence`
  - trust or certainty posture when applicable

- `related_memory_ids`
  - links to nearby memory objects when the relationship is explicit

- `supersedes`
  - reference to an older memory object that this one narrows or replaces

These fields should remain optional in Phase 1 so the object contract stays narrow.

---

## Relationship to the decision journal

The Phase 1 memory object is not the journal record.

The journal remains the persisted execution artifact.
The memory object is a separate admitted object that may reference a journaled source.

That distinction must remain visible in the contract itself.

This means:
- `memory_id` must be distinct from `envelope_id`
- source provenance may point to a journal artifact
- admission into memory is a separate governed act from journal persistence

---

## Phase 1 guardrails

This contract should protect against four common mistakes:

1. turning `ExecutionRecord` into informal memory
2. letting memory objects exist without provenance
3. allowing ambiguous tenant ownership
4. blurring retrieval eligibility with automatic runtime influence

If the object contract does not prevent those mistakes, it is too loose for Phase 1.

---

## Explicitly out of scope for this document

This document does not define:

- the memory service API
- automatic promotion rules
- semantic retrieval or ranking behavior
- broad lifecycle automation
- cross-tenant behavior
- heuristic extraction logic

Those belong in later artifacts.

---

## Developer net line

**The next Phase 1 step after the attachment map is to define one explicit, tenant-scoped, provenance-carrying memory object that is clearly separate from the decision journal and stable enough for a later governed memory service seam.**

# Persistent Memory Phase 1 Admission Path

Status: Canonical phase-1 admission-path draft  
Purpose: Define how a Phase 1 memory object is explicitly admitted through governed paths without widening into automatic runtime memory behavior.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_PERSISTENCE_PATH.md`

---

## Why this document exists

The memory architecture now defines what governed persistent memory is.

The attachment map defines where Phase 1 memory should attach.

The object contract defines the first canonical Phase 1 memory object.

The service seam defines the governed boundary for admitting and retrieving that object.

The persistence path defines where that object should be stored.

The next smallest useful artifact is the admission path that explains how a valid memory object moves from governed request to admitted memory state.

---

## Admission-path intent

Phase 1 memory admission should be explicit, governed, and narrow.

A memory object should not become persistent memory merely because:
- a decision was executed
- a journal record exists
- a runtime artifact was generated
- a developer finds the content strategically interesting

Admission in Phase 1 should be a separate governed act.

---

## Recommended admission posture

The safest Phase 1 admission posture is:

governed caller or admission request  
-> memory service seam  
-> memory persistence path  
-> admitted memory object

That posture matters because it prevents:
- silent promotion from journal to memory
- ad hoc writes from arbitrary runtime code
- provenance loss between request and storage
- tenant ambiguity at the point of admission

---

## Minimum admission requirements

Before a Phase 1 memory object is admitted, the admission path should require:

- a valid tenant scope
- a valid Phase 1 memory-object shape
- minimum provenance fields
- an allowed activation state
- an explicit reason for admission

If those conditions are not met, the object should not be admitted.

---

## Allowed Phase 1 admission sources

A Phase 1 memory object may originate from governed sources such as:

- an operator-directed admission request
- a decision artifact explicitly selected for admission
- another governed source path that supplies the full Phase 1 object contract

Phase 1 should not assume that every potentially useful artifact is automatically eligible for admission.

---

## Relationship to the current decision journal

The decision journal may provide source material for admission, but it is not itself the admission path.

That means:
- a journal record may be referenced in provenance
- journal persistence should remain separate from memory admission
- admitting memory from a journaled artifact should still require a separate governed admission step

This protects the boundary between:
- execution record
- journal record
- admitted memory object

---

## Explicitly out of scope in Phase 1

The Phase 1 admission path should not yet define:

- automatic journal-to-memory promotion
- broad heuristic harvesting
- semantic discovery logic
- ranking or retrieval scoring
- cross-tenant admission
- runtime behavior changes triggered automatically by admission
- lifecycle automation beyond basic Phase 1 admission

Those belong later.

---

## Developer net line

**After defining the memory object, service seam, and persistence path, the next foundation step is an explicit admission path that makes memory entry a governed act rather than an automatic side effect of runtime or journal activity.**


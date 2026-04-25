# Persistent Memory Phase 1 Lifecycle Policy

Status: Canonical phase-1 lifecycle-policy draft  
Purpose: Define the narrow lifecycle rules for Phase 1 memory objects without widening into autonomous memory management or broad automation.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ADMISSION_PATH.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_RETRIEVAL_PATH.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ACCESS_POLICY.md`

---

## Why this document exists

The memory architecture now defines what governed persistent memory is.

The admission, retrieval, and access documents define how memory enters, is read, and is controlled in Phase 1.

The next smallest useful artifact is the lifecycle policy that defines the narrow allowed state changes for Phase 1 memory objects.

---

## Lifecycle-policy intent

Phase 1 memory lifecycle should be explicit, governed, and narrow.

A memory object should not automatically change state merely because:
- it exists in storage
- it has been retrieved recently
- a related runtime artifact changed
- a caller considers it stale or strategically inconvenient

Phase 1 lifecycle changes should occur only through governed state transitions.

---

## Narrow Phase 1 lifecycle posture

The safest Phase 1 lifecycle posture is:

- admit once through a governed path
- allow narrow governed status changes only if explicitly defined
- avoid broad in-place mutation of memory content in Phase 1
- avoid automatic retirement or deletion behavior

This keeps Phase 1 memory predictable, auditable, and easy to reason about.

---

## Minimum Phase 1 lifecycle states

At minimum, a Phase 1 memory object should support a narrow lifecycle such as:

1. **Admitted**
   - the object has entered governed persistent state

2. **Active**
   - the object remains eligible for governed retrieval

3. **Disabled**
   - the object remains preserved but is no longer eligible for normal retrieval paths

Phase 1 should avoid a larger state machine unless explicitly required.

---

## Minimum Phase 1 lifecycle rules

At minimum, the lifecycle policy should enforce:

- no cross-tenant lifecycle changes
- no automatic deletion in Phase 1
- no broad content rewriting after admission
- disabled objects remain auditable even when normal retrieval is blocked
- lifecycle changes must occur through explicit governed actions

If a caller cannot satisfy those rules, the lifecycle change should be refused.

---

## Relationship to access policy

The lifecycle policy depends on the same governed access boundary already defined for Phase 1 memory.

That means:
- access policy decides who may attempt a lifecycle operation
- lifecycle policy decides which narrow state changes are allowed
- retrieval behavior should respect lifecycle state where applicable

---

## Explicitly out of scope in Phase 1

The Phase 1 lifecycle policy should not yet define:

- automatic deletion workflows
- autonomous lifecycle transitions
- broad content rewriting after admission
- heuristic-driven retirement logic
- cross-tenant lifecycle delegation
- background lifecycle automation beyond explicit governed actions

Those belong later.

---

## Developer net line

**After defining what memory is, how it is admitted, retrieved, accessed, and state-limited, the next foundation step is a narrow lifecycle policy that keeps Phase 1 memory governable without turning it into an autonomous memory-management system.**

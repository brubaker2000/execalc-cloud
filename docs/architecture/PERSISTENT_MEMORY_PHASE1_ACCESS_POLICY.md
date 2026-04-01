# Persistent Memory Phase 1 Access Policy

Status: Canonical phase-1 access-policy draft  
Purpose: Define who and what may admit, read, and list Phase 1 memory objects without widening into runtime autonomy or cross-tenant access.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ADMISSION_PATH.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_RETRIEVAL_PATH.md`

---

## Why this document exists

The memory architecture now defines what governed persistent memory is.

The admission path defines how memory enters governed persistent state.

The retrieval path defines how memory is read back through governed paths.

The next smallest useful artifact is the access policy that defines which governed actors and request paths may perform those operations in Phase 1.

---

## Access-policy intent

Phase 1 memory access should be explicit, governed, and tenant-scoped.

A caller should not gain memory access merely because:
- it can read the decision journal
- it can invoke runtime code
- it can see a related artifact
- it is technically inside the same service boundary

Phase 1 access should be granted only through governed request paths.

---

## Phase 1 operation classes

The access policy should treat these as separate governed operations:

1. **Admit**
   - create a new governed memory object

2. **Get**
   - retrieve one memory object within tenant scope

3. **List**
   - retrieve a bounded tenant-scoped view of memory objects

A caller allowed to perform one operation should not automatically be allowed to perform the others.

---

## Baseline Phase 1 actor policy

In Phase 1, memory access should be limited to governed actor classes such as:

- authorized operator-facing request paths
- authorized admin or system-governed maintenance paths
- service-boundary code paths explicitly approved for memory operations

Phase 1 should not assume that every internal caller, helper, or adjacent service path may access memory.

---

## Minimum Phase 1 policy rules

At minimum, the Phase 1 access policy should enforce:

- strict tenant scope on every memory operation
- explicit permission by operation class
- no implicit promotion of journal access into memory access
- no cross-tenant reads or writes
- no automatic runtime influence merely because a caller can retrieve memory

If a caller cannot satisfy those rules, the memory operation should be refused.

---

## Relationship to tenant isolation

Phase 1 memory access must preserve the same tenant-isolation posture already expected elsewhere in Execalc.

That means:
- admit operations must write only inside the caller's valid tenant scope
- get operations must read only inside the caller's valid tenant scope
- list operations must return only tenant-scoped results
- no shared fallback path should blur tenant boundaries

---

## Explicitly out of scope in Phase 1

The Phase 1 access policy should not yet define:

- semantic authorization logic
- automatic policy escalation from heuristic matches
- cross-tenant delegation
- broad role-mapping frameworks beyond the minimum governed actors
- runtime autonomy triggered by memory access
- policy inheritance from adjacent non-memory surfaces without explicit approval

Those belong later.

---

## Developer net line

**After defining how memory is admitted, stored, and retrieved, the next foundation step is an explicit access policy that limits Phase 1 memory operations to governed tenant-scoped actors and request paths.**


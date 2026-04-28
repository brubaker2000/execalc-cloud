# Persistent Memory Phase 1 Retrieval Path

Status: Canonical phase-1 retrieval-path draft  
Purpose: Define how Phase 1 memory objects are retrieved through governed paths without widening into semantic search or automatic runtime influence.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_PERSISTENCE_PATH.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ADMISSION_PATH.md`

---

## Why this document exists

The memory architecture now defines what governed persistent memory is.

The object contract defines the first canonical Phase 1 memory object.

The service seam defines the governed boundary for memory operations.

The persistence path defines where Phase 1 memory is stored.

The admission path defines how memory enters governed persistent state.

The next smallest useful artifact is the retrieval path that explains how a stored memory object is read back through governed paths in Phase 1.

---

## Retrieval-path intent

Phase 1 retrieval should be explicit, governed, and narrow.

A stored memory object should not automatically become active runtime influence merely because:
- it exists in persistent storage
- it was recently admitted
- it appears strategically useful
- it matches a loose resemblance to the current situation

Retrieval in Phase 1 should be a separate governed read path.

---

## Recommended retrieval posture

The safest Phase 1 retrieval posture is:

governed caller or retrieval request  
-> memory service seam  
-> memory persistence path  
-> retrieved memory object or bounded memory view

That posture matters because it prevents:
- direct raw reads from arbitrary runtime code
- bypass of tenant or provenance checks
- retrieval from silently becoming runtime activation
- broad search behavior from leaking into Phase 1

---

## Minimum retrieval modes

Phase 1 retrieval should stay narrow and deterministic.

A safe first-cut retrieval surface would support:

1. **Get one memory object by `memory_id`**
   - exact tenant-scoped retrieval

2. **List recent memory objects**
   - bounded tenant-scoped retrieval
   - minimal metadata view is acceptable in Phase 1

3. **Optional family-filtered list**
   - only if it remains simple and deterministic

Phase 1 retrieval should not widen into broad discovery behavior.

---

## Relationship to admission and persistence

The retrieval path depends on the same governed boundary already established for admission and persistence.

That means:
- admission decides what enters governed persistent state
- persistence decides where the admitted object is stored
- retrieval decides how that stored object may be read back out

This protects the boundary between:
- admission
- storage
- retrieval
- runtime influence

---

## Explicitly out of scope in Phase 1

The Phase 1 retrieval path should not yet define:

- semantic search
- ranking or retrieval scoring
- similarity matching
- cross-tenant retrieval
- automatic runtime activation from retrieved memory
- broad discovery workflows
- heuristic extraction during retrieval

Those belong later.

---

## Developer net line

**After defining how memory enters and is stored, the next foundation step is a governed retrieval path that allows narrow tenant-scoped reads without turning Phase 1 into a semantic search or automatic runtime-influence system.**

# Persistent Memory Phase 1 Persistence Path

Status: Canonical phase-1 persistence-path draft  
Purpose: Define where and how the Phase 1 memory service seam should persist and retrieve memory objects without widening into runtime memory behavior.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md`
- `src/service/db/postgres.py`

---

## Why this document exists

The memory architecture now defines what governed persistent memory is.

The attachment map defines where Phase 1 memory should attach.

The object contract defines the first canonical Phase 1 memory object.

The service seam defines the governed boundary for admitting and retrieving that object.

The next smallest useful artifact is the persistence path that sits beneath the service seam and beside the existing decision journal path.

---

## Persistence-path intent

Phase 1 memory persistence should be added beside the current decision journal path, not by mutating the journal into informal memory storage.

The persistence path should:
- remain tenant-scoped
- remain explicit
- remain auditable
- stay behind the governed memory service seam
- preserve a clear distinction between journal records and admitted memory objects

This means the persistence path should support:
- writing a canonical Phase 1 memory object
- reading a canonical Phase 1 memory object
- listing narrow tenant-scoped memory views
- tracing a memory object back to its provenance source when applicable

---

## Recommended storage posture

The safest Phase 1 storage posture is:

memory service seam  
-> dedicated persistence helper or module  
-> storage backend

That posture matters because it prevents:
- direct ad hoc writes from arbitrary runtime code
- journal and memory semantics from collapsing together
- tenant or provenance checks from being bypassed
- later backend evolution from forcing a redesign of the service seam

---

## Relationship to the current journal persistence path

The current decision journal persistence path should remain intact.

Phase 1 memory persistence should sit beside it, not inside it.

That means:
- `insert_execution_record` should remain the journal write path for execution records
- journal retrieval helpers should remain focused on journal records
- memory persistence should use its own helper surface, even if it initially shares the same backend technology

This protects the boundary between:
- execution record persistence
- journal retrieval
- admitted memory-object persistence

---

## Phase 1 persistence responsibilities

The persistence path beneath the memory service seam should support these responsibilities:

1. **Write one memory object**
   - persist a canonical Phase 1 memory object exactly once per admit operation

2. **Read one memory object**
   - retrieve a canonical Phase 1 memory object by `memory_id` within tenant scope

3. **List narrow tenant-scoped memory views**
   - support a bounded recent list without widening into discovery behavior

4. **Preserve provenance fields**
   - persist source and admission data without dropping required context

5. **Preserve audit legibility**
   - return enough structure that the service seam can explain what was stored and retrieved

---

## Explicitly out of scope in Phase 1

The Phase 1 persistence path should not yet define:

- semantic retrieval storage
- ranking indexes
- vector infrastructure
- automatic journal-to-memory promotion
- lifecycle automation beyond basic Phase 1 persistence
- cross-tenant storage paths
- runtime influence logic
- heuristic harvesting logic

Those belong later.

---

## Recommended helper surface

Beneath the Phase 1 memory service seam, the persistence helper should remain narrow.

A safe first-cut helper surface would support operations equivalent to:

- `insert_memory_object`
- `get_memory_object`
- `list_memory_objects`

That helper surface should:
- remain tenant-scoped by default
- accept canonical memory-object data rather than ad hoc blobs
- return predictable structures the service seam can explain
- stay clearly separate from journal helpers such as `insert_execution_record`

The goal is not to finalize method names today.
The goal is to preserve the architectural boundary so developers know a separate persistence helper is required.

---

## Developer net line

**After defining the Phase 1 memory object and service seam, the next foundation step is a separate tenant-scoped persistence path that stores admitted memory objects beside the existing decision journal rather than inside it.**


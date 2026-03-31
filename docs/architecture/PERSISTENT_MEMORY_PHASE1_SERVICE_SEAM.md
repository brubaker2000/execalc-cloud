# Persistent Memory Phase 1 Service Seam

Status: Canonical phase-1 service-boundary draft  
Purpose: Define the first governed service seam for persistent memory without widening into runtime memory behavior.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md`
- `docs/architecture/PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md`
- `src/service/decision_loop/service.py`

---

## Why this document exists

The memory architecture now defines what governed persistent memory is.

The attachment map defines where Phase 1 memory should attach.

The object contract defines the first canonical Phase 1 memory object.

The next smallest useful artifact is the governed service seam that will sit between callers and memory persistence.

---

## Service seam intent

Phase 1 memory should enter the system through a dedicated governed service seam.

That seam should be:
- explicit
- tenant-scoped
- provenance-aware
- narrow in responsibility
- auditable
- separate from the current decision journal service path

---

## Phase 1 responsibilities

The Phase 1 memory service seam should own these responsibilities:

1. **Admit memory**
   - accept a governed request to create a Phase 1 memory object
   - validate required fields
   - enforce tenant scope
   - preserve provenance
   - return a caller-ready result

2. **Retrieve memory**
   - fetch a specific memory object by identity within tenant scope
   - return a governed read shape rather than raw storage output

3. **List narrow memory views**
   - allow a simple tenant-scoped recent or bounded listing
   - keep retrieval intentionally narrow in Phase 1

4. **Reject invalid admission**
   - refuse malformed or under-specified memory writes
   - refuse ambiguous tenant ownership
   - refuse memory writes with missing provenance minimums

5. **Preserve auditability**
   - ensure a developer can inspect what was admitted and through which governed path it entered

---

## Explicitly out of scope in Phase 1

This first service seam should not yet define:

- semantic search
- ranking or retrieval scoring
- automatic promotion from journal to memory
- broad lifecycle automation
- heuristic extraction
- cross-tenant lookups
- runtime memory influence logic
- vector retrieval or embedding infrastructure

Those belong later.

---

## Phase 1 service-entry posture

The memory seam should follow the same design discipline already visible in the decision path:

caller or API  
-> governed memory service seam  
-> persistence abstraction

That posture matters because it:
- keeps runtime reasoning code free of storage leakage
- keeps memory writes inspectable
- keeps tenant and provenance checks centralized
- allows a later persistence backend to evolve without changing the surrounding contract

---

## Admission input shape

A Phase 1 admit operation should expect enough information to construct the memory object cleanly.

At minimum, the admission request should be able to carry:

- `tenant_id`
- `memory_family`
- `activation_state`
- `content`
- `summary`
- `provenance`

Optional fields may include:

- `confidence`
- `related_memory_ids`
- `supersedes`

The service seam should normalize and validate this request before any persistence occurs.

---

## Retrieval posture

Phase 1 retrieval should remain narrow.

Recommended first-cut retrieval modes:

1. **Get by memory_id**
   - tenant-scoped exact retrieval

2. **List recent memory objects**
   - tenant-scoped bounded list
   - minimal metadata view is acceptable in Phase 1

3. **Optional family filter**
   - only if it remains simple and deterministic

Phase 1 retrieval should not widen into semantic recall or broad discovery behavior.

---

## Relationship to the decision service

The decision service remains the governed seam for decision execution and journal persistence.

The memory service seam should sit beside it, not inside it.

That means:
- `run_decision_service` should not silently become a memory-admission service
- a decision artifact may become a source for later memory admission
- the admission itself should still pass through the dedicated memory seam

This protects the boundary between:
- execution artifact
- journal record
- admitted memory object

---

## Guardrails

A valid Phase 1 service seam should prevent these mistakes:

1. direct raw storage writes from arbitrary runtime code
2. memory admission without provenance
3. tenant ambiguity
4. silent journal-to-memory promotion
5. retrieval that automatically becomes runtime influence
6. widening Phase 1 into a search product before the seam is stable

If the seam does not prevent those mistakes, it is too loose.

---

## Developer net line

**After defining the Phase 1 memory object, the next foundation step is a dedicated governed memory service seam that admits and retrieves tenant-scoped memory explicitly, without collapsing memory into the existing decision journal path.**


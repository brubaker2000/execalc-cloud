# Persistent Memory Phase 1 Attachment Map

Status: Canonical implementation-mapping draft  
Purpose: Map Phase 1 Persistent Memory onto the current decision journal and service seams without widening into runtime implementation.

Related context:
- `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`
- `src/service/decision_loop/service.py`
- `src/service/db/postgres.py`
- `src/service/execution_record.py`

---

## Why this document exists

The Persistent Memory architecture now defines what governed memory should be.

Before implementation begins, Execalc needs a narrow map showing:
- what current components already act like an early memory spine
- what Phase 1 should reuse
- what Phase 1 should add
- what Phase 1 must explicitly defer

---

## Plain-English summary

Today, Execalc already stores decision outputs in a tenant-scoped journal.

That journal is useful, but it is not yet the full Persistent Memory system.

Phase 1 should treat the existing decision journal as an early memory spine and then add a separate, governed memory path beside it.

That means:
- do not rip out the current journal
- do not let ad hoc memory logic leak into runtime
- do define the first clean memory object and memory service seam
- do keep the first rollout narrow, explicit, and auditable

---

## Current attachment seams

Phase 1 Persistent Memory should attach to four seams that already exist in the system:

1. **Decision service seam**
   - `run_decision_service` is the current governed orchestration entrypoint.
   - It validates and normalizes scenario input, constructs the runtime `Scenario`, invokes the decision engine, assembles the `ExecutionRecord`, and calls the persistence abstraction.

2. **Execution record seam**
   - `ExecutionRecord` is the current immutable storage contract for one execution.
   - It contains tenant scope, envelope identity, result payload, and timestamp.
   - This is a useful journal contract, but it is smaller and narrower than a future canonical memory object.

3. **Journal persistence seam**
   - `insert_execution_record` is the current tenant-scoped journal write path.
   - `get_execution_record` and `list_execution_records` are the current tenant-scoped retrieval paths.
   - These functions already enforce the discipline that persisted records are retrieved by tenant-aware service calls rather than by ad hoc raw access from runtime code.

4. **Retrieval seam**
   - `get_decision_service` and `list_recent_decisions_service` already form a governed retrieval boundary above the storage helper.
   - This means Phase 1 memory should be attached through a comparable service boundary, not written as direct runtime/database coupling.

---

## What Phase 1 should reuse

Phase 1 should deliberately reuse the parts of the current system that already express good governance and tenant discipline:

1. **Tenant-scoped persistence discipline**
   - The current journal already persists by `tenant_id`.
   - Retrieval is already constrained by tenant-aware calls.
   - Phase 1 should inherit that same default posture for all memory objects.

2. **Governed service-entry posture**
   - Today, decision persistence is not called directly from arbitrary runtime locations.
   - It is reached through `run_decision_service`, which acts as a controlled orchestration seam.
   - Phase 1 memory should preserve this design principle by entering through a dedicated memory service boundary.

3. **Explicit contract discipline**
   - The current system already uses explicit runtime/storage contracts such as `Scenario` and `ExecutionRecord`.
   - Phase 1 should continue that pattern by introducing a clearly named canonical memory object rather than hiding memory semantics inside the existing decision journal record.

4. **Narrow retrieval patterns**
   - The current retrieval model is intentionally simple: get one item by identity, or list recent items for a tenant.
   - Phase 1 should begin with similarly narrow retrieval behavior so memory does not sprawl into premature search, promotion, or synthesis behavior.

5. **Audit-friendly rollout posture**
   - The current journal path is explicit enough to inspect, reason about, and test.
   - Phase 1 should reuse that same explicitness so memory admission and retrieval are understandable before more automated behavior is added.

---

## What Phase 1 should add

Phase 1 should add a new governed memory layer beside the current decision journal, not by stretching the journal until it informally becomes “memory.”

1. **A canonical memory object contract**
   - Phase 1 should define the first explicit memory object with its own identity, tenant scope, provenance, timestamps, activation state, and stored content.
   - This object should be separate from `ExecutionRecord`, even if some early memory entries are derived from decision outputs.

2. **A dedicated memory service boundary**
   - Memory admission and retrieval should have their own governed service seam.
   - This keeps memory behavior explicit and prevents direct database writes or hidden runtime coupling from becoming the default pattern.

3. **Explicit provenance on write**
   - Every Phase 1 memory object should record where it came from.
   - At minimum, that means being able to say whether the memory originated from a decision artifact, operator input, a future heuristic path, or another governed source.

4. **Activation-state support from day one**
   - Phase 1 should not treat memory as a flat bucket of stored text.
   - Even if the first rollout is narrow, memory objects should still support a governed state such as active, inactive, deferred, or similar lifecycle-ready status.

5. **A distinct admission path**
   - The system should be able to distinguish between “this was journaled” and “this was admitted into memory.”
   - That distinction is important because not every execution record automatically deserves promotion into persistent executive memory.

6. **Audit-ready memory operations**
   - Phase 1 should make memory writes and reads explicit enough that a developer or operator can inspect what was admitted, why it was admitted, and through which governed path it entered the system.

---

## What must remain out of scope in Phase 1

Phase 1 should stay intentionally narrow. The goal is to establish the first governed memory layer, not to quietly smuggle in the full future memory system.

1. **Automatic promotion from journal to memory**
   - Phase 1 should not assume that every decision artifact or execution record is automatically memory-worthy.
   - Admission should remain explicit and governed.

2. **Automatic heuristic extraction**
   - Phase 1 should not yet attempt to infer, harvest, or promote heuristics from arbitrary stored outputs.
   - That would widen the rollout from memory attachment into active synthesis logic.

3. **Cross-tenant or shared memory behavior**
   - Phase 1 memory must remain strictly tenant-scoped.
   - No shared pools, global memory overlays, or cross-tenant reuse behavior should be introduced here.

4. **Broad memory-driven runtime synthesis**
   - Phase 1 should not make runtime behavior silently depend on memory retrieval in new or implicit ways.
   - The first rollout is about establishing clean storage and service boundaries, not changing how the rest of the runtime reasons.

5. **Silent conversion of the decision journal into the full memory system**
   - The current execution journal should remain what it is: a tenant-scoped journal of decision outputs.
   - Phase 1 should sit beside it, not rename it into something larger than it currently is.

6. **Ad hoc database writes outside the future memory service**
   - Memory writes should not appear as one-off helper calls scattered across runtime paths.
   - Phase 1 should protect against that drift by requiring a dedicated memory service seam.

7. **Premature search, ranking, or semantic retrieval expansion**
   - Phase 1 should not widen into advanced retrieval, ranking logic, or vector-style search behavior.
   - Those may matter later, but they are not required to establish the first memory attachment layer safely.

---

## Recommended Phase 1 implementation posture

Phase 1 should be implemented as a narrow, governed attachment beside the current journal path.

1. **Build beside, not through**
   - Do not force the current `ExecutionRecord` path to impersonate the memory system.
   - Add a separate memory object and service seam beside the journal so both roles remain legible.

2. **Keep admission explicit**
   - Memory should be admitted through a deliberate governed operation.
   - Avoid “incidental memory” created merely because some payload happened to be persisted elsewhere.

3. **Preserve service-layer discipline**
   - The memory path should follow the same architectural posture already visible in the decision flow:
     API or caller -> governed service seam -> persistence abstraction.
   - This keeps memory logic inspectable and prevents storage behavior from leaking upward into runtime reasoning code.

4. **Start with minimal object families**
   - Phase 1 does not need to solve every future memory category.
   - It only needs the first canonical object and the first clean service path that can later be extended without rework.

5. **Design for future lifecycle control without implementing all of it now**
   - Activation state, provenance, and identity should exist from the start.
   - Broader lifecycle automation, promotion logic, and synthesis hooks should wait until the basic memory path is proven.

6. **Prefer auditable simplicity over cleverness**
   - A plain, explicit Phase 1 memory path is better than a more ambitious design that hides decisions behind convenience behavior.
   - Developers should be able to trace exactly how a memory object was admitted, stored, and retrieved.

7. **Treat the journal as predecessor infrastructure, not dead weight**
   - The current decision journal is not a mistake to be replaced.
   - It is useful predecessor infrastructure that should remain stable while the first memory layer is added beside it.

---

## Journal-to-memory relationship

The current decision journal and the future Phase 1 memory layer should be related, but they should not be collapsed into the same thing.

1. **The journal remains the execution record**
   - The decision journal exists to persist the outcome of governed executions.
   - It is the historical record of what the system produced for a tenant at a given moment.

2. **Memory becomes a governed selective layer**
   - Persistent Memory is not the same as “everything that was ever journaled.”
   - It is a narrower, governed layer containing items that have been explicitly admitted into memory.

3. **A journal entry may become a memory source**
   - Some Phase 1 memory objects may be derived from decision artifacts already stored in the journal.
   - But the journal entry is still the source artifact, while the memory object is a separate admitted object with its own contract and lifecycle.

4. **Not every journaled artifact should become memory**
   - Many execution results will be useful as records without deserving long-lived executive memory status.
   - This is why Phase 1 must preserve a distinction between persistence and admission.

5. **The journal gives Phase 1 a safe attachment point**
   - Because the journal is already tenant-scoped, governed, and auditable, it gives Phase 1 a safe place to attach the first memory path.
   - That attachment should reuse the journal’s discipline without pretending the journal already is the memory system.

6. **The two layers should remain explainable to developers**
   - A developer should be able to answer two different questions:
     - “What execution artifacts were persisted?”
     - “Which of those, if any, were explicitly admitted into memory?”
   - If those questions blur together, the Phase 1 boundary has been drawn too loosely.

---

## Enterprise-grade safety checks for Phase 1

Phase 1 should be considered safe only if the first memory layer preserves the same discipline already expected from the rest of Execalc’s governed architecture.

1. **Tenant isolation must remain absolute**
   - Every memory object, admission path, and retrieval path must remain explicitly tenant-scoped.
   - Phase 1 should not introduce any ambiguity about who owns a memory object or who may retrieve it.

2. **Admission must be explainable**
   - It should always be possible to inspect why a memory object exists.
   - If a developer cannot trace the admission reason and source path, the design is too implicit for Phase 1.

3. **Retrieval must remain narrow and governed**
   - Memory retrieval should not become a loose helper utility callable from anywhere.
   - It should remain behind a dedicated governed service boundary.

4. **The journal must remain stable while memory is added**
   - Adding Phase 1 memory should not destabilize the current execution journal behavior.
   - Existing decision persistence and retrieval should continue to function as their own bounded layer.

5. **Phase 1 must not create hidden runtime dependence**
   - The rest of the runtime should not quietly begin to depend on memory in undocumented ways.
   - If memory changes behavior elsewhere, that dependency should be explicit and governed.

6. **Object boundaries must remain legible**
   - Developers should be able to distinguish clearly between:
     - execution artifact
     - journal record
     - memory object
   - If those categories become interchangeable in practice, Phase 1 has lost architectural clarity.

7. **The rollout should be testable in small pieces**
   - Phase 1 should be implementable and verifiable through narrow seams:
     - object contract
     - service boundary
     - persistence path
     - retrieval path
   - This is the safest enterprise posture because each layer can be validated without widening the runtime blast radius.

---

## Developer net line

If a developer needs one sentence to guide implementation, it is this:

**Phase 1 Persistent Memory should be built as a new governed layer beside the existing tenant-scoped decision journal, using its own canonical memory object and service boundary, while preserving explicit admission, strict tenant isolation, narrow retrieval, and full auditability.**


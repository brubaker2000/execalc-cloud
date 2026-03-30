# Persistent Memory System

Status: Canonical architecture draft  
Purpose: Define how Execalc stores, classifies, governs, and retrieves memory beyond ephemeral chat.

---

## Why this exists

Chat remembers the conversation.  
Execalc must remember the work.

Persistent Memory is not raw transcript accumulation. It is governed executive memory designed to preserve what matters, why it matters, and when it should influence future runtime behavior.

---

## Core principles

- Memory writes are explicit, deliberate operations.
- Memory is tenant-scoped and actor-attributed.
- Provenance is mandatory.
- Memory stores structured executive objects, not just text blobs.
- Clarity qualifies as value and may justify memory admission.
- Private or tenant memory never becomes global runtime logic by accident.
- Not all memory should influence runtime immediately.


---

## Memory object families

Execalc memory may include:

- conversational memory
- strategic memory
- decision memory
- knowledge memory
- organizational memory
- heuristic memory
- clarity memory
- constraint memory
- relationship memory

These are categories of governed executive memory, not merely storage buckets.


---

## Memory activation states

Stored memory and runtime-active memory are not the same thing.

Every memory object should carry an activation state so Execalc knows whether the object is merely retained, available for retrieval, or allowed to influence live reasoning.

Canonical activation states:

- `active`
  - Eligible to influence governed runtime behavior when relevant.
  - May participate in retrieval, synthesis, and downstream decision support.

- `deferred`
  - Stored intentionally but not yet promoted into active runtime influence.
  - Available for later review, upgrade, or formal admission.

- `reference_only`
  - Retained for context, audit, or historical lookup.
  - May be retrieved for inspection but should not shape live reasoning by default.

- `dormant`
  - Stored and recallable, but explicitly fenced from reflex influence or automatic activation until promoted.
  - Used when memory should be preserved without contaminating runtime behavior.

These states are governance controls, not mere labels.
They determine whether a memory object can affect execution, retrieval priority, or live synthesis.


---

## Memory admission rules

Not every useful sentence deserves permanent storage.
Memory admission should be governed by whether the object has lasting executive value, operational relevance, or future retrieval importance.

A memory object may be admitted when one or more of the following are true:

- it captures a durable strategic objective
- it records a meaningful decision or decision rationale
- it preserves a constraint that should shape future behavior
- it stores a reusable heuristic or pattern
- it captures organizational context needed across sessions
- it preserves clarity that would otherwise be lost and is likely to matter again

A memory object should usually not be admitted when:

- it is merely conversational filler
- it is transient and unlikely to matter beyond the current exchange
- it duplicates an already admitted memory object without adding meaning
- it has unclear provenance or weak executive value

Admission is a governed act, not passive accumulation.


---

## Provenance and attribution

No persistent memory object should exist without traceable origin.
Execalc must know who created the memory, where it came from, and under what context it was admitted.

Every admitted memory object should carry provenance such as:

- tenant identifier
- actor or source identifier
- originating surface or system
- timestamp of admission
- memory family classification
- activation state
- confidence or trust posture when applicable

Provenance is not metadata garnish.
It is what prevents private memory from becoming ungoverned runtime influence and allows later audit, correction, or promotion.


---

## Retrieval and runtime influence

Retrieval is not the same thing as runtime influence.
A memory object may be found, inspected, or quoted without automatically shaping live judgment.

Execalc should evaluate retrieved memory through at least these questions:

- Is the memory object still relevant to the present task?
- Is its activation state eligible for live influence?
- Does its provenance support trust in this context?
- Is the memory object more specific and useful than the current chat context alone?
- Would using it improve clarity, consistency, or decision quality?

Default rule:

- retrieved memory may inform runtime only when its state, provenance, and context all clear governance review
- dormant or reference_only memory may be surfaced for inspection without affecting live reasoning by default
- active memory may influence synthesis when relevance and trust are both satisfied

This keeps retrieval broad enough for recall while keeping runtime influence governed and deliberate.


---

## Memory lifecycle operations

Persistent memory should change state through governed operations, not silent mutation.

Canonical lifecycle operations include:

- `admit`
  - create a new governed memory object with provenance and activation state

- `promote`
  - move a memory object into stronger runtime influence, such as deferred to active or dormant to active

- `demote`
  - reduce runtime influence when a memory object should remain stored but no longer shape live reasoning as strongly

- `archive`
  - preserve the object for audit or history while removing it from normal retrieval priority

- `retire`
  - explicitly end operational use of a memory object while preserving provenance if policy requires

Lifecycle operations should be auditable and actor-attributed.
This prevents silent drift in what the system remembers and how that memory affects runtime behavior.


---

## Memory conflict and precedence

Not all admitted memory objects will agree with one another.
Execalc needs a governed way to resolve collisions without silently producing soup.

When memory objects conflict, precedence should usually follow this order:

- explicit current-operator instruction
- newer valid tenant-scoped memory over older tenant-scoped memory
- higher-confidence and better-provenanced memory over weaker memory
- active memory over deferred, dormant, or reference_only memory when runtime influence is at issue
- object-specific memory over broad general memory when both apply to the same decision

Conflict handling should not silently erase losing memory objects.
The losing object may still be retained for audit, historical review, or later reactivation.

If the conflict is material, Execalc should be able to surface the collision rather than pretending no conflict exists.


---

## Canonical memory object shape

Every persistent memory object should follow a minimum governed shape.
The exact storage schema may evolve, but the architectural contract should remain stable.

A canonical memory object should include fields such as:

- `memory_id`
  - stable identifier for the memory object

- `tenant_id`
  - tenant ownership boundary

- `memory_family`
  - one of the governed memory object families

- `activation_state`
  - active, deferred, reference_only, or dormant

- `content`
  - the substantive memory payload

- `summary`
  - short executive-readable description of why the memory matters

- `provenance`
  - attribution, source, surface, and admission context

- `confidence`
  - optional trust or certainty posture

- `created_at`
  - original admission timestamp

- `updated_at`
  - latest governed modification timestamp

- `supersedes`
  - optional reference to an older memory object replaced or narrowed by this one

- `related_memory_ids`
  - optional links to associated memory objects

This shape is intended to preserve governance, auditability, and future portability even if storage backends change.


---

## Memory service boundary

Persistent memory should not be manipulated through ad hoc table reads or scattered helper logic.
Execalc should expose memory through a governed service boundary so memory behavior stays consistent across chat, orchestration, decision, and future API surfaces.

Canonical service responsibilities should include:

- admit memory
- retrieve memory
- promote memory
- demote memory
- archive memory
- retire memory
- inspect memory history

That service boundary should enforce tenant scope, provenance requirements, activation-state rules, and audit logging.
This keeps persistent memory portable across storage backends while preventing silent bypass of governance.


---

## Initial implementation implications

The current decision journal should be treated as an early memory spine, not the full Persistent Memory system.

A practical first implementation should likely begin with:

- tenant-scoped storage of governed memory objects
- explicit admit and retrieve operations before broader lifecycle automation
- activation-state support from day one
- provenance fields required at write time
- audit logging for promotion, demotion, archive, and retire events

This allows Execalc to gain durable memory safely before attempting broader organization-level synthesis or automatic memory promotion.


---

## Security and tenant isolation guarantees

Persistent memory must obey the same hard tenant boundaries as the rest of Execalc.
A memory object admitted for one tenant must never be retrievable, influenceable, or inspectable by another tenant unless an explicit governed sharing model exists.

Minimum guarantees should include:

- tenant-scoped read and write enforcement
- actor-aware authorization before memory inspection or mutation
- no automatic promotion of private tenant memory into cross-tenant logic
- auditability for every memory lifecycle operation
- explicit governance before any future shared-memory or cross-organization model is introduced

Persistent memory is not only a convenience layer.
It is a trust surface and must be treated as part of Execalc's security architecture.


---

## Audit and observability

Persistent memory should be inspectable as a governed system, not treated as a black box.

At minimum, Execalc should be able to log and inspect:

- memory admission events
- promotion and demotion events
- archive and retire events
- retrieval events when policy requires traceability
- actor identity for each lifecycle operation
- before-and-after state for material changes

This allows operators, developers, and future auditors to understand not only what memory exists, but how it came to influence runtime behavior over time.


---

## Shared memory and cross-organization boundaries

Shared memory is not part of the default Persistent Memory model.
By default, all admitted memory is private to its tenant boundary unless an explicit governed sharing framework is introduced.

Any future shared-memory model should require at minimum:

- explicit operator or tenant authorization
- clearly defined scope of what may be shared
- provenance that preserves original ownership
- retrieval rules that prevent silent contamination of private runtime logic
- auditability for every shared-memory access event

Until such a framework exists, cross-tenant memory influence should be treated as prohibited.


---

## Governed memory write path

Persistent memory should enter the system through a governed write path, not by direct ad hoc persistence.

A canonical write path should look like:

1. candidate memory is identified
2. admission rules are evaluated
3. provenance and attribution are attached
4. activation state is assigned
5. canonical memory object is created
6. memory object is persisted through the memory service boundary
7. admission event is logged for audit and observability

This path keeps memory admission explicit, inspectable, and portable across future storage backends.


---

## Governed memory read path

Retrieval should follow a governed read path, not a raw fetch-and-inject pattern.

A canonical read path should look like:

1. runtime or operator requests memory
2. tenant scope and authorization are verified
3. relevant candidate memory objects are retrieved
4. activation state and provenance are evaluated
5. conflict and precedence rules are applied when needed
6. eligible memory is surfaced for inspection or allowed to influence runtime
7. retrieval event is logged when policy requires traceability

This path keeps recall useful without letting stored memory bypass governance on the way back into live reasoning.


---

## Promotion and review triggers

Lifecycle operations such as promote and demote should not happen arbitrarily.
Execalc should use governed triggers to decide when a memory object deserves stronger or weaker runtime influence.

Promotion may be justified when:

- a deferred memory object repeatedly proves relevant across sessions
- a stored heuristic demonstrates reusable executive value
- an operator explicitly promotes the memory object
- a previously reference_only object becomes operationally relevant

Demotion may be justified when:

- the memory object is still valid but no longer needs strong runtime influence
- a newer or better-governed memory object supersedes it
- the memory object should remain recallable without shaping live reasoning by default

Material promotion or demotion should be auditable and attributable.

---

## Failure posture and safe defaults

Persistent memory should fail safe, not fail open.
When governance conditions are uncertain, Execalc should prefer reduced memory influence over untrusted runtime contamination.

Safe defaults should include:

- if tenant scope cannot be verified, memory retrieval and mutation should be denied
- if provenance is missing or materially incomplete, the object should not be admitted as governed memory
- if activation state is unclear, the object should default to reference_only rather than active influence
- if conflict cannot be resolved confidently, the collision should be surfaced or influence withheld
- if the memory service is unavailable, runtime should continue without silent ad hoc persistence

It is better to lose a memory opportunity than to contaminate runtime behavior with ungoverned memory.

---

## Phased rollout

A practical rollout should happen in governed phases rather than as one large memory launch.

### Phase 1 — governed memory foundation
- canonical memory object shape
- tenant-scoped storage
- admit and retrieve operations
- provenance required on write
- activation-state support
- audit logging for writes and reads when policy requires it

### Phase 2 — controlled lifecycle expansion
- promote and demote operations
- archive and retire operations
- conflict and precedence handling
- operator-visible inspection history

### Phase 3 — broader synthesis support
- stronger retrieval strategies
- more deliberate heuristic reuse
- governed review workflows for promotion
- any future shared-memory model only after explicit governance approval

This sequencing keeps the first release safe, useful, and implementation-ready without overreaching.


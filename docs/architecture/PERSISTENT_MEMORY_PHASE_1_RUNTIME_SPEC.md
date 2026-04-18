# PERSISTENT_MEMORY_PHASE_1_RUNTIME_SPEC.md

## Status
Draft v0.1 — Phase 1 Runtime Contract

## Owner
Architecture / Core 7

## Position in Core 7
Framework 3 — Sits between MDL (Framework 2) and EKE (Framework 4). All admitted heuristics, governed claims, and decision artifacts are stored here. EKE draws from this store at query time.

---

## Purpose

This document defines the runtime implementation contract for Persistent Memory Phase 1. It is the developer-facing complement to `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md`, which covers the governance philosophy.

This spec defines: what the memory object looks like, how admission works, what the service seam exposes, what the storage table must support, and what lifecycle rules govern Phase 1.

---

## Phase 1 Posture: Build Beside, Not Through

The current `ExecutionRecord` / `execution_records` path remains the execution journal. Persistent Memory gets its own object model, service seam, storage table, access policy, admission path, retrieval path, and lifecycle policy.

The two questions must remain separately answerable:
- "What execution artifacts were persisted?"
- "Which artifacts were explicitly admitted into memory?"

These are not the same question. Phase 1 is the boundary between persisted and admitted.

---

## Phase 1 Non-Goals

Phase 1 is intentionally narrow. The following are explicitly excluded:

- Automatic promotion from execution journal to memory
- Autonomous lifecycle transitions
- Automatic deletion
- Heuristic-driven retirement
- Background automation of any kind
- Embeddings or vector columns
- Content versioning
- Multi-tenant visibility (cross-tenant reads)

This is a controlled first memory spine, not a full autonomous memory fabric.

---

## Canonical Object Model

Every memory object must carry stable identity, tenant scope, provenance, content, timestamps, and activation state.

```typescript
type ActivationStatus =
  | "active"
  | "dormant"
  | "reference_only"
  | "deferred"
  | "disabled";

type MemoryFamily =
  | "conversational"
  | "strategic"
  | "decision"
  | "knowledge"
  | "organizational"
  | "heuristic"
  | "clarity"
  | "constraint"
  | "relationship";

type Provenance = {
  source_type: "decision_artifact" | "operator_input" | string;
  source_id: string | null;
  admitted_via: string; // service path or policy route
};

type MemoryObject = {
  memory_id: string;              // stable global identity
  tenant_id: string;              // required on every operation
  family: MemoryFamily;           // object classification
  provenance: Provenance;         // source traceability
  content: Record<string, unknown> | string;
  created_at: string;             // source creation time if known
  admitted_at: string;            // time admitted into governed memory
  last_accessed_at?: string | null;
  activation_status: ActivationStatus;
};
```

---

## Object Families

The nine Phase 1 memory families cover the full range of memory Execalc is designed to carry:

| Family | What it holds |
|---|---|
| `conversational` | Memory extracted from session dialogue |
| `strategic` | High-level strategic conclusions and positions |
| `decision` | Records of governed decisions and their rationale |
| `knowledge` | Factual institutional knowledge |
| `organizational` | Organizational structure, constraints, and configuration |
| `heuristic` | Encoded operator heuristics (Heuristic Coding System entries) |
| `clarity` | Clarified framings, definitions, and resolved ambiguities |
| `constraint` | Binding constraints on decisions and actions |
| `relationship` | Counterparty, partner, and stakeholder knowledge |

The Heuristic Library (Framework 5) is a governed subset of the `heuristic` family within this store.

---

## Activation State vs. Lifecycle State

These are two distinct layers. Do not conflate them.

**Activation state** — the retrieval and control vocabulary for individual objects:
- `active` — eligible for normal retrieval and runtime activation
- `dormant` — stored; not eligible for runtime activation unless explicitly promoted
- `reference_only` — retrievable for audit and reference; does not activate in reasoning
- `deferred` — pending revalidation before re-activation
- `disabled` — deactivated; auditable but not retrievable in normal operations

**Phase 1 minimum lifecycle states** — the minimal set the Phase 1 policy enforces:
```
admitted → active → disabled
```

Phase 1 lifecycle control is intentionally simple. The object model reserves the richer activation vocabulary from day one, but Phase 1 policy enforces only the three-state minimum. Additional states are reserved and governed by doctrine as the system matures.

---

## Admission Rules

A Phase 1 object is admitted only when all of the following are true:

1. **Tenant scope is known and valid** — `tenant_id` is mandatory on every operation. No memory object exists outside tenant scope.
2. **Provenance is explicit** — the object must identify where it came from and how it was admitted.
3. **Family classification is explicit** — the system must know what kind of memory object it is creating.
4. **Content is stable enough to preserve** — Phase 1 is selective by design; not every execution artifact is memory-worthy.
5. **Activation status is assigned at creation** — activation-state support is part of the day-one contract.

The admission path is: **explicit validation → construction → storage → return identity**. "Persisted" is not equivalent to "admitted into memory."

---

## Admission Interface

```typescript
type AdmitMemoryRequest = {
  tenant_id: string;
  family: MemoryFamily;
  provenance: Provenance;
  content: Record<string, unknown> | string;
  requested_activation_status?: ActivationStatus; // default "active"
};

type AdmitMemoryResult = {
  memory_id: string;
  tenant_id: string;
  admitted_at: string;
  activation_status: ActivationStatus;
};
```

---

## Service Seam

Retrieval and mutation happen through the service seam, not through direct DB reads in business logic.

```typescript
admit_memory(request: AdmitMemoryRequest): AdmitMemoryResult

get_memory_object(
  tenant_id: string,
  memory_id: string
): MemoryObject | null

list_memory_objects(
  tenant_id: string,
  opts?: {
    family?: MemoryFamily;
    activation_status?: ActivationStatus[];
    limit?: number;
  }
): MemoryObject[]
```

---

## Phase 1 Mutation Endpoints

To keep lifecycle explicit and auditable, Phase 1 exposes narrow mutations rather than broad update semantics:

```typescript
disable_memory_object(
  tenant_id: string,
  memory_id: string,
  reason: string
): MemoryObject

activate_memory_object(
  tenant_id: string,
  memory_id: string
): MemoryObject
```

Do not implement a generic `update_memory_object()` in Phase 1. The policy is explicitly biased toward preservation, explicit state control, and minimal rewriting.

---

## Phase 1 Lifecycle Transition Rules

```typescript
type LifecycleTransition =
  | { from: "admitted"; to: "active" }
  | { from: "admitted"; to: "disabled" }
  | { from: "active"; to: "disabled" };
```

**Forbidden in Phase 1:**
- Autonomous state changes
- Timed expiration
- Background retirement jobs
- Destructive delete paths
- Large-scale post-admission content rewrites
- Heuristic-triggered demotion or promotion
- Cross-tenant lifecycle changes

Disabled objects are never deleted. They remain auditable.

---

## Storage Table Shape

Separate table from the execution journal. Minimum required columns:

| Column | Type | Notes |
|---|---|---|
| `memory_id` | `uuid` | Primary key |
| `tenant_id` | `text` | Indexed; required on every operation |
| `activation_status` | `text` | Indexed; default `'active'` |
| `family` | `text` | Indexed |
| `provenance` | `jsonb` | source_type, source_id, admitted_via |
| `content` | `jsonb` or `text` | The memory itself |
| `created_at` | `timestamptz` | Source creation time if known |
| `admitted_at` | `timestamptz` | Time admitted into governed memory |
| `last_accessed_at` | `timestamptz` | Nullable; updated on governed retrieval |

---

## Retrieval Rules

Default retrieval behavior is lifecycle-aware, tenant-scoped, and active-by-default:

1. Always require `tenant_id`
2. Default filter: `activation_status = 'active'`
3. Never cross tenant boundaries
4. Allow explicit inclusion of non-active states only through governed service options
5. Update `last_accessed_at` on successful governed retrieval
6. Disabled objects remain auditable but are not returned in default retrieval

---

## Access Policy

Tenant isolation is absolute. RBAC is enforced at the service seam.

- Every method requires `tenant_id`
- Authorization is checked before lifecycle mutation or broad retrieval
- Cross-tenant memory reads or writes are forbidden
- Lifecycle mutation must be explicit, logged, and policy-checked
- No caller bypasses the seam, even with direct database access elsewhere in the stack

---

## Audit Logging

Every admission, retrieval, and lifecycle mutation produces an audit record. Minimum log fields:

| Field | Description |
|---|---|
| `actor` | Who or what performed the operation |
| `tenant_id` | Owning tenant |
| `memory_id` | Object identity |
| `operation` | `admit`, `get`, `list`, `disable`, `activate` |
| `timestamp` | Operation time |
| `provenance` | Source metadata (on admission) |
| `result` | `success`, `denied`, `not_found` |

---

## Relationship to Governance Doctrine

This spec is the runtime expression of the governance doctrine in `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md`. The doctrine defines why admission works the way it does. This spec defines what it looks like in code.

The promotion ladder in the doctrine (Observed → Candidate → Admitted → Weighted → Canonical) maps to runtime objects as follows:

| Ladder State | Runtime Representation |
|---|---|
| Observed | Not yet in the system; noted in session context |
| Candidate | Flagged for admission; awaits `admit_memory` call |
| Admitted | `MemoryObject` with `activation_status: "active"` |
| Weighted | `MemoryObject` with confidence and scope metadata enriched |
| Canonical | High-confidence, high-scope entry; treated as governing doctrine |

---

## Note on Family Taxonomy Alignment

The Phase 1 families (`conversational`, `strategic`, `decision`, `knowledge`, `organizational`, `heuristic`, `clarity`, `constraint`, `relationship`) extend the governance doctrine's original taxonomy, which listed `precedent memory` and `dissent or conflict memory`. Those categories are valid governance concepts that map to the runtime families as follows:

- `precedent memory` → maps to `decision` family with appropriate provenance
- `dissent or conflict memory` → maps to `strategic` or `organizational` family with conflict-flagged content

The runtime families are the canonical set for Phase 1. The governance doctrine taxonomy should be updated to align with these families.

---

## Design Principle

> Persistent Memory Phase 1 is the boundary between "the system persisted something" and "the system decided this deserves durable institutional memory." That distinction is the product.

The near-term mandate: build the memory service seam, construct the memory object model, add the separate storage table, and enforce admission validation without disturbing the existing execution journal. The execution journal and the memory store answer different questions and must remain separately queryable.

# Persistent Executive Memory — V1.0 Build Specification

**Status:** Canonized — Build Directive  
**Version:** 1.0  
**Date:** 2026-05-20  
**Authority:** Execalc Product Standards

---

## I. Why This Document Exists

The Persistent Memory architecture has been defined across eight prior documents. The object contract, service seam, admission path, retrieval path, lifecycle policy, access policy, persistence path, and attachment map are all drafted.

PEM is still not built.

This document is not another architecture draft. It is a build directive. It answers one question: what do we implement now, in what order, to what definition of done, so that the upstream reasoning layer is no longer stateless.

Everything in this document is implementation-ready. Nothing here is speculative.

---

## II. The Problem This Solves

Every upstream reasoning capability — Prime Directive, Polymorphia, Executive Knowledge Engine, Qualitative Synthesis, Recursive Analysis — currently operates with no memory of prior sessions.

Each session starts from zero. Conclusions reached last week are invisible to reasoning today. Patterns confirmed across multiple sessions have no accumulated weight. Cartridges cannot improve from prior activations. The corpus grows but the reasoning layer cannot see it.

This is the blind man problem: the table is full and the system cannot find the sandwich.

PEM closes the loop. It gives the upstream reasoning layer access to what the organization has already concluded, confirmed, and canonized — across all prior sessions, under proper governance.

Without PEM, Execalc is a high-quality tool. With PEM, it becomes an institution that gets smarter every time it is used.

---

## III. Relationship to Existing Documents

This spec governs implementation. The following documents govern architecture and remain authoritative for anything not specified here:

| Document | Governs |
|---|---|
| `PERSISTENT_MEMORY_SYSTEM.md` | Full memory architecture, activation states, lifecycle operations, conflict rules, security |
| `PERSISTENT_MEMORY_PHASE1_OBJECT_CONTRACT.md` | Object shape and field definitions |
| `PERSISTENT_MEMORY_PHASE1_SERVICE_SEAM.md` | Service boundary responsibilities |
| `PERSISTENT_MEMORY_PHASE1_ADMISSION_PATH.md` | Admission rules and allowed sources |
| `PERSISTENT_MEMORY_PHASE1_RETRIEVAL_PATH.md` | Retrieval posture and modes |
| `PERSISTENT_MEMORY_PHASE1_PERSISTENCE_PATH.md` | Storage backend |
| `PERSISTENT_MEMORY_PHASE1_LIFECYCLE_POLICY.md` | Promote, demote, archive, retire |
| `PERSISTENT_MEMORY_PHASE1_ACCESS_POLICY.md` | Tenant isolation and authorization |
| `PERSISTENT_MEMORY_PHASE1_ATTACHMENT_MAP.md` | Where PEM attaches in the decision path |

Where this spec conflicts with those documents, this spec governs for V1.0 implementation. The architecture docs were written before GAQP was canonized; this spec resolves the resulting gaps.

---

## IV. The GAQP Alignment Resolution

The Phase 1 object contract flagged an unresolved conflict: the `memory_family` taxonomy (conversational, strategic, decision, knowledge, organizational, heuristic, clarity, constraint, relationship) was designed before GAQP was canonized. The 24 GAQP claim types now exist. Both cannot coexist as parallel classification systems for the same objects.

**Resolution for V1.0:**

Memory objects are divided into two classes:

**Class A — GAQP Claims**  
Any memory object that is a qualitative claim — an assertion, conclusion, doctrine, heuristic, observation, precedent, or any of the 24 canonical types — is classified by `claim_type` from the GAQP taxonomy, not by `memory_family`. These objects are governed by GAQP. The `memory_family` field is not used for Class A objects.

**Class B — Structural Memory**  
Memory objects that are not qualitative claims — tenant configuration, operator relationships, organizational context, authority boundaries, constraint records — use `memory_family`. These are structural facts, not governed claims. They do not go through GAQP classification.

**The rule:** If a memory object can be assigned a GAQP claim type, it is Class A. If it cannot, it is Class B. Every memory object must be one or the other. None may be unclassified.

This eliminates the parallel taxonomy problem. GAQP governs qualitative memory. `memory_family` governs structural memory. They do not overlap.

---

## V. Relationship to the Qualitative Capture Runtime

The QCR pipeline (see `docs/product/QUALITATIVE_CAPTURE_RUNTIME_SPEC.md`) is the primary feeder for PEM's Class A objects.

The connection points:

| QCR Object | PEM Entry Condition | PEM Activation State |
|---|---|---|
| `atomic_nugget` reaching Structural confidence (1.00) | Auto-eligible for PEM admission | `active` |
| `preserved_idea` (human-memorialized) | Eligible immediately on creation | `active` |
| `promotion_candidate` approved by operator | Admitted as Canon-class memory | `active` |
| `rail_artifact` from Promote operator action | Admitted as `deferred` pending review | `deferred` |
| `executive_conclusion` with confidence ≥ 0.85 | Eligible after 3 independent session recurrences | `deferred → active` |

The QCR builds the corpus. PEM makes that corpus available to the upstream reasoning layer. These are two distinct systems with a governed handoff — the QCR does not write to PEM directly. Admission always passes through the PEM service seam.

---

## VI. Module Structure

```
src/service/memory/
  models.py           — MemoryObject ORM model (Class A + Class B)
  repository.py       — data access: admit, get, list, update state
  service.py          — governed service seam: all external callers use this
  admission.py        — admission path: validates, classifies, writes
  retrieval.py        — retrieval path: tenant-scoped reads
  lifecycle.py        — promote, demote, archive, retire operations
  qcr_bridge.py       — governed handoff from QCR corpus to PEM admission
  upstream_context.py — assembles PEM memory context for upstream reasoning
  tests/
```

---

## VII. Database Object

One new table: `memory_objects`.

| Field | Type | Required | Description |
|---|---|---|---|
| `memory_id` | UUID | Yes | Primary key — distinct from envelope_id and nugget_id |
| `tenant_id` | UUID | Yes | Hard tenant boundary — no cross-tenant reads |
| `memory_class` | enum | Yes | `gaqp_claim` (Class A) / `structural` (Class B) |
| `claim_type` | enum | Class A only | One of the 24 GAQP canonical claim types |
| `memory_family` | enum | Class B only | One of the governed structural memory families |
| `activation_state` | enum | Yes | `active` / `deferred` / `reference_only` / `dormant` |
| `content` | text | Yes | Substantive memory payload |
| `summary` | text | Yes | One-sentence executive-readable description |
| `source_kind` | enum | Yes | `qcr_nugget` / `qcr_preserved` / `qcr_promotion` / `operator_direct` / `decision_artifact` |
| `source_ref` | UUID | Yes | FK to the source object (nugget_id, idea_id, artifact_id, or envelope_id) |
| `actor_id` | UUID | No | User who admitted it (null for system-admitted) |
| `origin_surface` | string | Yes | Which surface produced the admission |
| `admission_reason` | text | No | Why this was admitted |
| `confidence` | float | No | Inherited from source GAQP object where applicable |
| `related_memory_ids` | UUID[] | No | Links to associated memory objects |
| `supersedes` | UUID | No | FK to prior memory_object this one replaces or narrows |
| `created_at` | timestamptz | Yes | Admission timestamp |
| `updated_at` | timestamptz | Yes | Latest governed state change |
| `archived_at` | timestamptz | No | When archived — null while active |

**Indexes:** `(tenant_id, activation_state)`, `(tenant_id, claim_type)`, `(tenant_id, memory_family)`, `(tenant_id, source_ref)`, `(tenant_id, created_at DESC)`

**Retention:** Perpetual. No hard deletes. Archive and retire are state changes.

---

## VIII. The Upstream Context Assembly

The most important V1.0 function is `upstream_context.py` — the module that assembles relevant PEM memory for the upstream reasoning layer before each session begins reasoning.

This is what closes the blind man problem. Before Prime Directive, Polymorphia, or EKE reasons about a scenario, the system assembles the relevant memory context from PEM and makes it available.

**V1.0 assembly logic:**

```
Given: tenant_id, scenario_type, domain

1. Retrieve all active memory objects for tenant
2. Filter by domain relevance (claim_type and memory_family match)
3. Filter by activation_state = active
4. Rank by: Structural confidence first, then recency
5. Cap at 20 objects (V1.0 limit — no semantic ranking yet)
6. Return as MemoryContext object to upstream caller
```

The MemoryContext is injected into the reasoning prompt alongside the current scenario. Upstream reasoning is now aware of what the organization has previously concluded in this domain.

This is the mechanism that makes sessions non-stateless. It is not semantic search. It is governed, deterministic, tenant-scoped context injection.

Semantic retrieval (embedding-based relevance ranking) is Phase 2.

---

## IX. Admission Sources in V1.0

Three admission sources are active in V1.0:

**1. QCR Bridge (primary — automated)**  
When a QCR `atomic_nugget` reaches Structural confidence (1.00), `qcr_bridge.py` generates a PEM admission request. The nugget's GAQP metadata (claim_type, domain, confidence, provenance) maps directly to the PEM memory object. Activation state: `active`.

**2. Human Memorialize (highest priority — operator-triggered)**  
When an operator Memorializes an item on the right rail, the preserved_idea is eligible for immediate PEM admission. These are admitted with `activation_state = active` and highest retrieval priority. This is the operator saying "this matters" — PEM treats it accordingly.

**3. Operator Promotion (canon-class)**  
When a promotion_candidate is approved, the promoted doctrine is admitted to PEM as `activation_state = active` with the `claim_type` of the approved GAQP type. These are the highest-authority memory objects — governing doctrine.

**Out of scope for V1.0:** Automatic journal-to-memory promotion, heuristic extraction, semantic discovery, cross-tenant admission.

---

## X. Service Seam API (V1.0)

Five operations. No more in V1.0.

```python
# Admit a new memory object
admit_memory(tenant_id, memory_class, content, summary, source_kind,
             source_ref, origin_surface, claim_type=None,
             memory_family=None, activation_state='active',
             actor_id=None, admission_reason=None) -> MemoryObject

# Get a specific memory object
get_memory(tenant_id, memory_id) -> MemoryObject

# List recent memory objects (bounded)
list_memory(tenant_id, limit=50, activation_state=None,
            claim_type=None, memory_family=None) -> list[MemoryObject]

# Assemble upstream context for reasoning
get_upstream_context(tenant_id, scenario_type, domain) -> MemoryContext

# Update activation state (promote, demote, archive, retire)
update_memory_state(tenant_id, memory_id, new_state,
                    actor_id, reason) -> MemoryObject
```

All operations enforce tenant scope. All state changes are logged to `audit_events`. No raw table access outside this seam.

---

## XI. What Does Not Change in V1.0

- The decision journal (`ExecutionRecord`) is unchanged — PEM sits beside it, not inside it
- The QCR pipeline is unchanged — `qcr_bridge.py` reads from it, does not modify it
- The chat surface is unchanged — memory context injection happens in the reasoning layer, invisible to the operator UI
- No vector database — V1.0 uses deterministic filtering and ranking only
- No semantic search — that is Phase 2

---

## XII. Definition of Done

V1.0 PEM is complete when:

- [ ] `memory_objects` table exists with migration
- [ ] `src/service/memory/` module exists with all six files
- [ ] `admit_memory` writes a valid memory object with required fields
- [ ] `get_memory` and `list_memory` enforce tenant scope
- [ ] `get_upstream_context` returns a MemoryContext that is injected into at least one upstream reasoning path (decision loop)
- [ ] `qcr_bridge.py` admits QCR Structural-confidence nuggets to PEM
- [ ] `update_memory_state` logs to `audit_events`
- [ ] All five service seam operations have passing unit tests
- [ ] No raw `memory_objects` table reads exist outside `repository.py`
- [ ] At least one end-to-end test: nugget reaches Structural → admitted to PEM → appears in upstream context on next session

---

## XIII. The Governing Formulation

Without PEM, every session reasons well and forgets everything.  
With PEM, every session reasons from what the organization already knows.

That is the difference between a tool and an institution.

V1.0 does not build the full institution. It builds the first working memory — the minimum that makes the reasoning layer non-stateless and allows institutional intelligence to begin compounding.

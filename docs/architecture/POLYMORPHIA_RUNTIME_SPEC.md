# POLYMORPHIA_RUNTIME_SPEC.md

## Status
Draft v0.1 — Developer-facing runtime spec

## Owner
Architecture / Core 7

## Companion Documents
- `POLYMORPHIA_RUNTIME_USAGE.md` — conceptual model, dimensional map, collapsed reading doctrine
- `POLYMORPHIA_MAP_SPEC.md` — map production, validation rules, pipeline flow

This document covers what those two do not: the representation model, entity framing, mode taxonomy, service seam, lifecycle, constrained degradation, audit events, storage schema, and test matrix.

---

## Purpose

Polymorphia is Execalc's governed multi-entity, multi-lens, representation-aware reasoning subsystem. Its job is to compose multiple strategic lenses, multiple relevant parties, and the correct represented-interest posture into a single disciplined reasoning frame — without loyalty drift, without ungoverned blending, and without collapsing complexity prematurely.

The existing specs define what the dimensional map contains and how it is validated. This spec defines the runtime machinery that produces it.

---

## Core Invariants

These are non-negotiable. If any invariant is violated, the subsystem must degrade or halt rather than continue.

### 1. Representation Invariant
Polymorphia must know whose interests it is representing before full reasoning mode can run. No unconstrained multi-party synthesis without an explicit declared representation anchor.

### 2. Governance Invariant
Polymorphia composes reasoning. It does not adjudicate final governed output. The Prime Directive is the downstream adjudicator.

### 3. No Hidden Role-Switch Invariant
The represented party cannot change midstream without a fresh declaration and a new validation pass.

### 4. No Soup Invariant
Multiple lenses may be composed, but not blended into an untraceable answer. Lens participation must remain inspectable in output and audit.

### 5. Constrained Fallback Invariant
If loyalty, entity structure, or lens integrity is unclear, the subsystem degrades safely rather than fabricating coherence.

### 6. Read-Only Lens Invariant
Polymorphic lenses may observe, annotate, surface tension, and contribute perspective to reasoning. They may not write to memory, trigger execution, or produce governed output independently.

A lens is an analytical instrument, not an actor. The Prime Directive is the downstream adjudicator. The lens provides input to that evaluation — it does not replace it.

**Specifically prohibited for any active lens:**
- Writing to session memory or operator memory
- Triggering reflex activation
- Producing output that reaches the operator without passing the Prime Directive gate
- Initiating execution pathways

**Violation consequence:** If a lens produces output that bypasses the evaluation gate, the output is invalid and must be discarded. The lens has contaminated the reasoning frame. This is a governance failure, not a reasoning error.

This invariant prevents the most common Polymorphia failure mode: a lens that was intended to provide perspective quietly becoming a decision-maker.

---

## Runtime Modes

```typescript
type PolymorphiaMode =
  | "triangulation"       // asymmetry across multiple parties
  | "role_switching"      // posture adaptation to represented principal
  | "multi_lens"          // same situation through multiple frameworks
  | "full_polymorphic";   // all three simultaneously — highest governance mode
```

### Mode Semantics

**triangulation**
Used when multiple relevant parties exist and asymmetry must be evaluated.
Question: Who gains, who loses, where is the leverage differential, and for whom?
Minimum: 2 entities, 1 representation anchor.

**role_switching**
Used when output must adapt posture to a specific represented principal.
Question: From whose seat am I reasoning right now?
Minimum: explicit representation anchor, context justification.

**multi_lens**
Used when the same situation must be tested through multiple frameworks.
Question: What changes when this is viewed through financial, market, operational, and risk lenses simultaneously?
Minimum: 2 distinct non-redundant lenses.

**full_polymorphic**
Used when all three functions are needed together.
This is the most heavily governed mode — requires all preconditions for all three.

---

## Data Contracts

### Representation Anchor

```typescript
type RepresentationAnchor = {
  represented_party_id: string;
  represented_party_type:
    | "operator"
    | "client"
    | "tenant"
    | "authorized_delegate";
  authority_basis:
    | "default_operator"
    | "active_cartridge"
    | "explicit_instruction"
    | "policy_binding";
};
```

Default anchor is always the current operator. Alternative anchors (client, delegate) require an active cartridge, explicit instruction, or policy binding. Free-floating "neutral" synthesis that blends parties without declaring a principal is disallowed.

---

### Entity Frame

```typescript
type EntityFrame = {
  entity_id: string;
  entity_type:
    | "operator"
    | "client"
    | "counterparty"
    | "market"
    | "partner"
    | "internal_team"
    | "external_actor";
  role_in_situation: string;
  objectives?: string[];
  constraints?: string[];
  risk_profile?: string;
  relationship_to_represented_party?:
    | "aligned"
    | "opposed"
    | "neutral"
    | "mixed"
    | "unknown";
};
```

---

### Reasoning Lenses

```typescript
type ReasoningLens =
  | "financial"
  | "market"
  | "operational"
  | "ethical"
  | "governance"
  | "supply_demand"
  | "risk_reward"
  | "balance_sheet"
  | "clarity"
  | "timing"
  | "relationship";
```

The three Prime Directive lenses (`supply_demand`, `risk_reward`, `balance_sheet`) must always be evaluable from the composed output. Additional lenses extend coverage but do not replace PD coverage.

---

### Lifecycle State

```typescript
type PolymorphiaState =
  | "declared"      // context assembled, not yet validated
  | "validated"     // all integrity checks passed
  | "active"        // reasoning mode live
  | "constrained"   // partial activation under fail-safe
  | "escalated"     // blocked pending clarification or policy resolution
  | "disabled";     // hard policy stop
```

---

### Runtime Context

```typescript
type PolymorphiaContext = {
  polymorphia_context_id: string;
  tenant_id: string;
  session_id: string;
  scenario_id?: string;
  cartridge_id?: string | null;
  representation: RepresentationAnchor;
  entities: EntityFrame[];
  selected_lenses: ReasoningLens[];
  mode: PolymorphiaMode;
  state: PolymorphiaState;
  activation_reason: string;
  operator_loyalty_verified: boolean;
  validation_notes: string[];
  fail_safe_flags: string[];
  created_at: string;
  updated_at: string;
};
```

---

### Lens Contribution and Entity Asymmetry

```typescript
type LensContribution = {
  lens: ReasoningLens;
  summary: string;
  conflicts?: string[];       // conflicts with other lenses
};

type EntityAsymmetry = {
  entity_id: string;
  upside?: string[];
  downside?: string[];
  leverage_points?: string[];
  exposure_points?: string[];
};
```

---

### Prime Directive Handoff

```typescript
type PolymorphiaHandoff = {
  represented_party_id: string;
  mode: PolymorphiaMode;
  lens_contributions: LensContribution[];
  entity_asymmetries: EntityAsymmetry[];
  synthesized_summary: string;
  constraint_notes: string[];
  fail_safe_flags: string[];
};
```

Polymorphia is not the final adjudicator. Its job is to produce this structured handoff object. The Prime Directive layer determines whether the composed path delivers value, whether the asymmetry is favorable, and whether the recommendation should proceed, adjust, or be blocked.

---

## Service Seam

These are internal service functions, not public API routes.

### declare_polymorphia_context

```typescript
type DeclarePolymorphiaContextRequest = {
  tenant_id: string;
  session_id: string;
  scenario_id?: string;
  cartridge_id?: string | null;
  representation: RepresentationAnchor;
  entities: EntityFrame[];
  requested_mode: PolymorphiaMode;
  selected_lenses: ReasoningLens[];
  activation_reason: string;
};

type DeclarePolymorphiaContextResult = {
  polymorphia_context_id: string;
  state: "declared";
};

declare_polymorphia_context(
  request: DeclarePolymorphiaContextRequest
): DeclarePolymorphiaContextResult
```

---

### validate_polymorphia_context

```typescript
type PolymorphiaValidationResult = {
  loyalty_check: "pass" | "fail";
  triangulation_check: "pass" | "fail";
  multi_lens_check: "pass" | "fail";
  role_switch_check: "pass" | "fail";
  fail_safe_check: "pass" | "fail";
  overall_status: "validated" | "constrained" | "escalated" | "blocked";
  notes: string[];
  fail_safe_flags: string[];
};

validate_polymorphia_context(
  tenant_id: string,
  polymorphia_context_id: string
): PolymorphiaValidationResult
```

---

### activate_polymorphia

```typescript
type ActivatePolymorphiaResult = {
  polymorphia_context_id: string;
  state: "active" | "constrained" | "escalated" | "disabled";
  operator_loyalty_verified: boolean;
  fail_safe_flags: string[];
};

activate_polymorphia(
  tenant_id: string,
  polymorphia_context_id: string
): ActivatePolymorphiaResult
```

---

### execute_polymorphia_pass

```typescript
type ExecutePolymorphiaPassRequest = {
  tenant_id: string;
  polymorphia_context_id: string;
  prompt: string;
  facts?: string[];
  constraints?: string[];
};

type ExecutePolymorphiaPassResult = {
  polymorphia_context_id: string;
  represented_party_id: string;
  mode: PolymorphiaMode;
  lens_contributions: LensContribution[];
  entity_asymmetries: EntityAsymmetry[];
  synthesized_summary: string;
  constraint_notes: string[];
  prime_directive_handoff_required: boolean;
};

execute_polymorphia_pass(
  request: ExecutePolymorphiaPassRequest
): ExecutePolymorphiaPassResult
```

---

### Lifecycle Mutations

```typescript
constrain_polymorphia_context(
  tenant_id: string,
  polymorphia_context_id: string,
  reason: string
): PolymorphiaContext

disable_polymorphia_context(
  tenant_id: string,
  polymorphia_context_id: string,
  reason: string
): PolymorphiaContext

get_polymorphia_context(
  tenant_id: string,
  polymorphia_context_id: string
): PolymorphiaContext | null
```

Avoid a generic `update_polymorphia_context()`. The lifecycle policy is explicitly biased toward narrow, auditable mutations — mirroring the Persistent Memory Phase 1 posture.

---

## Validation Rules

Validation runs after declaration and before activation.

### Loyalty Check
**Pass:** `represented_party_id` exists; `authority_basis` is valid; represented party is permitted in current tenant/session context.
**Fail:** represented party missing; authority basis unsupported; client representation asserted without cartridge, policy, or explicit instruction.

### Triangulation Check
**Pass:** mode requires triangulation and ≥ 2 material entities present; each entity has a role; `relationship_to_represented_party` is known or explicitly `"unknown"`.
**Fail:** only one entity in triangulation/full mode; entities named but structurally empty; entity roles absent.

### Multi-Lens Check
**Pass:** mode requires multiple lenses and ≥ 2 distinct relevant lenses selected; lenses are non-duplicative and non-decorative.
**Fail:** one lens only in multi-lens/full mode; lenses overlap so heavily they are effectively duplicates.

### Role-Switch Check
**Pass:** reasoning posture matches represented party; no competing representation anchor.
**Fail:** answer posture implicitly favors a different entity than the declared principal; mixed representation attempted without explicit support.

### Fail-Safe Check
**Pass:** a safe degraded mode exists when some validation checks fail.
**Fail:** system would need to fabricate missing representation, entity structure, or lens integrity to continue.

---

## Lifecycle Transitions

```
declared  →  validated       (all checks pass)
declared  →  constrained     (some checks fail; safe partial mode exists)
declared  →  escalated       (loyalty or governance unresolved)
validated →  active          (runtime execution begins)
active    →  constrained     (midstream conflict detected)
active    →  disabled        (hard policy stop)
constrained → active         (missing conditions resolved)
escalated →  active          (explicit resolution received)
```

**No hidden transitions.** No invisible role changes midstream. No switching represented party without a new declaration and validation pass.

---

## Degradation Policy

### constrained
Use when: representation is valid but entities are incomplete; lens set is thin; triangulation is partial but still useful.
Behavior: run narrowed analysis; emit fail-safe flags; do not label output as `full_polymorphic`.

### escalated
Use when: represented party is unresolved; authority basis missing; client/cartridge posture conflicts with operator-default.
Behavior: no full execution; emit escalation reason; require upstream clarification or policy resolution.

### disabled
Use when: hard policy blocks execution; represented party is forbidden; governance gate fails.
Behavior: terminate polymorphic path; emit audit event; hand control back to non-polymorphic path or stop.

---

## Failure Cases

### PM-001 Missing Represented Party
Condition: no `represented_party_id`
Expected: loyalty check fails; status = `escalated` or `blocked`

### PM-002 Unsupported Authority Basis
Condition: `authority_basis` not in allowed enum
Expected: loyalty check fails; activation denied

### PM-003 Triangulation Mode With One Entity
Condition: `mode = "triangulation"` or `"full_polymorphic"`; `entities.length < 2`
Expected: triangulation check fails; state = `constrained` or `escalated`

### PM-004 Multi-Lens Mode With One Lens
Condition: `mode = "multi_lens"` or `"full_polymorphic"`; `selected_lenses.length < 2`
Expected: multi-lens check fails; no full activation

### PM-005 Hidden Role Drift
Condition: output posture shifts toward non-represented party mid-pass
Expected: role-switch check fails or post-pass constraint triggers; state → `constrained` or `disabled`

### PM-006 Client Posture Without Valid Linkage
Condition: `represented_party_type = "client"`; no active cartridge or explicit instruction
Expected: loyalty validation fails; escalation required

### PM-007 Excessive Lens Sprawl
Condition: lens count exceeds configured maximum without justification
Expected: lens set reduced or activation constrained

### PM-008 Entity Ambiguity
Condition: entities present but all have vague or identical roles
Expected: triangulation check fails; no asymmetry output produced

---

## Audit Events

### Event Schema

```typescript
type PolymorphiaAuditEvent = {
  event_id: string;
  tenant_id: string;
  polymorphia_context_id: string;
  session_id: string;
  scenario_id?: string;
  event_type:
    | "polymorphia_declared"
    | "polymorphia_validated"
    | "polymorphia_validation_failed"
    | "polymorphia_activated"
    | "polymorphia_constrained"
    | "polymorphia_escalated"
    | "polymorphia_disabled"
    | "polymorphia_pass_executed"
    | "polymorphia_prime_directive_handoff";
  represented_party_id?: string;
  authority_basis?: string;
  mode?: PolymorphiaMode;
  entity_count?: number;
  selected_lenses?: ReasoningLens[];
  fail_safe_flags?: string[];
  notes?: string[];
  created_at: string;
};
```

### Minimum Required Events
Emit at minimum on:
- declaration
- validation pass or failure
- activation
- constrained downgrade
- escalation
- disable
- successful pass execution
- Prime Directive handoff

---

## Storage Schema

### polymorphia_contexts

| Column | Type | Notes |
|---|---|---|
| `polymorphia_context_id` | string PK | stable identity |
| `tenant_id` | string indexed | required on every operation |
| `session_id` | string indexed | |
| `scenario_id` | string nullable | |
| `cartridge_id` | string nullable | |
| `represented_party_id` | string | from representation anchor |
| `represented_party_type` | string | |
| `authority_basis` | string | |
| `mode` | string | enum |
| `state` | string indexed | enum |
| `operator_loyalty_verified` | boolean | |
| `activation_reason` | text | |
| `entities_json` | jsonb | EntityFrame[] |
| `selected_lenses_json` | jsonb | ReasoningLens[] |
| `validation_notes_json` | jsonb | string[] |
| `fail_safe_flags_json` | jsonb | string[] |
| `created_at` | timestamp | |
| `updated_at` | timestamp | |

### polymorphia_audit_events

| Column | Type | Notes |
|---|---|---|
| `event_id` | string PK | |
| `tenant_id` | string indexed | |
| `polymorphia_context_id` | string indexed | |
| `session_id` | string indexed | |
| `scenario_id` | string nullable | |
| `event_type` | string | enum |
| `represented_party_id` | string nullable | |
| `authority_basis` | string nullable | |
| `mode` | string nullable | |
| `entity_count` | integer nullable | |
| `selected_lenses_json` | jsonb nullable | |
| `fail_safe_flags_json` | jsonb nullable | |
| `notes_json` | jsonb nullable | |
| `created_at` | timestamp indexed | |

---

## Test Matrix

### Activation Tests
- Declares context with valid operator representation
- Validates full mode with 3 entities and 3 lenses
- Activates triangulation with valid operator loyalty
- Activates role-switch mode for client with valid cartridge linkage
- Activates multi-lens mode with 2 distinct lenses

### Constraint Tests
- Constrains full mode when only one lens survives validation
- Constrains triangulation when second entity is under-specified
- Preserves represented party while degrading mode to constrained

### Escalation Tests
- Escalates when client representation lacks authority basis
- Escalates when represented party is missing
- Escalates when two competing representation anchors appear

### Disable Tests
- Disables when policy forbids represented party type
- Disables when governance check fails after activation

### Audit Tests
- Emits declaration event on context creation
- Emits validation event on pass
- Emits constraint event on downgrade
- Emits Prime Directive handoff event after pass execution

### Drift Tests
- Blocks hidden role change between declaration and execution
- Flags output that favors non-represented entity
- Preserves original anchor in audit trail after failure

---

## Canonical Example

**Use case:** Negotiation on behalf of a client

```
represented_party:  client hockey team (Leafs front office)
entities:           Leafs, player, agent, rival club, cap environment
lenses:             financial, supply_demand, risk_reward, relationship
mode:               full_polymorphic
authority_basis:    active_cartridge
```

**Flow:**
1. `declare_polymorphia_context` — assemble the frame
2. `validate_polymorphia_context` — loyalty, entity structure, lens integrity
3. `activate_polymorphia` — state → `active`
4. `execute_polymorphia_pass` — produce lens contributions, entity asymmetries, synthesized summary
5. Hand off `PolymorphiaHandoff` to Prime Directive
6. Emit audit events throughout

**What the output captures:**
- What the Leafs gain and risk from each option
- What the agent and player are optimizing for (and where that diverges from the Leafs' interests)
- Where leverage sits (supply/demand: rival club interest as BATNA)
- What the financial and relationship lenses say in combination
- Which path the Prime Directive should evaluate

---

## Relationship to Existing Polymorphia Docs

| Document | Covers |
|---|---|
| `POLYMORPHIA_RUNTIME_USAGE.md` | What Polymorphia is; dimensional map; collapsed reading doctrine; PD relationship |
| `POLYMORPHIA_MAP_SPEC.md` | Map production; required axes; validation rules; operator disclosure format |
| **This document** | Representation model; entity framing; mode taxonomy; service seam; lifecycle; degradation; audit events; storage; test matrix |

The three documents are complementary. This spec does not supersede the others — it extends them with the runtime machinery that the conceptual docs imply but do not specify.

---

## Design Principle

> Polymorphia is not the framework that finds the answer. It is the framework that ensures the answer was found from the right seat, through the right lenses, with all relevant parties in view.

The representation anchor is not bureaucracy. It is what prevents the system from reasoning brilliantly on behalf of the wrong principal.

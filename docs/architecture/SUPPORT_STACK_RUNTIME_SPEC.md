# SUPPORT_STACK_RUNTIME_SPEC.md

## Status
Draft v0.1 — Developer-facing runtime spec

## Owner
Architecture / Runtime Layer

## Companion Documents
- `SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md` — four named components, governance enforcement hierarchy, conceptual model
- `REFLEX_AND_ACTIVATION_SYSTEM.md` — five-stage detection cascade, reflex gate, context package assembly

This document covers what those two do not: the runtime object model, named system reflexes (PRP-01, BDR-01), Carat interlock mechanics, Heuristic Hygiene System, service seam, lifecycle states, audit event schema, and test matrix.

---

## Purpose

The Support Stack is Execalc's governance layer, reflex shield, and operational immune system. It does not generate strategy. It ensures that every output the system produces is valid, timely, context-aware, aligned with operator interests, and correctable under stress.

Its job in one sentence: keep the judgment engine from becoming chaotic, brittle, noisy, or disloyal — in production, under adversarial conditions, over time.

**The core runtime principle:**

> Reflexes do not fire directly from the model. They fire through the Support Stack.

Reflex activation is a governed runtime event, not a statistical output. The stack continuously checks for drift, contradiction, scenario mismatch, and overload before any logic unit is allowed to activate.

---

## Five Runtime Components

The Support Stack has five named runtime components. Each is a distinct subsystem with its own object contract, service methods, and audit requirements.

| Component | Function |
|---|---|
| **Reflex Triggers** | Always-on background checks that detect drift, contradiction, mismatch, and overload |
| **System Reflexes** | Hardcoded QA behaviors (PRP-01, BDR-01) that fire on specific conditions |
| **Carat Interlocks** | Governance layer that prevents conflicting, mismatched, or low-priority Carats from co-activating |
| **Heuristic Hygiene System** | Continuous background maintenance of the heuristic library |
| **Recursive Reintegration Protocol** | Self-repair loop that audits and corrects failed decision paths |

---

## Data Contracts

### Stack Lifecycle State

```typescript
type SupportStackState =
  | "monitoring"           // background checks running, no candidate detected
  | "candidate_detected"   // trigger fired; candidate logic path identified
  | "validated"            // candidate cleared governance checks
  | "constrained"          // partial activation under fail-safe
  | "suppressed"           // overload or conflict blocks output
  | "escalated"            // operator complaint or governance ambiguity; recursive audit required
  | "active";              // selected reflex path running
```

### Reflex Trigger Types

```typescript
type ReflexTriggerType =
  | "drift_detector"            // output deviating from governing logic patterns
  | "contradiction_checker"     // inconsistent heuristic chain detected
  | "scenario_match_validator"  // Carat or thinker inappropriate for classified scenario
  | "overload_buffer";          // too many simultaneous signals; output quality at risk
```

### System Reflex Codes

```typescript
type SystemReflexCode =
  | "PRP-01"   // operator complaint → recursive audit sequence
  | "BDR-01";  // latent strategic value in operator input → promotion or triage
```

### Carat Interlock Types

```typescript
type InterlockType =
  | "polarity_conflict"      // two Carats with opposing polarity cannot co-activate
  | "scenario_gate"          // Carat is outside its valid situational domain
  | "priority_suppression";  // lower-leverage Carat suppressed by higher-stakes Carat
```

### Hygiene Event Types

```typescript
type HygieneEventType =
  | "decay_scan"           // heuristic freshness evaluated against time and usage
  | "contradiction_scan"   // heuristic conflicts with another active heuristic
  | "duplicate_merge"      // two heuristics are functionally identical; merged
  | "duplicate_flag"       // suspected duplicate flagged for operator review
  | "version_roll"         // heuristic updated; prior version preserved
  | "confidence_recompute"; // confidence score updated based on observed performance
```

### Runtime Context Object

```typescript
type SupportContext = {
  support_context_id: string;
  tenant_id: string;
  session_id: string;
  scenario_id?: string | null;
  represented_party_id?: string | null;
  state: SupportStackState;
  active_trigger_types: ReflexTriggerType[];
  active_system_reflexes: SystemReflexCode[];
  active_interlocks: InterlockType[];
  fail_safe_flags: string[];
  notes: string[];
  created_at: string;
  updated_at: string;
};
```

---

## Component 1: Reflex Triggers

Reflex triggers are always-on background checks that run continuously during a session. They are the earliest detection layer — they do not activate logic paths themselves, but they produce candidates that the rest of the stack evaluates.

### Trigger Object

```typescript
type ReflexTrigger = {
  trigger_id: string;
  tenant_id: string;
  session_id: string;
  type: ReflexTriggerType;
  status: "watching" | "fired" | "cleared" | "suppressed";
  reason: string;
  evidence: string[];
  severity: "low" | "medium" | "high";
  created_at: string;
  resolved_at?: string | null;
};
```

### Trigger Behavior

**drift_detector**
Fires when output reasoning begins to deviate from the patterns established by the governing logic for this session. Does not block output — surfaces the deviation for downstream evaluation.
*Detection method:* Compare intermediate reasoning steps against active governance framework constraints. Flag when a step produces a conclusion inconsistent with prior steps or active PD lens evaluations.

**contradiction_checker**
Fires when two heuristics in the active set produce opposing guidance for the same situation without a reconciliation mechanism.
*Detection method:* Cross-check activation tags of simultaneously active heuristics. Flag when `polarity` fields conflict and no resolution doctrine governs the tension.

**scenario_match_validator**
Fires when a Carat, thinker, or corpus entry is loaded that does not match the classified scenario's situational domain.
*Detection method:* Compare loaded corpus activation tags against classified scenario tags. Mismatch above threshold triggers candidate suppression review.

**overload_buffer**
Fires when the number of simultaneously active signals, Carats, or heuristics exceeds the coherent composition threshold.
*Detection method:* Count active logic units in the context package. Above threshold, evaluate which units are below materiality and suppress them before output proceeds.

### Service Methods

```typescript
get_active_triggers(
  tenant_id: string,
  session_id: string
): ReflexTrigger[]

resolve_trigger(
  tenant_id: string,
  trigger_id: string,
  resolution: "cleared" | "suppressed",
  notes: string
): ReflexTrigger
```

---

## Component 2: System Reflexes

System reflexes are hardcoded QA behaviors. Unlike scenario-specific reflexes that are configured per situation, system reflexes fire on specific runtime conditions regardless of scenario type. They are non-optional.

---

### PRP-01 — Performance Recovery Protocol

**Trigger condition:** Operator flags a flaw, error, or failure in the system's output or reasoning.

**What it does:** A single complaint does not merely patch the answer. It triggers a five-stage recursive audit of the decision path that produced the flawed output.

**Five stages:**
1. **Logic rewind** — replay the reasoning chain that produced the output
2. **Memory source validation** — verify that admitted memory referenced in the output was accurate and current
3. **Heuristic drift scan** — check whether any heuristic active during the decision has degraded since it was encoded
4. **Reflex correction injection** — if a missed or misfired reflex is identified, inject the correction into the current session
5. **QA archive flagging** — flag the decision in the audit archive for governance review

**Why it matters:** Without PRP-01, operator complaints become one-off corrections that evaporate. With PRP-01, a complaint is a signal that propagates backward through the logic trail and forward into system improvement.

```typescript
type PRP01Request = {
  tenant_id: string;
  session_id: string;
  target_output_id: string;
  complaint_text: string;
};

type PRP01Result = {
  audit_run_id: string;
  stages_executed: (
    | "logic_rewind"
    | "memory_source_validation"
    | "heuristic_drift_scan"
    | "reflex_correction_injection"
    | "qa_archive_flagging"
  )[];
  correction_flags: string[];
  archive_flagged: boolean;
  corrective_heuristic_prompted: boolean;
};

run_prp_01(request: PRP01Request): PRP01Result
```

---

### BDR-01 — Blind/Deaf Reflex (Latent Value Elevation)

**Trigger condition:** Operator input contains latent strategic value — a pattern, heuristic candidate, contact intelligence, buyer/seller signal, or causal insight — that has not been explicitly tagged or flagged by the operator.

**What it does:** Elevates the detected signal rather than letting it scroll past as conversational context.

**Target signal classes:**
- Offhand remarks that contain encoded strategic patterns
- Pattern fragments the operator expresses as casual observation
- Heuristic candidates ("I've noticed that...", "when X happens, Y follows")
- Contact or relationship intelligence
- Buyer/seller behavioral signals
- Causal claims derived from experience

**Output behavior:**
- High confidence detection → automatic promotion candidate into Heuristic Coding pipeline
- Low confidence detection → triage flag for operator confirmation before promotion

**Architectural note:** BDR-01 fires from the Support Stack. When it produces a promotion candidate, that candidate enters the Heuristic Coding System's admission pipeline (BDR-01 is the interception reflex described in `HEURISTIC_CODING_SYSTEM.md`). The Support Stack is the trigger; Heuristic Coding is the pipeline. Same reflex, two specs, correct positioning.

```typescript
type BDR01Request = {
  tenant_id: string;
  session_id: string;
  raw_input: string;
};

type BDR01Result = {
  detected_signal_classes: string[];
  action: "promote_heuristic" | "flag_for_triage" | "no_action";
  confidence: number;
  heuristic_candidate_id?: string | null;
  triage_reason?: string | null;
};

run_bdr_01(request: BDR01Request): BDR01Result
```

---

## Component 3: Carat Interlocks

Carat Interlocks are the anti-soup mechanism. Without them, multiple Carats with conflicting logic can co-activate, producing incoherent or contradictory output. Interlocks govern which Carats can be simultaneously active.

### Carat Activation Candidate

```typescript
type CaratActivationCandidate = {
  carat_id: string;
  polarity:
    | "positive"
    | "negative"
    | "preventive"
    | "aggressive"
    | "defensive"
    | "mixed";
  scenario_domain: string[];    // scenarios this Carat is valid for
  leverage_level: number;       // 0.0–1.0; used for priority suppression
};
```

### Interlock Decision

```typescript
type InterlockDecision = {
  candidate_carat_id: string;
  allowed: boolean;
  blocked_by?: InterlockType[];
  notes: string[];
};
```

### Three Interlock Rules

**Polarity Conflict**
Two Carats with directly opposing polarity (e.g., `aggressive` and `defensive`) cannot be simultaneously active without an explicit reconciliation doctrine. When detected, the lower-confidence Carat is suppressed and the conflict is surfaced.

**Scenario Gate**
A Carat may only activate within its declared `scenario_domain`. A Carat valid for `negotiation` scenarios does not activate in a `strategic_planning` session. The gate checks the candidate's domain against the classified scenario before allowing activation.

**Priority Suppression**
When a high-leverage Carat (`leverage_level` ≥ 0.8) is active, lower-leverage Carats (`leverage_level` < 0.5) competing for the same attention space are suppressed. This prevents the output from becoming cluttered with marginal signal when a dominant strategic frame is already loaded.

### Service Method

```typescript
evaluate_carat_interlocks(
  tenant_id: string,
  scenario_id: string,
  candidates: CaratActivationCandidate[]
): InterlockDecision[]
```

---

## Component 4: Heuristic Hygiene System

The Heuristic Hygiene System is continuous background maintenance of the heuristic library. It is distinct from Recursive Analysis Mode 2 (which performs periodic and trigger-based audit of heuristic performance against Decision Outcomes). The Hygiene System performs ongoing structural health checks.

**Recursive Analysis Mode 2** asks: *is this heuristic producing the outcomes it predicted?*
**Heuristic Hygiene System** asks: *is this heuristic still structurally coherent and non-redundant?*

Both are required. Neither replaces the other.

### Hygiene Event Object

```typescript
type HeuristicHygieneEvent = {
  hygiene_event_id: string;
  tenant_id: string;
  heuristic_id: string;
  type: HygieneEventType;
  status: "detected" | "applied" | "flagged_for_review";
  rationale: string;
  prior_confidence?: number | null;
  new_confidence?: number | null;
  version_from?: string | null;
  version_to?: string | null;
  duplicate_of?: string | null;
  created_at: string;
};
```

### Hygiene Operations

**decay_scan**
Evaluates whether a heuristic's `freshness_rule` has been exceeded — whether time, event conditions, or usage patterns indicate the heuristic should be re-evaluated before next activation.

**contradiction_scan**
Checks the active heuristic set for structural conflicts: two heuristics that produce opposing guidance for the same Dynamic Class tag combination. Flags the pair for reconciliation; does not auto-retire either entry.

**duplicate_merge / duplicate_flag**
When two heuristics are functionally identical (same claim, same activation tags, same polarity), the system either merges them (if one clearly supersedes the other) or flags both for operator review. Deletion is not permitted — the weaker entry is versioned and dormanted, not erased.

**version_roll**
When a heuristic is updated after operator review, the prior version is preserved with a `superseded_by` reference. The doctrine is non-destructive: no heuristic is deleted. Retired heuristics become historical record.

**confidence_recompute**
When Decision Outcome data from Recursive Analysis Mode 2 arrives, or when the operator provides explicit feedback, the heuristic's confidence score is recomputed. The prior confidence is preserved in the version history.

### Service Method

```typescript
scan_heuristic_hygiene(
  tenant_id: string,
  heuristic_id: string
): HeuristicHygieneEvent[]
```

---

## Component 5: Recursive Reintegration Protocol

The Recursive Reintegration Protocol gives the Support Stack a self-repair loop. Every governed decision carries a full logic trail. When a later outcome reveals a failure, the system can replay what happened, audit what should have fired, and retrain the decision path rather than leaving the failure as institutional noise.

This is the component that prevents the Support Stack from being a defense only at runtime. It makes it a learning system over time.

### How It Works

1. **Replay** — reconstruct the original scenario, signals, context package, and reflex set that governed the failed decision
2. **Overlay** — compare what actually fired against what should have fired given the now-known outcome
3. **Audit** — identify missed triggers, misfired reflexes, and stale heuristics that contributed to the failure
4. **Retrain** — inject corrections into the active reflex and heuristic sets
5. **Prompt** — optionally surface a corrective heuristic candidate to the operator for encoding

### Service Contracts

```typescript
type ReintegrationRequest = {
  tenant_id: string;
  decision_id: string;
  failure_reason: string;
  outcome_evidence?: string | null;
};

type ReintegrationResult = {
  reintegration_run_id: string;
  replay_completed: boolean;
  missed_triggers: ReflexTriggerType[];
  missed_system_reflexes: SystemReflexCode[];
  misfired_carats: string[];
  stale_heuristics: string[];
  corrective_actions: string[];
  corrective_heuristic_prompted: boolean;
  archive_updated: boolean;
};

run_recursive_reintegration(
  request: ReintegrationRequest
): ReintegrationResult
```

---

## Reflex Firing Order

The canonical Support Stack firing sequence. Suppression and validation always precede expressive output.

```
1.  Input received
2.  Background trigger scan
      → drift_detector, contradiction_checker, scenario_match_validator, overload_buffer
3.  Situational classification
      → confirm scenario; confirm representation anchor
4.  System reflex evaluation
      → BDR-01 (latent value scan on every input)
      → PRP-01 (if operator complaint flag present)
5.  Carat interlock evaluation
      → polarity_conflict check
      → scenario_gate check
      → priority_suppression check
6.  Heuristic hygiene side-check
      → run when heuristic candidates or active heuristic conflicts are involved
7.  Reflex path activated or suppressed
      → validated paths proceed; suppressed paths log and stop
8.  Output shaped under Support Stack constraints
9.  Audit record emitted
10. Recursive reintegration available
      → fires later if outcome evidence indicates failure
```

---

## Lifecycle Transitions

```
monitoring         →  candidate_detected    (trigger fires)
candidate_detected →  validated             (scenario fit + interlocks clear)
candidate_detected →  suppressed            (overload or polarity conflict blocks)
candidate_detected →  escalated             (loyalty or governance unresolved)
validated          →  active                (reflex path allowed to run)
validated          →  constrained           (only partial activation is safe)
active             →  constrained           (midstream conflict detected)
active             →  escalated             (operator complaint received → PRP-01)
constrained        →  active                (missing conditions resolved)
escalated          →  active                (explicit resolution received)
any                →  suppressed            (hard governance stop)
```

No hidden transitions. Every state change must produce an audit event.

---

## Audit Events

```typescript
type SupportStackAuditEvent = {
  event_id: string;
  tenant_id: string;
  session_id: string;
  support_context_id: string;
  event_type:
    | "trigger_fired"
    | "trigger_cleared"
    | "trigger_suppressed"
    | "system_reflex_invoked"
    | "system_reflex_completed"
    | "carat_allowed"
    | "carat_blocked"
    | "heuristic_hygiene_detected"
    | "heuristic_hygiene_applied"
    | "reintegration_started"
    | "reintegration_completed"
    | "output_suppressed"
    | "output_constrained"
    | "state_transition";
  trigger_type?: ReflexTriggerType | null;
  system_reflex_code?: SystemReflexCode | null;
  interlock_type?: InterlockType | null;
  carat_id?: string | null;
  heuristic_id?: string | null;
  hygiene_event_type?: HygieneEventType | null;
  prior_state?: SupportStackState | null;
  new_state?: SupportStackState | null;
  details: string[];
  created_at: string;
};
```

Emit at minimum on: every trigger fire and resolution, every system reflex invocation, every Carat block or allow decision, every hygiene detection, every reintegration start and completion, every state transition.

---

## Storage Schema

### support_contexts

| Column | Type | Notes |
|---|---|---|
| `support_context_id` | string PK | |
| `tenant_id` | string indexed | required on every operation |
| `session_id` | string indexed | |
| `scenario_id` | string nullable | |
| `represented_party_id` | string nullable | |
| `state` | string indexed | enum |
| `active_trigger_types_json` | jsonb | ReflexTriggerType[] |
| `active_system_reflexes_json` | jsonb | SystemReflexCode[] |
| `active_interlocks_json` | jsonb | InterlockType[] |
| `fail_safe_flags_json` | jsonb | string[] |
| `notes_json` | jsonb | string[] |
| `created_at` | timestamp | |
| `updated_at` | timestamp | |

### support_stack_audit_events

| Column | Type | Notes |
|---|---|---|
| `event_id` | string PK | |
| `tenant_id` | string indexed | |
| `session_id` | string indexed | |
| `support_context_id` | string indexed | |
| `event_type` | string | enum |
| `trigger_type` | string nullable | |
| `system_reflex_code` | string nullable | |
| `interlock_type` | string nullable | |
| `carat_id` | string nullable | |
| `heuristic_id` | string nullable | |
| `hygiene_event_type` | string nullable | |
| `prior_state` | string nullable | |
| `new_state` | string nullable | |
| `details_json` | jsonb | string[] |
| `created_at` | timestamp indexed | |

### heuristic_hygiene_events

| Column | Type | Notes |
|---|---|---|
| `hygiene_event_id` | string PK | |
| `tenant_id` | string indexed | |
| `heuristic_id` | string indexed | |
| `type` | string | enum |
| `status` | string | enum |
| `rationale` | text | |
| `prior_confidence` | float nullable | |
| `new_confidence` | float nullable | |
| `version_from` | string nullable | |
| `version_to` | string nullable | |
| `duplicate_of` | string nullable | |
| `created_at` | timestamp indexed | |

---

## Test Matrix

### Reflex Trigger Tests
- `drift_detector` fires when reasoning step contradicts active PD lens evaluation
- `contradiction_checker` fires when two active heuristics have opposing polarity on same Dynamic Class
- `scenario_match_validator` blocks corpus entry with no matching scenario activation tags
- `overload_buffer` suppresses output when active logic unit count exceeds threshold
- All four triggers emit audit events on fire and resolution

### System Reflex Tests — PRP-01
- Operator complaint triggers all five audit stages
- Logic rewind reconstructs the original context package
- Heuristic drift scan identifies stale heuristics active at decision time
- QA archive flag is set on the target output record
- Corrective heuristic prompt is produced when a missed heuristic is identified

### System Reflex Tests — BDR-01
- High-confidence latent value produces promotion candidate into Heuristic Coding pipeline
- Low-confidence detection produces triage flag, not automatic promotion
- Signal class detection identifies heuristic candidates, contact intelligence, and buyer/seller signals
- No-action result when input contains no encodable strategic signal
- BDR-01 emits audit event regardless of action taken

### Carat Interlock Tests
- Opposing-polarity Carats cannot co-activate; lower-confidence is suppressed
- Out-of-domain Carat is blocked by scenario gate
- Low-leverage Carat is suppressed when high-leverage Carat is active
- All three interlocks emit `carat_blocked` audit events
- Allowed Carat emits `carat_allowed` audit event

### Heuristic Hygiene Tests
- Contradiction scan flags pair of heuristics with opposing polarity on same tags
- Duplicate merge produces versioned history of prior entry
- Version roll preserves prior version with `superseded_by` reference
- Confidence recompute updates score while preserving prior value in version history
- No heuristic is deleted — retired entries transition to dormant, not erased

### Recursive Reintegration Tests
- Failed outcome triggers replay of original context package
- Missed trigger set is correctly identified against replayed scenario
- Misfired Carat is identified when scenario gate would have blocked it
- Corrective actions are recorded in the reintegration result
- Archive is updated after reintegration completes

### Lifecycle Tests
- `monitoring` → `candidate_detected` on trigger fire
- `candidate_detected` → `suppressed` on overload buffer activation
- `candidate_detected` → `escalated` on unresolved governance ambiguity
- `active` → `escalated` on PRP-01 invocation
- Every state transition emits `state_transition` audit event

---

## Relationship to Companion Specs

| Document | Relationship |
|---|---|
| `SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md` | Defines the four governance components this spec implements at runtime |
| `REFLEX_AND_ACTIVATION_SYSTEM.md` | Defines the five-stage detection cascade; this spec governs the stack that protects that cascade |
| `HEURISTIC_CODING_SYSTEM.md` | BDR-01 fires here; Heuristic Coding receives the promotion candidate |
| `RECURSIVE_ANALYSIS_MODEL.md` | RA Mode 2 performs heuristic performance audits; Hygiene System performs structural health checks; complementary, not redundant |
| `CARAT_REGISTRY_STANDARD.md` | Defines Carats; this spec defines the interlocks that govern their co-activation |
| `AMBIENT_TRIGGER_REGISTRY.md` | Ambient triggers prime attentional posture; Support Stack reflex triggers govern runtime logic integrity; different layers, different jobs |

---

## Design Principle

> The Support Stack is not optional. It is the difference between a system that reasons correctly in a demo and a system that reasons correctly in production, under adversarial conditions, over time.

Governance that cannot protect itself from drift, manipulation, and silent degradation is not governance. It is the appearance of governance.

The two hardcoded system reflexes — PRP-01 and BDR-01 — are the clearest expression of this principle in runtime form. PRP-01 ensures the system learns from failure rather than patching it. BDR-01 ensures the system hunts for value rather than waiting to be pointed at it.

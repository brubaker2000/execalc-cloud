# STAGE_8_GOVERNED_JUDGMENT_PIPELINE.md

## Status
Spec — not yet built

## Owner
Build / Architecture

## Stage Number
Stage 8

## One-Line Purpose
Stage 8 is where the code becomes what the docs say it is: the first LLM call enters the decision path, governed by the Reflex and Activation System, evaluated by the Prime Directive gate, and reviewed by Recursive Reintegration before reaching the operator.

---

## The Gap Stage 8 Closes

From the Capability Presence Matrix:

> "There is no LLM call in the decision path. The governed cognitive operating system described in the doctrine runs on a deterministic template engine."

Stage 8 replaces that template engine with a governed judgment pipeline. The endpoint shapes stay the same. The tenant isolation stays the same. What changes is everything between input receipt and output delivery.

**Before Stage 8:** Input → templates → structured output  
**After Stage 8:** Input → Reflex/Activation cascade → LLM judgment → Prime Directive gate → Reintegration check → structured output

---

## Sub-Stage Breakdown

Stage 8 is delivered in four sequential sub-stages. Each sub-stage has a clear exit condition. No sub-stage begins until the previous one passes its exit condition.

---

### Sub-Stage 8A: Support Stack Phase 4 — Condition-Aware Boundary Decisions

**What it builds:** The four named Support Stack components replacing the always-allow-true scaffolding in `support_stack.py`.

**Current state:** `ReflexRegistry` is in-memory. `ReflexGateDecision` returns allow-all. `BoundaryDecision` always returns `allowed=True`.

**Deliverables:**

1. **Recursive Audit Triggers**
   - At each reasoning step, evaluate output against active governance frameworks
   - Deviation detection: fires before output reaches operator
   - Produces audit record: trigger fired / deviation detected / resolution (blocked / flagged / passed)

2. **Compromise-Awareness Reflexes**
   - Scan inputs for: leading framing, false premises, authority appeals, contradictions with established context, selective suppression
   - Distinguish between legitimate contextual updates and adversarial/inadvertent bias injection
   - Response: flag with pattern description, request confirmation before proceeding
   - Audit every detection event regardless of resolution

3. **Runtime Validation Protocols**
   - Structural integrity check at each reasoning step (not a re-run — a constraint check)
   - Step fails validation: flagged, does not automatically propagate
   - Distinct from Recursive Reintegration (step-level vs. output-level)

4. **Governance Enforcement Drivers**
   - Session initialization: confirm all governance frameworks loaded and active
   - Mid-session: verify no configuration drift has altered governance state
   - Session close: preserve governance state for next session
   - Enforcement hierarchy enforced: Compliance > Prime Directive > Core 7 > Carats > Operator preferences

**Files affected:** `src/service/decision_loop/support_stack.py` (primary rebuild)

**Exit condition:**
- All four components have passing unit tests
- Compromise-awareness fires correctly on a crafted adversarial input
- Boundary decisions return condition-aware results (not always-allow)
- All component events appear in the session audit trail
- Existing governed tests continue to pass

---

### Sub-Stage 8B: Five-Stage Reflex and Activation Cascade (Stages 1–4)

**What it builds:** The detection and context-assembly pipeline that fires before any LLM call. This covers Stages 1–4 of the five-stage cascade defined in `REFLEX_AND_ACTIVATION_SYSTEM.md`. Stage 5 (the LLM call itself) is sub-stage 8C.

**Deliverables:**

1. **Stage 1 — Signal Extraction** (labor tier)
   - Scan input for signals matching activation signal library
   - Each of the 25 scenarios carries a signal list (from `SCENARIO_REGISTRY.md`)
   - Output: scored list of matched signals with source text references and confidence
   - Model tier: Haiku-class or rule-based (extraction, not judgment)

2. **Stage 2 — Scenario Detection**
   - Score each scenario against matched signals
   - Primary scenario + secondary scenario with confidence scores
   - 0.70 confidence threshold: below → ambiguity flag raised
   - Ambiguity flag: surface top 2–3 candidates to operator; request clarification before proceeding
   - Default fallback: Scenario 21 (Opportunity Discovery) as broadest safe container
   - Model tier: labor for simple cases; Premium when signals ambiguous or contradictory

3. **Stage 3 — Reflex Gate**
   - Load reflex set for detected scenario
   - Four reflex types: diagnostic / warning / framework / posture
   - Suppression check: if input signals indicate a reflex is not applicable, suppress it
   - Starter reflex registry from `REFLEX_AND_ACTIVATION_SYSTEM.md` is the initial dataset
   - Rule-based: no model call needed for standard cases

4. **Stage 4 — Activation Pathway**
   - Assemble context package in priority order:
     1. Compliance constraints (if any cartridges active)
     2. Prime Directive frame
     3. Active Carats (none in Stage 8; Carat system is Stage 9)
     4. Scenario logic
     5. Active reflexes
     6. EKE corpus entries for this scenario (seed corpus; full corpus is Stage 9)
     7. Operator memory (none in Stage 8; memory runtime is Stage 9)
     8. Session context
   - Output: fully assembled context package ready for Stage 5

**New file:** `src/service/decision_loop/reflex_activation.py` — the five-stage cascade

**Exit condition:**
- Given a sample input, the cascade correctly identifies the primary scenario
- Ambiguity detection triggers correctly when signals are below 0.70
- Context package is assembled with correct priority order
- Full audit record produced: signals matched, scenarios scored, reflexes activated, corpus entries loaded
- Cascade does not call the LLM (that is sub-stage 8C)

---

### Sub-Stage 8C: First LLM Call — The Judgment Call

**What it builds:** The actual model call that replaces the template engine. This is Stage 5 of the Reflex and Activation cascade.

**The model receives:**
- The assembled context package from sub-stage 8B
- The operator's input
- The output template for the detected scenario

**Model tier:** Premium (Opus-class) — this is judgment, not labor.

**Deliverables:**

1. **LLM client integration** (model abstraction layer)
   - Route judgment calls to Opus-class model
   - Route labor calls (extraction, summarization) to Haiku-class
   - Model selection is governed by trust tier, not cost preference (invariant)

2. **Structured output enforcement**
   - Model output must conform to the scenario's output template
   - Every claim must reference the context that supports it
   - Output is not free-form text — it is a structured decision artifact

3. **Prompt assembly**
   - Context package → prompt construction
   - Output template → response format specification
   - No "blank page" prompting — the model reasons within the prepared context

4. **Prime Directive evaluation gate** (runs after judgment call, before delivery)
   - All three PD lenses must appear and be evaluated
   - Gate verdict: pass / flag / block
   - Blocked output triggers a revised judgment call, not a silent failure

5. **Replace template engine**
   - `src/service/decision_loop/engine.py` currently uses string templates
   - Stage 8C replaces the template logic with the LLM call path
   - Endpoint contracts (`POST /decision/run`) do not change — only what happens inside them

**Exit condition:**
- `POST /decision/run` produces an output from an actual LLM call
- Prime Directive gate fires on every output; gate verdict appears in audit trail
- All three PD lenses present in every output
- Model tier routing correct: judgment → Opus, labor → Haiku
- All existing endpoint tests pass (output shape unchanged, content richer)

---

### Sub-Stage 8D: Recursive Reintegration + Full Audit Trail

**What it builds:** The closing loop — the output review cycle that checks the judgment call's output against the governing logic before it reaches the operator, plus the full audit trail stitching every component event together.

**Deliverables:**

1. **Recursive Reintegration** (Core 7 Framework 7)
   - Five checks against the complete output:
     - Prime Directive alignment (all three lenses present and evaluated)
     - Polymorphia consistency (secondary dimensions acknowledged if identified)
     - Memory consistency (output consistent with active admitted memory — moot in Stage 8 but gate must exist)
     - Corpus anchor integrity (citations accurate)
     - Compliance constraint adherence (if cartridges active)
   - Verdict: pass / flag / block
   - Flag: output proceeds with disclosed reintegration note
   - Block: revised judgment call triggered
   - Operator disclosure: transparent when reintegration flagged or blocked

2. **Full session audit trail**
   - Every event from every component in every sub-stage must appear
   - Audit record schema (per `SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md` audit requirements)
   - Decision artifact includes: which scenario detected, which reflexes fired, which corpus entries loaded, which PD lenses evaluated, reintegration verdict
   - Audit trail is reconstructable: given the audit record, the full reasoning path can be traced

3. **Decision artifact finalization**
   - Output format: structured decision artifact (not LLM response text)
   - Required fields: executive summary, confidence, sensitivity, next actions, traceability metadata, audit trail reference
   - Decision artifact persisted to `execution_records`

**Exit condition:**
- Every component event in the session appears in the audit trail
- Reintegration check fires on every output with five check results recorded
- Decision artifacts are structured, persisted, and reconstructable
- A new agent reading the audit trail can reconstruct why a specific output was produced
- Full regression suite passes

---

## Stage 8 Exit Condition (Complete)

Stage 8 is complete when:

1. `POST /decision/run` produces an output from a real LLM call governed by the full cascade
2. The five-stage Reflex and Activation cascade runs on every input
3. The Prime Directive gate fires on every output
4. Recursive Reintegration fires on every output
5. Every component event appears in the session audit trail
6. The Support Stack provides condition-aware boundary decisions (not allow-all)
7. All existing governed tests pass
8. Model tier routing is correct and invariant-compliant

**What Stage 8 does not deliver** (these are Stage 9):
- EKE corpus fully loaded and dynamically activated
- Memory admission pipeline
- Carat system active
- Compliance cartridges toggleable
- Cross-session persistent memory

---

## Files Primarily Affected

| File | Change |
|---|---|
| `src/service/decision_loop/support_stack.py` | Rebuild — Phase 1 scaffolding → four named components |
| `src/service/decision_loop/engine.py` | Replace template engine with LLM call path |
| `src/service/decision_loop/reflex_activation.py` | New — five-stage cascade |
| `src/service/decision_loop/reintegration.py` | New — Recursive Reintegration cycle |
| `src/service/decision_loop/audit_trail.py` | New — session audit trail stitching |
| `src/service/decision_loop/model_router.py` | New — labor vs. judgment tier routing |

---

## Spec Dependencies

Stage 8 is fully specced. All required design docs exist:

| Component | Spec Location |
|---|---|
| Support Stack four components | `docs/architecture/SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md` |
| Five-stage cascade | `docs/architecture/REFLEX_AND_ACTIVATION_SYSTEM.md` |
| 25-scenario registry | `docs/architecture/SCENARIO_REGISTRY.md` |
| Prime Directive model | `CLAUDE.md §4`, `docs/architecture/CORE_7_REMEDIATION_DIRECTIVE.md` |
| Recursive Reintegration | `docs/architecture/RECURSIVE_REINTEGRATION_MODEL.md` |
| Multi-model routing invariant | `CLAUDE.md §7`, `docs/architecture/SUBSTRATE_ROUTING_AND_MODEL_TIERING_DOCTRINE.md` |
| Audit requirements | `docs/architecture/SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md` §Audit Requirements |

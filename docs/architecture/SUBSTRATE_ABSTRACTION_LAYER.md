# Substrate Abstraction Layer

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-20  
**Authority:** Execalc Product Standards

---

## I. Purpose

This document defines the Substrate Abstraction Layer — the single system component responsible for all LLM provider interactions — and the Substrate Selection Policy that governs which model tier is used for which class of call.

The substrate abstraction layer is a non-negotiable architectural requirement. It is the mechanism by which Execalc remains provider-agnostic, acquisition-ready, and cost-governed simultaneously.

---

## II. The Central Principle

**Execalc governs. The substrate renders.**

The governance layer — the scenario envelope, GAQP corpus activation, seven-test admission gate, DecisionReport schema, Execution Boundary Engine — does the structural work of turning an executive situation into a governed reasoning frame.

By the time a call reaches the substrate, most of the intelligence has already been applied. The substrate is not being asked to figure anything out. It is being asked to render structured output against a prepared frame.

This principle has a direct cost implication: a highly-governed call does not need the most capable (most expensive) model. It needs reliable instruction-following and clean structured output generation. These are properties available at lower model tiers.

The routing variable is therefore not turn type alone. It is **governance coverage** — how much of the reasoning work Execalc has already done before the substrate is invoked.

---

## III. The Substrate Abstraction Layer

### What it is

A single, isolated system component that:

- Accepts a normalized `SubstrateRequest` object from the orchestration layer
- Selects the appropriate provider and model tier based on the selection policy
- Formats the request per provider API requirements
- Executes the call
- Normalizes the response back to a `SubstrateResponse` object
- Returns the normalized response to the orchestration layer

### What it is not

- It is not part of the governance layer
- It is not part of the GAQP corpus
- It is not part of the orchestration rail
- It does not make routing decisions based on business logic — it receives a routing signal from the orchestration layer and executes against it

### Boundary rule

No component outside the substrate abstraction layer may reference a specific LLM provider, model name, or provider API. All model calls flow through this layer. No exceptions.

This boundary is what makes provider swaps non-disruptive and acquisition integration clean.

---

## IV. The Normalized Interface

### SubstrateRequest

```
SubstrateRequest:
  call_class: SubstrateCallClass        # see Section V
  governance_coverage: CoverageLevel    # see Section VI
  system_prompt: str
  user_turn: str
  output_schema: dict | None            # JSON schema if structured output required
  max_tokens: int
  tenant_id: str
  call_id: str                          # for audit trail
  override_tier: ModelTier | None       # explicit override, see Section VII
```

### SubstrateResponse

```
SubstrateResponse:
  content: str
  structured_output: dict | None
  provider: str                         # which provider was used
  model: str                            # which model was used
  input_tokens: int
  output_tokens: int
  call_id: str
  latency_ms: int
```

The orchestration layer never sees a provider name or model name except as audit metadata in the response. It sees only the normalized content.

---

## V. Substrate Call Classes

Call classes are set by the orchestration layer based on turn classification. The substrate abstraction layer uses call class as the primary routing input.

| Call Class | Description | Source Turn Type |
|---|---|---|
| `CONVERSATIONAL` | Freeform exchange with no governed output required | conversational |
| `CLASSIFICATION` | Turn type detection, scenario framing, intent interpretation | detection / framing |
| `CORPUS_RETRIEVAL` | Activating and ranking GAQP claims for a scenario | evidence-seeking |
| `STRUCTURED_SYNTHESIS` | Generating a DecisionReport against a fully-governed frame | decision-seeking |
| `ACTION_FRAMING` | Generating an ActionProposal against a structured scenario | action-proposing |
| `EXECUTION_GATE` | Any call where EBE outcome is implicated | execution-seeking |
| `AUDIT_NARRATION` | Generating human-readable audit summaries from structured records | post-decision |

---

## VI. Governance Coverage Levels

Governance coverage is assessed by the orchestration layer and passed to the substrate abstraction layer as a signal. It reflects how much of the reasoning frame has been constructed before the substrate is invoked.

| Coverage Level | Meaning |
|---|---|
| `FULL` | Scenario envelope complete, GAQP corpus activated, output schema defined, downstream validation active |
| `PARTIAL` | Some governance applied but frame is incomplete — novel scenario, thin corpus match, or no output schema |
| `MINIMAL` | Little to no governance scaffolding — freeform input, no corpus match, no schema |

---

## VII. Substrate Selection Policy

The selection policy is a function of call class and governance coverage. The output is a model tier.

| Call Class | Coverage: FULL | Coverage: PARTIAL | Coverage: MINIMAL |
|---|---|---|---|
| `CONVERSATIONAL` | Economy | Economy | Economy |
| `CLASSIFICATION` | Economy | Standard | Standard |
| `CORPUS_RETRIEVAL` | Economy | Standard | Standard |
| `STRUCTURED_SYNTHESIS` | Standard | Capable | Capable |
| `ACTION_FRAMING` | Standard | Capable | Capable |
| `EXECUTION_GATE` | Capable | Capable | Capable |
| `AUDIT_NARRATION` | Economy | Economy | Standard |

**Model tiers (provider-agnostic):**

| Tier | Characteristic | Current Anthropic Mapping | Current Gemini Mapping |
|---|---|---|---|
| `Economy` | Fast, cheap, structured-output reliable, instruction-following on well-formed prompts | Claude Haiku | Gemini Flash |
| `Standard` | Solid reasoning, reliable on complex instructions, good schema adherence | Claude Sonnet | Gemini Pro |
| `Capable` | Best available reasoning, calibrated uncertainty, strongest long-context coherence | Claude Opus | Gemini Ultra |

Provider mappings are configuration, not code. Updating a provider or swapping a tier's backing model requires no code change — only a configuration update in the substrate abstraction layer.

---

## VIII. Hard Override Rules

The following conditions force `Capable` tier regardless of call class or coverage level:

1. **Any call where EBE outcome is implicated** — execution gating is never routed below Capable
2. **Tenant governance posture is `ELEVATED` or above** — tenant-level policy can mandate minimum tier
3. **Scenario risk classification is `HIGH` or `CRITICAL`** — set by the Detection and Framing Layer
4. **Explicit `override_tier` set on the SubstrateRequest** — orchestration layer may always escalate; it may never de-escalate below policy minimum

---

## IX. Why Economy Tier Is Sufficient for Governed Calls

The following properties of the Execalc runtime reduce dependence on model capability for well-governed calls:

**The scenario envelope does the framing.** A smaller model does not need to infer what kind of situation it is reasoning about. The frame is constructed and handed to it.

**The GAQP corpus does the knowledge retrieval.** A smaller model does not need to recall domain knowledge. Relevant admitted claims are activated and included in the prompt.

**The output schema does the structure enforcement.** A smaller model does not need to decide what to output. The schema defines every field. The task is slot-filling, not synthesis.

**The seven-test admission gate does the quality filtering.** Outputs that fail the gate are not persisted. A smaller model's occasional schema drift is caught downstream, not silently accepted.

**The Execution Boundary Engine does the safety gate.** No action is authorized by LLM output alone. A smaller model cannot bypass EBE by generating a permissive-sounding output.

---

## X. Where Capability Still Matters

Economy and Standard tiers are insufficient when:

- **The prompt is long and deeply nested** — cheaper models drift on complex, multi-section system prompts
- **The scenario is genuinely novel** — no corpus match, no prior governance frame, first-encounter situations
- **Calibrated uncertainty is required** — cheaper models overstate confidence and fail to flag when they are outside their competence
- **The call must detect governance gaps** — recognizing when a situation falls outside the scaffold requires the model to reason about the limits of the scaffold itself

These conditions map precisely to the call classes and coverage levels that route to Capable tier in the selection policy above.

---

## XI. Provider Agnosticism Discipline

The following rules enforce provider agnosticism across the codebase:

1. No import, reference, or string literal naming a specific LLM provider may exist outside `src/service/substrate/`
2. All provider API keys are environment variables injected at runtime, never hardcoded
3. Provider selection is configuration-driven — the active provider per tier is set in `substrate_config` and loaded at startup
4. Model version pinning is per-configuration, not per-call — the orchestration layer never specifies a model version
5. Adding a new provider requires only: a new provider adapter in `src/service/substrate/providers/`, registration in `substrate_config`, and tier mapping entries

This discipline ensures that swapping the substrate — for cost, capability, or acquisition integration reasons — is a configuration and adapter change, not a codebase change.

---

## XII. Implementation Scope (Not Yet Built)

The substrate abstraction layer is specified here but not yet implemented. Current code calls LLM providers directly from the orchestration layer.

**Implementation requirements when this stage is scheduled:**

- `src/service/substrate/` — new module
  - `interface.py` — `SubstrateRequest`, `SubstrateResponse`, `SubstrateCallClass`, `CoverageLevel`, `ModelTier`
  - `router.py` — selection policy logic
  - `providers/` — one adapter per provider (`anthropic.py`, `google.py`, etc.)
  - `config.py` — tier-to-provider-to-model mapping, loaded from environment
- Orchestration layer refactored to emit `SubstrateRequest` objects rather than calling providers directly
- All existing provider references in orchestration removed and routed through the new layer
- Audit trail extended to capture `provider`, `model`, `input_tokens`, `output_tokens` per call

This implementation does not change any governance, GAQP, or decision loop behavior. It is a structural refactor of the call path only.

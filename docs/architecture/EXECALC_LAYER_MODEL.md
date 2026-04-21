# EXECALC_LAYER_MODEL.md

## Status
Canonical v1.0

## Owner
Architecture / Product

---

## Purpose

This document defines the macro three-layer positioning model for Execalc — how the system situates itself in the broader AI value chain.

This is not a replacement for the Strategic Mesh. The Strategic Mesh describes the internal architecture of the upstream layer. This document describes where that layer sits relative to the LLM and the integration surface — and why that positioning matters.

---

## The Three-Layer Model

```
──────────────────────────────────────────────
  UPSTREAM — Executive Intelligence Layer (EIL)
──────────────────────────────────────────────
  Governance Stack       Security Stack
  Logic Stack            Reflex Engine
  Diagnostics Library    Executive Knowledge Engine
  Tenant Frameworks      Memory Architecture
──────────────────────────────────────────────
  MIDSTREAM — Substrate Layer (LLM / Core AI)
──────────────────────────────────────────────
  GPT / Claude / Gemini / Llama
  Embeddings
  Vector Reasoning
  Predictive Patterns
──────────────────────────────────────────────
  DOWNSTREAM — Exterior Integration Layer
──────────────────────────────────────────────
  Dashboards             APIs
  Zapier Drivers         CRM Connectors
  Data Pipelines         File Storage Bridges
──────────────────────────────────────────────
```

---

## Upstream — The Executive Intelligence Layer (EIL)

The EIL is the governed intelligence architecture that sits above the substrate. It is what makes Execalc different from raw LLM access.

Any organization can access a capable LLM. What they cannot access off the shelf is a system that governs what the LLM receives, enforces alignment with organizational objectives, accumulates institutional intelligence, and protects the reasoning environment from drift and manipulation.

That system is the EIL.

> The LLM is the engine. The EIL is the product.

### The Eight Components

| EIL Component | What It Does | Canonical Doc |
|---|---|---|
| **Governance Stack** | Runtime operational controls that protect reasoning fidelity under real-world conditions — audit triggers, compromise-awareness reflexes, runtime validation | `SUPPORT_STACK_OPERATIONAL_CONTROL_LAYER.md` |
| **Logic Stack** | The Core 7 governance frameworks — the permanent logical architecture through which all information must pass before it becomes a recommendation | `EXECALC_COGNITIVE_ENGINE_ARCHITECTURE.md` |
| **Security Stack** | Tenant isolation, audit controls, breach prevention — controls who sees what and what happens to sensitive information | `STRATEGIC_MESH_ARCHITECTURE.md §Layer 3` |
| **Reflex Engine** | Automatic runtime responses to classified signals — fires before the operator is asked, routes to the right logic, enforces activation discipline | `REFLEX_AND_ACTIVATION_SYSTEM.md` |
| **Diagnostics Library** | Named callable analytical procedures for runtime state inspection and system introspection | `EXECALC_REASONING_STACK.md` |
| **Executive Knowledge Engine** | Knowledge activation — selects which corpus, frameworks, carats, and thinker nuggets enter the reasoning context for this specific situation | `EXECUTIVE_KNOWLEDGE_ENGINE_STRATA.md` |
| **Tenant Frameworks** | Operator-specific compliance constraints, cartridges, and scoped knowledge that override or extend the baseline | `COMPLIANCE_CARTRIDGE_ARCHITECTURE.md` |
| **Memory Architecture** | Governed accumulation of institutional intelligence — not a transcript; a claim store with admission criteria | `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md` |

The internal architecture of how these eight components interoperate is defined in the Strategic Mesh: `STRATEGIC_MESH_ARCHITECTURE.md`.

---

## Midstream — The Substrate Layer

The substrate layer is the raw prediction engine: large language models and their supporting infrastructure.

```
GPT-5 / Claude / Gemini / Llama
Embeddings
Vector Reasoning
Predictive Patterns
```

The substrate is powerful. It is also ungoverned, stateless, and indifferent to organizational context. Left alone, it produces plausible-sounding output with no accountability to the operator's actual interests.

**The substrate is not the product. It is the raw material the EIL governs.**

Execalc is model-agnostic. The substrate can be swapped. The EIL does not change when the underlying model does.

---

## Downstream — The Exterior Integration Layer

The downstream layer is the integration surface: the channels through which governed outputs reach the places operators already work.

```
Dashboards         APIs
Zapier Drivers     CRM Connectors
Data Pipelines     File Storage Bridges
```

**The judgment core does not reach out. The Exterior Integration Layer delivers context in and governed results out.**

This separation is architectural and intentional. The EIL should never become entangled in the mechanics of how outputs are delivered or how data arrives. Integration complexity must not contaminate reasoning fidelity.

This principle is established in the Exterior Stack doctrine: `docs/build_plan/BUILD_DOCTRINE_ADDENDUM.md §The Exterior Stack`.

---

## Why This Frame Matters

Most AI systems described to investors and buyers operate on a one-layer model:

```
Prompt → LLM → Response
```

The three-layer model makes visible what is architecturally true and competitively important:

1. **Execalc is upstream.** It governs the reasoning before the LLM produces output — not after. It is not a wrapper or a formatter. It is a governance layer.

2. **The LLM is in the middle.** Not at the top. The substrate is replaceable. The EIL is the durable asset.

3. **Integration is downstream.** Output delivery is a solvable engineering problem. The defensible value is in the upstream architecture.

This frame answers the investor objection — "couldn't you just use ChatGPT?" — with architectural clarity: ChatGPT is the midstream substrate. Execalc is the upstream layer that governs it.

---

## Relationship to Existing Architecture Docs

| Document | Relationship |
|---|---|
| `STRATEGIC_MESH_ARCHITECTURE.md` | Internal architecture of the EIL — the three-layer breakdown of what's inside the upstream layer |
| `EXECALC_COGNITIVE_ENGINE_ARCHITECTURE.md` | The Logic Stack in detail — the Core 7 runtime loop |
| `REFLEX_AND_ACTIVATION_SYSTEM.md` | The Reflex Engine in detail |
| `EXECUTIVE_KNOWLEDGE_ENGINE_STRATA.md` | The EKE in detail — knowledge strata and activation |
| `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md` | Memory Architecture in detail |
| `JUDGMENT_SUPERSTRATE_POSITIONING.md` | Competitive positioning — judgment superstrate vs orchestration superstrate |
| `docs/build_plan/BUILD_DOCTRINE_ADDENDUM.md` | Exterior Stack separation doctrine |

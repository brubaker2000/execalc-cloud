# CAPABILITY_PRESENCE_MATRIX.md

## Purpose
This document maps every governed capability in the Execalc architecture against its actual current code status.

It exists because the build plan tracks stages, not capabilities. A completed stage can create the false impression that the underlying capability is production-ready when it may only be stubbed or documented. This matrix provides the honest picture.

## Status Levels

| Level | Meaning |
|---|---|
| `spec_only` | Doctrine or design doc exists. No runtime code. |
| `stubbed` | Placeholder code exists. Returns defaults or no-ops. Real logic absent. |
| `scaffolded` | Structure and interfaces exist. Logic is incomplete or hardcoded. |
| `implemented` | Working logic present. Not yet wired to governance chain. |
| `tested` | Passing unit or integration tests. Behavior verified. |
| `governed` | Tested + connected to governance chain (Prime Directive, audit trail, tenant boundary). |

---

## 1. Infrastructure and Plumbing

| Capability | Status | Notes |
|---|---|---|
| Tenant isolation per request | `governed` | Enforced on every route; tested |
| Actor context lifecycle | `governed` | Guaranteed setup/cleanup; tested |
| Auth — API key enforcement | `governed` | Fails closed without key |
| Dev harness safety gate | `governed` | Deny-by-default; Cloud Run locks to prod |
| Postgres driver (lazy-loaded) | `tested` | Lazy import prevents test failures without DB |
| Execution record persistence | `tested` | `execution_records` table; end-to-end proven |
| Tenant persistence | `tested` | `tenants` table; lifecycle covered |
| Connector framework | `tested` | echo + null connectors; scope enforcement proven |
| Cloud Run deploy gate | `tested` | Gate script verified; deployed revision confirmed |

---

## 2. Decision Loop

| Capability | Status | Notes |
|---|---|---|
| `POST /decision/run` endpoint | `governed` | Tenant-scoped, persisted, tested |
| Scenario input model | `scaffolded` | Fields exist including EKE-forward stubs; no validation against scenario registry |
| Scenario classification / detection | `stubbed` | Caller supplies `scenario_type` manually; no runtime detection logic |
| Prime Directive evaluation | `scaffolded` | String templates keyed on objective type; not actual governed evaluation; no LLM |
| Polymorphia fields | `scaffolded` | Actors/incentives/asymmetries generated from templates; no multi-perspective reasoning engine |
| Tradeoff analysis | `scaffolded` | Hardcoded upside/downside lists; scenario-type-switched strings |
| Confidence scoring | `stubbed` | Returns `"medium"` or `"unknown"` based on missing fields; no real scoring model |
| LLM integration in decision loop | **`spec_only`** | **No LLM call exists anywhere in the decision path.** |
| Sensitivity variable detection | `implemented` | Checks required fields by scenario type; functional but narrow |
| Next actions generation | `scaffolded` | Templated list; not scenario-aware beyond objective type |
| Execution trace / audit trail | `scaffolded` | Records what ran; does not yet record which frameworks were activated or why |

---

## 3. Decision Journal and Retrieval

| Capability | Status | Notes |
|---|---|---|
| `GET /decision/<id>` | `governed` | Tenant-scoped; tested |
| `GET /decision/recent` | `governed` | Tenant-scoped; limit param; tested |
| `GET /decision/compare` | `tested` | Deterministic compare engine; tested; Stage 7B |
| Decision lineage / reconstructability | `spec_only` | GAQP Principle 10; no runtime implementation |

---

## 4. Support Stack

| Capability | Status | Notes |
|---|---|---|
| Reflex registry | `stubbed` | In-memory; registers reflexes but gate always returns allow-all |
| Reflex gate | `stubbed` | Phase 1 default: allows everything; no policy logic |
| Boundary decision | `stubbed` | Always returns `allowed=True`; placeholder checks only |
| Procedure plan | `scaffolded` | Generates step list; steps are not actually executed as discrete governed operations |
| Condition-aware boundary decisions | `spec_only` | Support Stack Phase 4; listed as NOW in NEXT_ACTIONS.md; not yet built |
| Reflex priority ordering | `spec_only` | GAP-RJ identified; no implementation |
| Signal suppression rules | `spec_only` | GAP-RJ identified; no implementation |

---

## 5. Memory System

| Capability | Status | Notes |
|---|---|---|
| Memory admission pipeline | `spec_only` | Full doctrine in PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md; zero runtime code |
| Six-test admission filter | `spec_only` | Fully specified; not implemented |
| Memory promotion ladder | `spec_only` | Observed → Candidate → Admitted → Weighted → Canonical; not implemented |
| Memory candidate flagging | `spec_only` | Betty spec defines the on-ramp; no runtime pipeline behind it |
| Active vs. dormant memory state | `spec_only` | Defined in doctrine; no storage model implemented |
| Memory classification dimensions | `spec_only` | family/source/activation state/scope/confidence/time horizon/sensitivity; not implemented |
| Temporal decay model | `spec_only` | Identified in Governance Gap Register Wave 1; not specified in detail yet |
| Session-to-persistent memory boundary | `spec_only` | Gap identified; no implementation |
| `ADMIT_MEMORY()` formula | `spec_only` | Qualitative Formula Library concept; no runtime |
| `REVISE()` formula | `spec_only` | Same |
| Memory runtime scaffolding (Stage 8B.8) | `spec_only` | Listed as NEXT in NEXT_ACTIONS.md |

---

## 6. Executive Knowledge Engine (EKE)

| Capability | Status | Notes |
|---|---|---|
| EKE corpus schema | `spec_only` | EXECUTIVE_KNOWLEDGE_ENGINE_CORPUS_SCHEMA.md written; no storage or loader |
| Monolith (synthesized pattern engine) | `spec_only` | Strata doc defines it; seed dataset exists but not committed or classified |
| Thought Leadership Nuggets | `spec_only` | Defined in strata; seed dataset unclassified |
| Execalc runtime cartridges | `spec_only` | Schema defined; no cartridge objects exist in repo |
| Client cartridges | `spec_only` | Architecture defined; no implementation |
| Scenario routing to EKE | `spec_only` | No activation pathway code |
| `FRAME()` formula | `spec_only` | Defined; no runtime |
| `THINKER()` formula | `spec_only` | Defined; no runtime |
| `SYNTHESIZE()` formula | `spec_only` | Defined; no runtime |
| EKE Thinker registry | `spec_only` | Identified as required follow-on spec; not yet written |
| Heuristic object classification | `spec_only` | Classification model just written; reclassification of seed dataset not started |

---

## 7. Carat System

| Capability | Status | Notes |
|---|---|---|
| Carat registry standard | `spec_only` | CARAT_REGISTRY_STANDARD.md written and committed |
| Carat activation pathway | `spec_only` | Runtime cascade defined in spec; no code |
| Carat arbitration rules | `spec_only` | Identified as follow-on spec; not written |
| Carat conflict handling | `spec_only` | Doctrine written; no implementation |
| Carat audit trail | `spec_only` | Requirements written; no implementation |
| Any actual Carat objects | `spec_only` | Zero Carat instances exist in the corpus |

---

## 8. Governance Layer

| Capability | Status | Notes |
|---|---|---|
| Prime Directive — formal two-tier model | `spec_only` | Fully documented; not enforced in runtime |
| Prime Directive runtime enforcement | `spec_only` | PRIME_DIRECTIVE_RUNTIME_ENFORCEMENT.md not yet written (Tier 1 remediation) |
| GAQP principles enforcement | `spec_only` | 10 principles defined; none enforced in code |
| Governed claim taxonomy | `spec_only` | 13 claim types defined; no runtime classification |
| Six-test admission filter (claims) | `spec_only` | Fully specified; not implemented |
| Input normalization contract | `spec_only` | Governance Gap Register Wave 1; not yet specified |
| Evidence and provenance model | `spec_only` | Governance Gap Register Wave 1; not yet specified |
| Synthesis provenance chain | `spec_only` | Gap identified; not specified |
| Audit trail format spec | `spec_only` | Gap identified; not specified |

---

## 9. Multi-Model Routing

| Capability | Status | Notes |
|---|---|---|
| Model tier doctrine | `spec_only` | SUBSTRATE_ROUTING_AND_MODEL_TIERING_DOCTRINE.md written |
| Premium tier for judgment operations | `spec_only` | Invariant defined; no routing code |
| Labor tier for summarization/extraction | `spec_only` | Invariant defined; no routing code |
| Model selection at runtime | `spec_only` | No model calls exist yet — moot until LLM is wired in |

---

## 10. Interface Modes

| Capability | Status | Notes |
|---|---|---|
| Betty Executive Secretary Mode | `spec_only` | Full spec written; zero runtime code |
| Betty capture object schema | `spec_only` | Identified as follow-on spec; not written |
| Betty memory candidate handoff | `spec_only` | Identified as follow-on spec; not written |
| Named activation (wake word routing) | `spec_only` | Concept defined; no implementation |

---

## 11. Qualitative Formula Library

| Capability | Status | Notes |
|---|---|---|
| Full formula taxonomy | `spec_only` | 30+ formulas named and categorized |
| Any formula runtime implementation | `spec_only` | None. This is Stage 9+ territory. |

---

## Summary Assessment

| Layer | Overall Status |
|---|---|
| Infrastructure / Plumbing | **Solid.** Production-grade. |
| Tenant / Auth / Persistence | **Solid.** Governed and tested. |
| Decision Loop endpoints | **Working** — request handling is real; judgment is templates. |
| Decision Loop intelligence | **Does not exist yet.** No LLM, no governed reasoning. |
| Support Stack | **Stubbed.** Runs but allows everything by default. |
| Memory System | **Entirely doc-only.** No runtime existence. |
| EKE / Corpus | **Entirely doc-only.** No runtime existence. |
| Carat System | **Entirely doc-only.** No runtime existence. |
| Governance Enforcement | **Entirely doc-only.** No enforcement code anywhere. |
| Multi-Model Routing | **Moot until LLM is wired in.** |
| Qualitative Formula Library | **Concept only.** Far future build scope. |

---

## The Critical Gap

The single largest gap between what the docs describe and what the code does:

**There is no LLM call in the decision path.**

The governed cognitive operating system described in the doctrine runs on a deterministic template engine. The templates are well-structured and architecturally correct in their shape — they produce Prime Directive fields, Polymorphia fields, tradeoffs, sensitivity. But they are strings, not reasoning.

Stage 8 is where the code becomes what the docs say it is.

---

## Maintenance Note

This matrix should be updated whenever:
- a capability moves from one status level to the next
- a new capability is added to the architecture
- a stage is completed

It is not a changelog. It is a current-state snapshot. Date of last update should be maintained at the top of the file.

**Last updated:** 2026-04-13

# Execalc Product Vision

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-06  
**Authority:** Execalc Build Authority

---

## Category Statement

Execalc is a **governed execution platform**. It operates one layer above models, tools, agents, and data — supplying the judgment, governance, memory, and permission structure that raw AI capability cannot provide for itself.

Execalc treats the LLM as a language substrate, not the system.

---

## The Unified Model

Execalc is the platform. IFD and Bridge are governed execution containers that Execalc runs. You need an Execalc seat to have either. They are not standalone products — they are the platform's interfaces to the world.

The platform's core promise, stated simply:

**Only signal gets through.**

---

## The Strategic Position: Agents, MCP, and Execalc

The market is flooding with agents and MCP servers. That creates power, but also chaos.

- **Agents provide labor.** They plan, call tools, coordinate subtasks, and execute multi-step work. They should not independently decide what the organization values, who has authority, or whether a tradeoff is strategically acceptable.
- **MCP provides access.** It is the standard plumbing connecting AI systems to external tools, files, databases, and APIs.
- **Execalc provides executive control.** It decides which agent is allowed to act, which tools it may use, which claims matter, which actions require approval, which results become memory, and what is logged.

Ungoverned agent stacks have access and action, but not judgment. Execalc is the governed runtime for agentic enterprise work.

---

## The GAQP Foundation — What Is Built

### The Breakthrough: Claim Over Document

Before GAQP, the smallest analytical unit was the document. Documents are containers — scaffolding and signal mixed together, indistinguishable from the outside. Retrieving a document retrieves everything: cover page, methodology, appendices, and the three paragraphs that actually matter.

GAQP redefines the atomic unit. **The claim, not the document, is the smallest unit of qualitative intelligence.**

A claim is the minimum extractable assertion:

> "Segment C total addressable market is approximately $2.1B — based on three independent market analyses, strong confidence."

The document that contained it is preserved as a source artifact. It is no longer the unit of reasoning.

This changes four things:

**Retrieval** — A document consumes 2,000–8,000 context window tokens. Three relevant claims extracted from that document consume 150–300 tokens. With GAQP, Execalc reasons across the equivalent knowledge of 15–20 documents in the context window previously needed for 2–3.

**Confidence** — Without GAQP, a document is a single confidence object — everything in it carries the same weight. With GAQP, each claim carries its own confidence level. A verified fact and a hopeful projection in the same document are no longer treated as equally reliable inputs.

**Contradiction detection** — Two documents produced six months apart may make conflicting claims. Without GAQP, this is only caught if both happen to land in the same context window. With GAQP, contradiction detection runs at corpus admission — before reasoning begins.

**Knowledge compounding** — Without GAQP, organizational knowledge is the sum of its documents. It cannot build on itself. With GAQP, every new document either adds novel claims, corroborates existing ones (raising confidence), or contradicts them (triggering review). The corpus gets stronger with every artifact processed.

---

### The 24 Canonical Claim Types

Every claim admitted to the corpus belongs to exactly one of 24 types. The types are not arbitrary taxonomy — each type has distinct properties governing how Execalc weights it, retrieves it, detects contradictions, and decays it over time.

The taxonomy is locked at 24 types. Changes require explicit canon revision with documented rationale. See `docs/gaqp/GAQP_CLAIM_TYPE_TAXONOMY.md`.

---

### The Confidence Ladder

Claims carry one of four confidence levels, each with a numeric score:

| Level | Score | Meaning |
|---|---|---|
| Seed | 0.50 | First occurrence — one read is an opinion |
| Developing | 0.72 | Second independent source confirms |
| Strong | 0.91 | Three independent frameworks converging — a finding |
| Structural | 1.00 | Institutional doctrine — elevated to operating rule |

Confidence advances only when independent sources increase. Same-tenant repetition is tracked separately and does not promote confidence. This operationalizes GAQP's Multi-Source Corroboration principle: one read is an opinion, three independent reads converging is a finding.

---

### Corpus Admission

Claims are not stored — they are **admitted**. Every candidate must pass seven admission tests before entering the corpus. Tests 1–4 are hard gates (failure → rejected). Tests 5–7 are soft gates (failure → held for operator review).

Only admitted claims reach the corpus. The corpus reflects not just what the organization has encountered, but what it has decided to believe, at what confidence, based on what evidence.

That is the difference between a document archive and institutional memory.

---

### The Activation Engine (v1)

When a decision request arrives, Execalc runs the activation engine rather than retrieving documents. The engine:

1. Queries the corpus for claims relevant to the incoming scenario
2. Returns claims sorted by confidence score
3. Constructs an `ActivationBundle` containing activated claims with rationale

The bundle is surfaced alongside the `DecisionReport` — operator-visible, never silently injected into the decision output. The operator sees both the judgment and the corpus evidence that informed it.

**v1 activation matching is deterministic (keyword-based).** Universal-scope claims always fire. Other scopes fire when activation trigger keywords match the scenario context. Embedding-based semantic matching is a planned v2 capability.

---

### Current State of the GAQP Layer

**Fully operational:**
- `GAQPClaim` as the atomic corpus unit with all metadata fields
- 24 claim types enforced in code
- Confidence ladder with numeric scores
- Seven-test admission gate
- Corroboration profile tracking independent sources
- Deterministic fingerprint for idempotent extraction
- Tenant-scoped corpus persistence (Postgres)
- Activation engine returning bundles by confidence and trigger match
- Backfill pipeline for seeding corpus from existing execution records

**v1 scope (foundation present, engine not yet built):**
- Extraction is `direct_field` from `DecisionReport` output only. LLM-decomposed extraction from arbitrary documents (the full claim extraction pipeline described in the PDF) is in the type system but not yet implemented.
- Contradiction detection is tracked per claim (`contradiction_refs`) but the activation engine does not yet actively surface contradiction alerts in the bundle.
- Confidence promotion (seed → developing → strong via corroboration events) is tracked in the data model but the promotion engine is not yet built.
- Gap detection ("what don't we know?") is not yet implemented in the activation engine.

---

## The Product Surface — What Is Next

### IFD — Intelligent Front Door

The IFD is a governed inbound execution container. External submissions — pitches, proposals, reports, emails, requests — enter through a dedicated channel and are processed by a layered battery of specialized agents, each with kill authority.

```
SUBMISSION ENTERS CONTAINER
        ↓
LAYER 1 — SECURITY AGENTS      Cheapest. Fastest. Kill: immediate abort.
LAYER 2 — SPAM AGENTS          Pattern-based. Kill: immediate abort.
LAYER 3 — SIGNAL AGENTS        Semantic. Kill: abort if below threshold.
LAYER 4 — RELEVANCE AGENTS     Context-aware. Kill: abort if no match.
LAYER 5 — VALUE AGENTS         Full GAQP reasoning. Kill: final decision.
        ↓
PASSES TO RECIPIENT WITH CONTEXT PACKAGE
```

The economics follow from kill-early design: most submissions die in Layers 1–2 at near-zero cost. Only signal-bearing material survives to the expensive layers.

**Critical differentiator from generic spam filters:** the IFD uses client-defined signal criteria. Every organization declares what signal means for them. A venture capital firm and a wholesale distributor run the same agents against completely different criteria.

The IFD is not AI email filtering. It is agentic signal enforcement through a governed container.

**Status:** Specified. Not yet implemented.

---

### Bridge — Bilateral Governed Execution

The Bridge is a governed execution container where two or more Execalc tenants connect under a mutually approved syllabus, run certified agents on both sides, and execute pre-authorized workflows — ordering, billing, receiving, paying, reporting — with full audit trails and commitment receipts visible to both parties simultaneously.

**The key innovation is the syllabus model.** Two organizations do not configure an integration. They describe an intent. Execalc reads both declarations, constructs a unified workflow, surfaces it to both parties for approval, and upon confirmation assembles the agents and activates the Bridge.

The syllabus is the governing execution instrument inside the Bridge. Every agent action is governed by it — nothing outside it can execute.

**Bridge replaces three things** that have plagued B2B commerce:
- Brittle bilateral EDI-style integration patterns requiring technical teams on both sides
- AP/AR friction from invoice disputes, unmatched receipts, delayed payments
- Integration projects requiring months of custom engineering to start a new supplier relationship

**Status:** Specified. Not yet implemented.

---

### The Agent Registry

Execalc does not treat all agents as equal. A certified agent registry governs which agents are permitted to act, under what authority, within what scope. Registry entries carry declared capabilities, certification tier, approved actions, tool permissions, tenant scope, audit record, and human-approval requirements.

The registry is Execalc's labor control layer. MCP can expose tools. Execalc decides which agents are allowed to use which tools under which circumstances.

**Status:** Concept defined. Not yet specified or implemented.

---

### Cartridges

A cartridge is a complete program for Execalc — a structured instruction set governing how Execalc conducts a complex, multi-party, multi-step process from start to finish. It governs not just what to do but how to ask, how to listen, when to loop back, and when to conclude.

A cartridge is distinct from a playbook. A playbook governs one action. A cartridge governs a program.

The negotiation cartridge is the canonical example: Execalc loads it to conduct a bilateral syllabus negotiation between two parties, mediating their declarations, structuring terms, surfacing gaps, and reaching mutual confirmation.

Cartridges come in two kinds:
- **Proprietary** — built by the tenant, about the tenant, living exclusively in their namespace. This is the institutional intelligence that makes one tenant's Execalc instance smarter than a competitor's.
- **Community store** — built by domain experts (practitioners, scholars, analysts), available for purchase and installation into any tenant namespace. The community store is a V2/V3 product surface with governance requirements that must be fully designed before implementation.

**Status:** Concept defined. Not yet specified or implemented.

---

## The Executive Knowledge Engine

Every organization's Execalc instance is shaped by its own reality — constraints, priorities, knowledge, heuristics. Same platform. Completely different intelligence.

The EKE makes organizational thinking explicit, executable, and persistent. An institution's judgment survives the individuals who created it. The GM's trade philosophy survives the GM. The CFO's capital discipline survives the CFO.

Execalc does not replace the decision-maker. It makes the decision-maker's thinking institutional.

---

## What Execalc Is Not

- An ungoverned chatbot
- An agent swarm that self-directs actions
- A workflow automation product as its core identity
- A dashboard-only "insights" tool
- A system that relies on chat history as its source of truth
- A discovery or matchmaking tool (Bridge is not that)

---

## Sovereignty Model

- **Integrations provide access**
- **Workers perform labor**
- **Informants supply signal**
- **Execalc alone produces judgment**

Workers may draft and execute bounded tasks only when authorized by Execalc under policy gates and proof standards.

MCP gives access. Agents execute. Execalc governs.

---

## Build Doctrine

This document describes what Execalc is and is becoming. It does not describe a wish list — it describes a governed build sequence.

What is built is described as built. What is specified but not built is described as next. What is visioned but not specified is described as future. These distinctions are not cosmetic. Execalc's own governance principle applies to its own build record: no floating assertions.

The repository is the constitutional source of truth. Chat is ideation. This document is doctrine.

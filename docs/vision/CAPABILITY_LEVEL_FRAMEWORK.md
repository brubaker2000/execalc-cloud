# Execalc Capability Level Framework

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-20  
**Authority:** Execalc Product Standards

---

## Purpose

This framework defines five levels of AI capability maturity in organizational settings. It establishes the competitive landscape, names the category Execalc occupies, and articulates why Level 5 is not an incremental improvement over lower levels but a categorically different kind of system.

---

## The Five Levels

### Level 1 — Raw LLM

Fluent, fast, useful, but ungoverned.

The model can generate impressive language, but it does not know what is admissible, authoritative, strategic, or institutionally safe. It reasons from training data and prompt context alone. Every session starts from zero. Nothing compounds.

*Examples: ChatGPT (base), Claude (base), Gemini (base)*

---

### Level 2 — Governed AI

The model now reasons inside doctrine.

It is constrained by frameworks, values, priorities, memory, heuristics, and decision boundaries. Output starts becoming system-shaped instead of merely prompt-shaped. The model knows what it is supposed to do, what it should avoid, and what the organization cares about.

This is where AI begins to feel like a product rather than a tool.

*Examples: Custom GPTs with system prompts, enterprise AI with policy guardrails, Copilot with organizational context*

---

### Level 3 — Governed AI with Agents

The system gains operational reach.

It can search, retrieve, route, execute, update, and coordinate. The AI is no longer confined to generating text — it can take action in the world. But if the agents themselves are not governed, the system has action capability without full institutional discipline. The governance applies to the reasoning; the actions may still be ungoverned.

*Examples: OpenAI Agents, AutoGPT-style systems, AI with tool use but without action boundaries*

---

### Level 4 — Governed AI with Governed Agents

The agents operate inside authority boundaries.

They know what they may do, what they may not do, when to escalate, what must be logged, and what requires approval. Action becomes auditable. The system can be held accountable because its decisions and actions leave a traceable record. This is where enterprise AI becomes safe enough for consequential decisions.

*Examples: Execalc with Execution Boundary Engine active — this is where the current governed runtime path lives*

---

### Level 5 — GAQP-Enabled Governed AI with Governed Agents

The qualitative material itself is governed.

The system is not merely producing answers or taking actions. It is working from source-anchored claims, provenance, confidence scores, admissibility status, contradiction handling, and reusable intelligence objects. Every piece of qualitative reasoning the system draws on has been admitted through a structured gate, tagged with metadata, and stored in a corpus that compounds over time.

This is where institutional trust begins to scale.

---

## The Deepest Point

GAQP does not just improve the output.

**It improves the raw material the system is allowed to reason from.**

That is a much bigger move than better prompting or better agent orchestration. A system at Level 4 reasons well from whatever it is given. A system at Level 5 controls what it is given — and has governed that input through admission, classification, provenance, and confidence assessment before reasoning begins.

The difference is not speed or fluency. It is epistemic discipline.

---

## The Connection to Qualitative Capture

A normal chatbot — even a governed one — produces valuable transcript material that immediately becomes hard to retrieve. The insight exists in the conversation. It does not survive as institutional knowledge.

A Level 5 system captures that material as governed qualitative intelligence: claims, insights, assumptions, risks, opportunities, decisions, and source-anchored nuggets that can be retrieved, activated, and recombined across future sessions and across the organization.

The transcript is the source stream. The GAQP corpus is the system of record.

This is not a memory feature. It is a fundamentally different model of how organizational intelligence accumulates.

---

## The Category Argument

Most AI products are trying to make the model smarter.

Execalc and GAQP are trying to make the entire reasoning environment governable, auditable, and reusable.

These are not the same goal. They do not produce the same kind of system. And they do not serve the same kind of organization.

A Level 1–3 system is useful. A Level 4 system is enterprise-ready. A Level 5 system is institutionally trustworthy — the kind of system that can sit above high-stakes decisions, hold a long-term strategic memory, and be audited by regulators, boards, or acquirers.

**No current commercial AI product operates at Level 5.**

The products closest to Level 4 are constrained by the absence of a governed qualitative corpus. They have governance over reasoning and action. They do not have governance over the raw material that feeds reasoning. Without that, the system's intelligence does not compound. It restarts.

---

## Competitive Mapping

| Product | Level | Limiting Factor |
|---|---|---|
| ChatGPT (base) | 1 | No governance, no memory, no corpus |
| Claude (base) | 1 | No governance, no memory, no corpus |
| Copilot for M365 | 2–3 | Governance thin, agents present, no governed corpus |
| NotebookLM | 2 | Knowledge retrieval, no governance, no corpus |
| Custom GPTs / Assistants | 2 | System prompt governance only, no action boundary, no corpus |
| OpenAI Agents | 3 | Action reach without full authority boundary |
| Execalc (current) | 4 | EBE live, GAQP corpus building, Level 5 in progress |
| **Execalc (Level 5 complete)** | **5** | **GAQP corpus fully operational, qualitative capture live** |

---

## Design Implication

Every architectural decision in this repo should be evaluated against one question:

**Does this move us toward Level 5, or does it add capability without governance?**

Capability without governance moves the system laterally, not upward. A Level 3 system with more agents is still a Level 3 system.

The path to Level 5 runs through GAQP completion, Qualitative Capture runtime, and full substrate abstraction — not through feature expansion at lower levels.

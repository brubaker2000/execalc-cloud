# Qualitative Capture Runtime Specification

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-19  
**Authority:** Execalc Product Standards

---

## I. Purpose

This document specifies the Qualitative Capture Runtime — the parallel intelligence pipeline that runs alongside the Execalc chat surface, extracts durable signal from conversational events, and surfaces compressed intelligence on the Executive Rail.

This is not a summary feature. It is not a memory feature. It is not a bookmark. It is a governed capture, classification, compression, retrieval, and reconstruction pipeline that converts raw conversation into a tenant-scoped, GAQP-compliant knowledge corpus.

---

## II. The Central Problem

AI creates qualitative value faster than humans can absorb it.

The chatbot model has three structural failure modes:

1. **Output overload** — more generated than can be processed
2. **Discovery overload** — unexpected insight appears with no clean capture path
3. **Retrieval failure** — valuable language exists but cannot be located later

These are not personal organization problems. They are product architecture problems.

The current model treats conversation as the unit of storage. That is wrong.

A conversation is the source stream. The system of record is what is extracted from it.

**Governing rule:** Preserve source. Compress aggressively. Reconstruct on demand.

---

## III. What Is Already Defined

The following specs define adjacent surfaces. This document does not duplicate them — it unifies them into a single pipeline model.

| Document | What it governs |
|---|---|
| `docs/gaqp/GAQP_RUNTIME_ARCHITECTURE.md` | The six-layer GAQP classification engine and seven output types |
| `docs/gaqp/GAQP_METADATA_SCHEMA.md` | The atomic nugget schema, confidence ladder, and field requirements |
| `docs/gaqp/GAQP_CLAIM_TYPE_TAXONOMY.md` | The canonical claim type register |
| `docs/product/EXECALC_MEMORIALIZE_SPEC.md` | Human-triggered capture via right-click → Memorialize |
| `docs/product/EXECALC_NUGGET_CAPTURE_SYSTEM.md` | Keyboard-native capture via "Nugget" trigger word |
| `docs/product/EXECUTIVE_RAIL_WORKSPACE_SPEC.md` | The three-pane workspace layout and rail role |

This document governs: how those pieces connect as a runtime pipeline, what database objects implement that pipeline, how the pipeline flows from raw event to rail card, and how rail cards become second-order intelligence.

---

## IV. The Five Intelligence Tiers

Not all output from the pipeline is the same. The system should maintain five distinct tiers and never collapse them.

| Tier | Name | Description |
|---|---|---|
| 0 | Raw archive | The original conversation transcript, untouched. The source. |
| 1 | Captured signal | Important moments extracted from the stream — atomic nuggets and memorialized items. |
| 2 | Structured claims | Source-anchored, typed, tagged, confidence-labeled GAQP corpus objects. |
| 3 | Executive conclusions | Reconstructed intelligence — clean operator-facing synthesis across multiple claims. |
| 4 | Canon | Durable governing doctrine promoted by human authority. Governs future reasoning. |

Each tier is a separate database concern. Collapsing them destroys the architecture.

---

## V. The Five-Layer Runtime

The pipeline operates as five coordinated layers.

### Layer 1 — Capture

The system watches every conversation event for material worth preserving.

**Machine capture** detects:
- New doctrines and product decisions
- Definitions and naming decisions
- Metaphors with explanatory power
- Architecture commitments
- Market theses and investor language
- Technical decisions
- Open questions and unresolved loops
- Contradictions between prior claims
- Confidence threshold crossings in the nugget corpus

**Human capture** is the complement — never the fallback:
- Right-click → Memoralize (see `EXECALC_MEMORIALIZE_SPEC.md`)
- "Nugget" trigger word (see `EXECALC_NUGGET_CAPTURE_SYSTEM.md`)
- A human-preserved idea receives stronger weight and bypasses Knowledge Policy sliders

Both paths feed the same pipeline. Neither replaces the other.

### Layer 2 — Classification

Every captured item maps to exactly one canonical GAQP claim type (see `GAQP_CLAIM_TYPE_TAXONOMY.md`).

Classification is not cosmetic. It governs how the item is retrieved, weighted, and used:
- A **Doctrine** constrains future reasoning
- A **Heuristic** surfaces as a decision shortcut
- A **Risk** triggers warnings
- A **Metaphor** enriches explanation
- A **Market Thesis** elevates in investor-facing reconstruction

An unclassified nugget is an incomplete nugget.

### Layer 3 — Compression

The pipeline regularly compresses captured signal into usable objects. This is where the fire hose becomes a garden hose.

Five operator-selectable compression levels exist:

| Level | Request | Output |
|---|---|---|
| 1 | "What did we just decide?" | One-line net — the single governing conclusion |
| 2 | "Give me the 5 key points" | Executive brief — top signal ranked by importance |
| 3 | "How did this idea evolve?" | Development journal — reconstructed progression |
| 4 | "Convert to canon-ready doctrine" | Doctrine packet — promotion-ready governing statements |
| 5 | "Show every source that supports this" | Source audit — full provenance trace |

Compression should be on-demand, not automatic. The system should not flatten useful signal without operator intent.

### Layer 4 — Retrieval

Stored intelligence should be conversationally accessible. The operator should be able to ask:

- "Show every claim related to fixed-ops performance."
- "Find the origin of the fire hose/garden hose metaphor."
- "What have we decided about GAQP vs. Execalc?"
- "Show the best investor language we have produced."
- "What architectural questions are still open?"
- "Give me the current canon on Qualitative Capture."
- "Rehydrate the discussion about Stage 9."

This is the difference between chat history and a usable memory system.

### Layer 5 — Reconstruction

The highest-value layer. Does not merely retrieve stored material — recombines it into new usable forms.

Examples of reconstruction targets:
- Historical development journal
- Investor memo
- Product requirements document
- Technical build packet
- Founder doctrine
- White paper or standards package
- Repo hydration packet
- Board memo

The distinction: search finds fragments. Reconstruction turns fragments into usable executive output.

---

## VI. The Runtime Path

```
User sends chat message
  ↓
Raw conversation_event stored (Tier 0)
  ↓
Main chat response proceeds normally — pipeline does NOT block chat
  ↓
In parallel: event enters qualitative-capture queue
  ↓
GAQP deconstructor runs (Layer 1 + 2 above)
Atomic nuggets extracted, classified, confidence-scored
  ↓
Nuggets written to tenant-scoped atomic_nuggets table (Tier 1 → Tier 2)
  ↓
Reconstructor clusters high-signal nuggets above threshold
Executive conclusion generated (Tier 3)
  ↓
Clean conclusion appears on Executive Rail as right_rail_card
  ↓
Operator may: preserve / pin / dismiss / route / promote
  ↓
Rail card stored as rail_artifact (first-class object — not ephemeral)
  ↓
Rail artifact later deconstructed into second-order nuggets
Second-order nuggets enter the corpus as Tier 2 objects
```

**Critical constraint:** The pipeline is parallel and non-blocking. Chat latency must not increase because of capture activity.

---

## VII. Database Objects

These nine objects implement the pipeline. Do not collapse them into fewer tables — each tier boundary is a seam.

| Object | Tier | Description |
|---|---|---|
| `conversation_events` | 0 | Raw message events, timestamped, tenant-scoped |
| `atomic_nuggets` | 1–2 | Extracted GAQP-compliant claims, full metadata schema |
| `preserved_ideas` | 1–2 | Human-memorialized items, selection_method tagged, perpetual retention |
| `executive_conclusions` | 3 | Reconstructed operator-facing conclusions, sourced from nugget clusters |
| `right_rail_cards` | 3 | Display objects projected onto the Executive Rail |
| `rail_artifacts` | 3 | Persisted rail cards — first-class objects, not display ephemera |
| `promotion_candidates` | 3→4 | Items nominated for Canon elevation, pending human approval |
| `runtime_activations` | 2–3 | Records of nugget activations — when a claim fired in context |
| `audit_events` | All | Full audit trail across all tiers |

The atomic nugget schema is defined in `docs/gaqp/GAQP_METADATA_SCHEMA.md`. The other object contracts are not yet fully frozen — see Section X.

---

## VIII. The Executive Rail

The right pane of the Execalc workspace is the live signal surface. See `docs/product/EXECUTIVE_RAIL_WORKSPACE_SPEC.md` for the workspace layout definition.

The rail displays, in simple card form only:
- Preserved ideas (human-memorialized — visually distinct)
- Executive conclusions
- Risks and warnings
- Opportunities
- Contradictions surfaced
- Open questions
- Promotion candidates

**The rail is for reading. Metadata is for audit.**

Every rail card should expose one clean conclusion and nothing else. Supporting nuggets, source anchors, provenance, confidence, and audit trail live behind the card, accessible on demand — not displayed by default.

**Rail artifact recursion:** A rail card is not ephemeral. Once displayed, it is stored as a `rail_artifact`. Rail artifacts are then deconstructed by the same GAQP pipeline into second-order atomic nuggets, which re-enter the corpus as Tier 2 objects. The organization therefore learns not just from conversations, but from the compressed signal of its own intelligence output.

---

## IX. Human Preservation as a Value Signal

The right-click → Memorialize action is not bookmarking. It is a user-declared value signal.

When an operator preserves text:
- Confidence elevates immediately to Strong (0.91)
- Durability class is set to Enduring — no expiry
- Promotion bypasses Knowledge Policy sliders — always promotes to corporate pool
- Retrieval priority elevates above auto-extracted claims of the same type and domain
- If a second user independently memorializes the same language, confidence auto-elevates to Structural (1.00)

The aggregate of all memorialized nuggets across an organization's tenant is the highest-quality knowledge corpus it can produce. Auto-extraction is the floor. The memorialized corpus is the ceiling.

---

## X. Session Intelligence Packet

At the close of a significant conversation session, the system should be capable of producing a compact Session Intelligence Packet. This is the anti-overload mechanism.

**Contents:**
- Session title
- Core breakthrough (single most important output)
- Captured nuggets (ranked by estimated future importance)
- New claims introduced
- New doctrine candidates
- Decisions made
- Open questions
- Follow-up artifacts needed
- Source anchors for key items
- Canon updates, if operator-approved

The Session Intelligence Packet format is the model for what a rehydration object looks like. Long conversation in. Operational packet out.

---

## XI. What This Is Not

To prevent implementation drift, the following must be explicitly rejected:

| Wrong implementation | Why it fails |
|---|---|
| Post-chat summary appended to chat | Collapses Tier 0 and Tier 3; destroys provenance |
| Memory feature that stores conversation context | Not intelligence — just history |
| Bookmark feature with user-added notes | No classification, no pipeline, no reconstruction |
| Generic notes panel on the right | No GAQP compliance, no corpus, no retrieval |
| Long metadata card on the rail | Violates "rail is for reading" principle |
| Single `insights` table | Destroys tier separation |
| Chatbot sidebar with summaries | No source anchors, no auditability, no corpus |

---

## XII. Module Structure

```
src/service/qualitative_capture/
  events.py          — conversation event ingestion and storage
  deconstructor.py   — GAQP extraction and nugget classification
  reconstruction.py  — nugget clustering and executive conclusion generation
  rail.py            — rail card generation, display, and artifact persistence
  preserved_ideas.py — human memorialize path and weight rules
  promotion.py       — promotion candidate logic and Canon elevation workflow
  models.py          — ORM models for all nine database objects
  repository.py      — data access layer
  tests/
```

---

## XIII. Specs Still to be Frozen

The following implementation specifics require a dedicated freeze session before full build-out:

- `docs/product/RIGHT_RAIL_CAPTURE_UX_SPEC.md` — exact card types, visual treatment, interaction behaviors
- `docs/product/GAQP_CORPUS_OBJECT_CONTRACT.md` — full object contracts for all nine database objects
- `docs/product/RAIL_ARTIFACT_RECURSION_SPEC.md` — policy for deconstructing rail artifacts into second-order nuggets
- Admissibility and confidence enum values beyond the atomic nugget schema
- Promotion workflow from candidate to canon
- First closed set of rail card types

---

## XIV. The Governing Formulation

> AI creates qualitative value faster than humans can absorb it. The winning system is not the one that produces the most language. It is the one that captures, classifies, compresses, retrieves, and reconstructs the right intelligence at the right time.

This is not a feature. It is the product's structural answer to the fire hose problem.

Chat remains the thinking surface.  
The Executive Rail becomes the live signal surface.  
Postgres becomes the durable GAQP corpus.

That is the build target.

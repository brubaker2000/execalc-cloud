# CORPUS_RETRIEVAL_MODEL.md

## Status
Draft v0.1 — Pre-Stage-8 blocker spec

## Owner
Architecture / Stage 8B + Stage 9A

## Purpose
This document specifies how EKE corpus entries are retrieved and injected into the Stage 4 Activation Pathway context package.

It exists because "pull all EKE corpus entries associated with the detected scenario" is not a retrieval model. At scale it would overflow the LLM's effective reasoning capacity. This document makes retrieval governed, token-budgeted, and ranked.

---

## The Foundational Doctrine

> **Execalc does not recall knowledge. It recalls decision fragments.**

This is the canonical distinction.

A knowledge retrieval system pulls full texts, essays, and comprehensive frameworks. It attempts to inject all relevant information and let the model reason from it.

Execalc retrieves **decision fragments** — compressed, pre-structured units of strategic judgment that activate the right reasoning pattern without consuming the reasoning capacity needed to apply it.

The grandmaster analogy made operational: the grandmaster does not re-read Sun Tzu before responding to a competitive threat. They activate a compressed pattern — "flank, don't charge" — and apply it immediately. The full text is not in working memory. The operative fragment is.

This distinction governs every decision in this spec.

---

## The Problem Being Solved

The EKE Monolith Seed Corpus contains 230 entries. The scenario-to-corpus mapping for a Risk & Defense scenario associates entries from Sun Tzu (7), Clausewitz (7), Taleb (7), and Kahneman (7) — 28 entries, each averaging 200–400 words.

28 entries × 300 words average = **8,400 words = ~11,000 tokens** before the operator's input arrives.

Opus's context window can hold this. But reasoning quality degrades when the model must process a large block of loosely related material and determine which parts apply. The model becomes a reader, not a thinker.

The retrieval model solves this by:
1. Selecting only the most relevant entries (not all eligible entries)
2. Compressing each entry to its operative decision fragment (not its full text)
3. Enforcing a strict token budget

---

## Corpus Entry Structure (Runtime)

Each corpus entry in the runtime store has two representations:

**Full text** — the complete entry as committed in the corpus manifest. Stored in the corpus database. Used for retrieval ranking and human review. Never injected into the LLM context directly.

**Decision fragment** — a 40–80 word compressed distillation of the entry's operative logic. Structured as:
- The core pattern or heuristic in one sentence
- The activation condition (when this applies)
- The operative implication (what it means for this decision)

**Example (HTL-0023 — Sun Tzu: Attack Where Unprepared):**

Full text (≈ 300 words): "Sun Tzu's principle of attacking where the enemy is unprepared..."

Decision fragment (≈ 60 words):
```
PATTERN: Concentrate force where the opponent is weakest, not where they are strongest.
ACTIVATION: When competitive threat scenario is active and opponent has identifiable gaps.
IMPLICATION: Before responding symmetrically, identify where the competitor is unprepared. 
The question is not "how do we match them?" It is "where can't they follow us?"
```

Decision fragments are pre-authored at corpus load time (Stage 9A). They are not generated dynamically. This is deliberate — dynamic compression introduces variance and cannot be audited.

---

## Retrieval Pipeline

### Step 1: Scenario-Bucket Filtering

From the detected scenario, identify the scenario bucket (Growth/Opportunity, Deal/Capital, Org/Execution, Risk/Defense, Strategic Insight).

Pull the eligible corpus entries for that bucket from the scenario-to-corpus map in `REFLEX_AND_ACTIVATION_SYSTEM.md`.

This is the **candidate pool** — all entries that are potentially relevant. This may be 20–40 entries.

**Model tier:** No model call. Lookup from pre-built map.

---

### Step 2: Relevance Ranking

Rank the candidate pool against the operator's specific input using embedding similarity between:
- The operator's input text
- Each corpus entry's decision fragment (not full text)

Output: ranked list of all candidate entries with relevance scores.

**Model tier:** Labor (embedding model). Same model used in Layer 2 of scenario detection.

---

### Step 3: Top-N Selection

Select the top N entries by relevance score, subject to the token budget:

| Scenario Type | Max Entries | Token Budget (fragments only) |
|---|---|---|
| Single clear scenario (≥ 0.85 confidence) | 5 | 400 tokens |
| Standard scenario (0.70–0.84 confidence) | 7 | 600 tokens |
| Dual scenario (primary + secondary both active) | 5 primary + 3 secondary | 700 tokens |
| Ambiguous / Opportunity Discovery fallback | 3 | 250 tokens |

**Hard ceiling:** No more than 7 corpus entries total per context package, regardless of scenario type.

**No exceptions to the token budget.** If the top-N entries would exceed the budget, reduce N until the budget is met.

---

### Step 4: Fragment Injection

Only decision fragments — not full text — are injected into the context package.

Fragments are injected in a dedicated `corpus_entries` slot in the context package with the following structure:

```json
{
  "corpus_entries": [
    {
      "corpus_id": "HTL-0023",
      "thinker": "Sun Tzu",
      "theme": "Competitive Positioning",
      "relevance_score": 0.91,
      "decision_fragment": "PATTERN: Concentrate force where the opponent is weakest..."
    },
    ...
  ],
  "total_entries": 5,
  "token_budget_used": 312,
  "token_budget_limit": 600,
  "entries_suppressed": 3
}
```

`entries_suppressed` is the count of candidate entries that were eligible but not included due to the token budget. This appears in the audit trail.

---

## Fragment Authoring Standard

Decision fragments must be authored at corpus load time according to the following standard:

**Required elements:**
1. `PATTERN:` — the core strategic insight in one sentence, 15–25 words
2. `ACTIVATION:` — when this pattern applies, 10–20 words
3. `IMPLICATION:` — what it means for the immediate decision, 20–40 words

**Total fragment length:** 45–85 words.

**Authoring authority:** Decision fragments are authored by the Execalc team and locked at commit. They are not generated by the LLM on demand. This is a governance requirement — dynamically generated fragments cannot be audited, versioned, or held accountable.

**Fragment quality gate:** A fragment that cannot be written in 45–85 words has not been distilled enough. The distillation process is where the intellectual work lives — not in the retrieval.

---

## Override: Direct Corpus Entry Request

An operator may explicitly request a specific framework or thinker ("apply Clausewitz to this"). In this case:

1. The requested thinker's entries are included in the candidate pool regardless of relevance score
2. Up to 2 entries from the explicitly requested thinker are guaranteed inclusion
3. These 2 entries count against the token budget and the max-N limit

This override is logged in the audit trail as `operator_requested_corpus`.

---

## Relationship to Stage 8 vs. Stage 9

**Stage 8** needs a minimal corpus bootstrap to populate the `corpus_entries` slot before the full corpus loader (Stage 9A) is built. The Stage 8 bootstrap is:

- A flat JSON/YAML file containing pre-authored decision fragments for the starter reflex registry scenarios (7, 8, 14, 16, 18 from `REFLEX_AND_ACTIVATION_SYSTEM.md`)
- No database required — loaded at service init from a static file
- Covers the most critical scenarios for initial testing

**Stage 9A** replaces this bootstrap with the full corpus database, loader, and retrieval pipeline described in this spec.

The Stage 8 bootstrap is explicitly temporary. It is labeled as such in code comments and must not be extended beyond the 5 starter scenarios.

---

## Audit Requirements

Every corpus retrieval must produce an audit record containing:
- Detected scenario and bucket
- Candidate pool size
- Relevance scores for all candidates
- Top-N selected entries (with corpus_ids)
- Token budget used vs. limit
- Entries suppressed (count and corpus_ids)
- Any operator-requested corpus overrides

---

## Design Principle

> The retrieval model governs what the LLM thinks with, not what the LLM thinks about. A model reasoning from 7 sharp decision fragments is more governed than a model reasoning from 28 full texts. Precision of input is the foundation of precision of output.

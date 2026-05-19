# Rail Artifact Recursion Specification

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-19  
**Authority:** Execalc Product Standards

---

## I. Purpose

This document defines the policy for second-order deconstruction — the process by which rail artifacts are themselves deconstructed by the GAQP pipeline into atomic nuggets that re-enter the corpus.

This is not a background cleanup task. It is a core intelligence-compounding mechanism.

For the pipeline that creates rail artifacts, see `docs/product/QUALITATIVE_CAPTURE_RUNTIME_SPEC.md`.  
For the object contracts governing rail artifacts and second-order nuggets, see `docs/product/GAQP_CORPUS_OBJECT_CONTRACT.md`.

---

## II. The Governing Insight

A conversation generates first-order signal.  
The pipeline extracts that signal into atomic nuggets.  
The reconstructor compresses those nuggets into executive conclusions.  
Those conclusions appear on the rail as cards.  
The cards are persisted as rail artifacts.

Here is the key insight: **a rail artifact is itself a high-quality qualitative object.**

It is not a raw transcript. It has already been deconstructed, classified, reconstructed, and operator-validated. It represents the system's own best compressed intelligence about a conversation.

When that compressed intelligence is deconstructed again, the resulting second-order nuggets are often more durable, more portable, and more composable than the first-order nuggets they were derived from — because the reconstruction step already filtered noise.

This is how the organization learns not just from raw conversations, but from the intelligence it has already produced about its own conversations.

---

## III. What Qualifies as a Rail Artifact

Not every rail card becomes a rail artifact. Rail artifacts are created under the following conditions:

| Trigger | Description |
|---|---|
| Operator Preserve | Operator clicks Preserve on a rail card |
| Operator Promote | Operator clicks Promote on a rail card |
| Operator Route | Operator routes a card to another user, project, or artifact |
| System Auto | A rail card crosses a significance threshold (see Section IV) |

Cards that are only dismissed — without any of the above actions — do not become rail artifacts. They remain in `right_rail_cards` with `is_dismissed = true` and their underlying `executive_conclusions` remain in the corpus, but no artifact record is created.

---

## IV. System Auto-Artifact Threshold

The system automatically converts a rail card to a rail artifact when any of the following conditions are met:

1. The underlying executive conclusion has `reconstruction_confidence >= 0.85`
2. The underlying cluster contains three or more atomic nuggets of `durability_class = Enduring`
3. The card type is `Contradiction` (all contradictions are auto-artifacted — they require audit retention)
4. The card type is `Promotion Candidate` (all promotion nominees are auto-artifacted)
5. The underlying conclusion contains one or more nuggets with `selection_method = human_memorialized`

Auto-artifacted cards receive `operator_action = system_auto` in the `rail_artifacts` table.

---

## V. The Second-Order Deconstruction Policy

### When deconstruction runs

Second-order deconstruction runs on every rail artifact with `second_order_deconstruction_status = pending`. It is a background process — it does not block artifact creation or rail display.

Default timing: within 60 minutes of artifact creation.  
Priority queue: artifacts from Preserve and Promote actions run before system_auto artifacts.

### What the deconstructor does

The second-order deconstructor applies the same GAQP extraction process used on raw conversation events, but with the rail artifact text as the input rather than a raw message. Because the input is already compressed and structured, the deconstructor operates on a higher signal-to-noise ratio.

The deconstructor:

1. Reads the `artifact_text` from the rail artifact
2. Reads the `source_nugget_ids` from the linked `executive_conclusions` record (for context)
3. Runs GAQP classification — identifies claimable units within the artifact text
4. Assigns claim type, domain, polarity, durability class, evidence status, freshness class
5. Writes each extracted claim to `atomic_nuggets` with:
   - `selection_method = second_order`
   - `generation_depth = 2`
   - `source_rail_artifact_id` = the parent artifact's `artifact_id`
   - `confidence_level = Developing` (0.72) as the floor — second-order nuggets start higher than Seed because the reconstruction step already applied a confidence filter
6. Links the new nugget IDs back to the parent artifact's `second_order_nugget_ids` array
7. Updates `second_order_deconstruction_status = complete`

### Confidence floor for second-order nuggets

First-order machine-extracted nuggets start at Seed (0.50).  
Second-order nuggets start at Developing (0.72).

The rationale: the reconstruction step that produced the rail artifact already applied a confidence filter across the source nugget cluster. The resulting artifact text carries the aggregate confidence of its sources. Starting second-order nuggets at Developing reflects that inherited signal quality.

Human-memorialized rail artifacts produce second-order nuggets that start at Strong (0.91), not Developing — because the human preservation act is itself a high-confidence signal.

---

## VI. Recursion Depth Limit

Second-order deconstruction is depth-limited to `generation_depth = 2`.

Second-order nuggets (`generation_depth = 2`) do not themselves feed a third-order deconstruction pass. They enter the corpus as standard atomic nuggets and participate in future reconstructions on equal footing — but they do not trigger another artifact-creation-and-deconstruction cycle.

**Why:** Unbounded recursion would cause corpus inflation as nuggets derived from nuggets derived from reconstructions of nuggets accumulate without bound. The signal-to-noise advantage of second-order deconstruction degrades rapidly beyond depth 2. The governed rule is: compress twice (conversation → rail artifact → second-order nugget), then stop.

The `generation_depth` field in `atomic_nuggets` enforces this. The deconstructor checks `generation_depth` before running and skips any artifact whose source nuggets are already `generation_depth = 2`.

---

## VII. How Second-Order Nuggets Participate in the Corpus

Second-order nuggets are full GAQP corpus citizens. They:

- Activate in reconstructions on equal footing with first-order nuggets
- Contribute to the confidence ladder (Seed → Developing → Strong → Structural) through corroboration
- Fire in reflex and diagnostic contexts
- Appear in retrieval results
- Can be memorialized by operators (elevating them to human-preserved status)
- Can become promotion candidates for Canon elevation

They are distinguished from first-order nuggets only by `generation_depth = 2` and the presence of `source_rail_artifact_id`. This distinction is metadata — it does not constrain their participation in the corpus.

---

## VIII. Provenance Traceability

Every second-order nugget carries a complete provenance chain:

```
atomic_nugget (generation_depth=2)
  ← source_rail_artifact_id → rail_artifacts
    ← source_card_id → right_rail_cards
      ← source_conclusion_id → executive_conclusions
        ← source_nugget_ids → atomic_nuggets (generation_depth=1)
          ← source_event_id → conversation_events
```

This chain must remain resolvable at every link. The audit trail in `audit_events` records every step.

An operator querying "where did this nugget come from?" should be able to trace it back to the specific messages in the specific conversation that originally generated it — even if that nugget is the product of two compression passes.

---

## IX. Cross-Session Compounding

Second-order nuggets participate in the confidence ladder across sessions.

If a second-order nugget from session A is independently corroborated by:
- A first-order nugget from session B (same tenant, different session)
- A second-order nugget from session C

...then the standard corroboration rules apply: confidence advances along the ladder (Developing → Strong → Structural at the third independent corroboration).

This is the compounding engine. Over time, claims that appear independently in multiple conversations — whether as raw extraction or as reconstructed conclusions — accumulate confidence automatically. The corpus becomes richer without requiring additional operator effort.

---

## X. Audit Events for Second-Order Deconstruction

The `audit_events` table records the following events in the second-order deconstruction lifecycle:

| Event type | Fired when |
|---|---|
| `artifact.created` | A rail artifact record is written |
| `artifact.deconstruction_started` | Deconstruction begins on an artifact |
| `nugget.created` | Each second-order nugget is written (one event per nugget) |
| `artifact.deconstruction_complete` | All second-order nuggets written; artifact status updated |
| `artifact.deconstruction_skipped` | Artifact was depth-limited or produced no extractable claims |

---

## XI. Operator Visibility

Operators do not need to manage second-order deconstruction. It is a background process.

However, operators should be able to:
- See that a rail artifact has been deconstructed (status indicator in artifact detail view)
- View the second-order nuggets produced from a specific artifact
- Trace a second-order nugget back to its source artifact and conversation

These are audit and inspection capabilities — they are not part of the default rail UX.

---

## XII. The Governing Formulation

Rail artifacts are not the end of the pipeline. They are the beginning of the next compression pass.

The organization learns from conversations.  
Then it learns from what it concluded about those conversations.  
Then those conclusions re-enter the corpus and inform future reasoning.

That is the compounding engine. That is why the corpus becomes more valuable over time without growing proportionally larger.

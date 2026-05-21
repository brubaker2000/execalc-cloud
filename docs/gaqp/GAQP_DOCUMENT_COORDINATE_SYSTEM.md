# GAQP Document Coordinate System

**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

---

## I. Purpose

Every GAQP claim must be traceable to a precise location in its source material. Vague provenance ("this came from the strategy deck") does not satisfy the GAQP traceability requirement. The Document Coordinate System defines the anchor format that makes source provenance exact and machine-readable.

---

## II. The Coordinate Model

A document coordinate is a four-level address: **Document → Section → Paragraph → Sentence**.

```
[doc_ref]:[section].[paragraph].[sentence]
```

**Example:**
```
strategy_deck_2026Q1:3.2.1
```
This reads as: strategy deck, Q1 2026 — Section 3, Paragraph 2, Sentence 1.

---

## III. Coordinate Levels

| Level | Identifier | Description |
|---|---|---|
| Document | `doc_ref` | A stable, unique string identifying the source document. Format: `{slug}_{version}` |
| Section | Integer | Top-level section number. 0 if the document has no sections. |
| Paragraph | Integer | Paragraph within the section. 1-indexed. |
| Sentence | Integer | Sentence within the paragraph. 1-indexed. |

**Shorthand rules:**
- `doc:0.0.0` — document-level only; source identified but no finer resolution available
- `doc:3.0.0` — section-level; the claim is from Section 3 but paragraph cannot be determined
- `doc:3.2.0` — paragraph-level; sentence cannot be determined

---

## IV. Document Reference Format

A `doc_ref` must be:
- Lowercase, underscore-separated
- Suffixed with a version or date identifier where the document is versioned
- Registered in the tenant's document registry before claims can cite it

**Examples:**

| Source | `doc_ref` |
|---|---|
| "Strategy Deck Q1 2026" | `strategy_deck_2026q1` |
| "Board Memo March 2026" | `board_memo_2026_03` |
| "GAQP Master v1.0" | `gaqp_master_v1` |
| "Series A Term Sheet" | `series_a_term_sheet_v2` |
| "Earnings Call Transcript Q4 2025" | `earnings_call_2025q4` |
| Conversation session | `session_{session_id}` |

---

## V. Application to GAQP Claims

The `source_location` field in a GAQP claim accepts a document coordinate:

```json
{
  "claim_id": "abc123",
  "claim_text": "Fixed-ops revenue carries a 60%+ gross margin at scale.",
  "source_location": "investor_brief_2026q1:2.3.1",
  "provenance_source": "investor_brief_2026q1"
}
```

For claims extracted from conversational sessions, the coordinate is:

```
session:{session_id}:{turn_number}.{sentence_number}
```

Example: `session:d4a9f1b2:14.2` — Session d4a9f1b2, turn 14, sentence 2.

---

## VI. Why Sentence-Level Resolution Matters

A paragraph may contain both a thesis and its qualification. Extracting the thesis without its qualification produces a misleading claim. Sentence-level coordinates force the extractor to identify exactly what was asserted — not what the paragraph was generally about.

A claim without a sentence-level coordinate is a claim whose scope is ambiguous. Ambiguous scope is an admission failure under Test 1 (Stand-Alone).

---

## VII. Rehydration Use Case

The coordinate system enables rehydration — the ability to reconstruct the precise context of a claim on demand.

When an operator asks: *"Where did this claim come from?"* the system can return:
- The document reference
- The surrounding paragraph
- The adjacent sentences for context
- The full section if requested

This is the difference between a citation and a live anchor.

---

## VIII. Governing Rule

> Every GAQP claim produced from a document source must carry a document coordinate accurate to at least the paragraph level. Sentence-level resolution is required for claims extracted from text. Document-level coordinates are permitted only for claims derived from oral or unstructured sources where finer resolution is unavailable.

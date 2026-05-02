# GAQP Granularity Doctrine

**Status:** Canonized
**Version:** 1.0
**Date:** 2026-05-02
**Authority:** Execalc GAQP Standards Body

---

## I. The Foundational Move

Every field that made a step-change advance did so by finding the natural granularity of its subject — the level at which the object can no longer be divided without losing what makes it meaningful.

- **Finance** found the transaction. Not the annual report, not the quarterly summary — the individual ledger entry. GAAP says: record at transaction level. Aggregate up from there. The entire discipline of financial governance became possible only after the right atomic unit was identified.
- **Chemistry** found the atom. Not the substance, not the compound — the indivisible unit. Periodicity, bonding, reaction prediction — none of it was visible until analysis operated at the right resolution.
- **Genomics** found the base pair. Not the organism, not the gene — the nucleotide sequence. The entire sequencing revolution required operating at that granularity.

GAQP found the claim. Not the document, not the conversation, not the session — the atomic governed claim. The smallest unit of qualitative knowledge that carries standalone meaning and can be evaluated, classified, composed, and retrieved without reference to its source container.

GAQP did not invent the claim. It identified the claim as the natural granularity of qualitative knowledge and built a governance standard around it. That is the same move GAAP made with the transaction.

---

## II. Why the Document Is the Wrong Granularity

Documents are arbitrary containers. They do not correspond to any natural unit of meaning. A fifty-page report may contain four governed claims, twelve hedges, twenty-two restatements of prior points, six context paragraphs, and an executive summary that restates everything twice. Every element is stored at identical granularity — same file, same retrieval unit. The system makes no distinction between the signal and the scaffolding.

When you need the insight, you retrieve the entire container and decompress it manually. Every time. The retrieval cost scales with the document, not with the claim.

**The critical information-theoretic constraint:** you can go from fine granularity to coarse, but never from coarse to fine. Store at document granularity and the signal is permanently entangled with the noise. You cannot later disaggregate to the claim without re-processing the entire document. The entanglement is structural, not incidental.

This is why every knowledge management system ever built eventually fails at retrieval. It was storing at the wrong level. Better search, better tagging, better summarization — all of these are attempts to compensate for operating at the wrong granularity. They do not solve the problem. They manage it.

---

## III. What Claim-Level Granularity Enables

Operate at claim granularity and capabilities emerge that are structurally impossible at document granularity.

**Precision retrieval.** Not "give me the 2022 market analysis" — "give me every governed claim about market consolidation in the Southeast real estate sector with confidence above 0.72 that is still within its durability window, ranked by retrieval priority." That query is impossible at document granularity. It is trivial at claim granularity.

**Composability.** Fine-grained units compose. Documents do not. A Heuristic from a 2022 deal analysis combined with a Threshold Condition from a 2024 board session can synthesize a new governed position. At document granularity, that synthesis requires a human to read both documents and perform the combination manually — every time it is needed.

**Temporal differential.** Documents age uniformly — a 2019 report is "old." Claims age by type. An Axiom from 2019 may still be Structural. An Observation from 2019 may be expired. A time-sensitive Opportunity from 2019 has been promoted to Institutional Precedent. GAQP retrieves at the right temporal resolution: not "is this document current?" but "is this specific claim still valid given its type and durability class?"

**Confidence tracking.** You cannot attach a confidence score to a document. You can attach one to a claim. The confidence ladder — Seed through Structural — is only coherent at claim granularity. Document-level confidence is meaningless: the document contains claims at many confidence levels simultaneously.

**Corroboration.** Two documents that contain the same insight cannot automatically corroborate each other — the system has no mechanism to recognize the equivalence. Two claims carrying the same governed language can. GAQP's corroboration engine, and the Second Memoralization Rule, only function because claims are stored as discrete addressable objects with comparable structure.

**Synthesis at scale.** The 44:1 noise-to-signal ratio means a corpus of 1,000 documents contains roughly 4,000 governed claims embedded in 44,000 units of scaffolding. At document granularity, synthesis must process all 45,000 units. At claim granularity, synthesis operates on 4,000 units. The reduction is not stylistic. It is structural.

---

## IV. The 44:1 Ratio as a Granularity Ratio

The 44:1 noise-to-signal compression ratio is not a compression ratio in the engineering sense. It is the cost of operating at the wrong granularity.

A fifty-page document contains approximately one governed claim per twelve pages — an estimated 44 units of scaffolding (context, hedging, narrative, repetition, transition) for every one unit of extractable governed signal. All of it is stored at identical granularity. The scaffolding does not cost more to store. It costs just as much to retrieve.

GAQP does not compress the document. It identifies the signal inside it and stores that signal at its natural resolution. The scaffolding remains in the source record for provenance and reference. It simply stops being the retrieval unit.

The ratio will vary by document type. A scouting report compresses differently than a board presentation. A LinkedIn post compresses differently than a legal opinion. The directional claim — that documents are overwhelmingly scaffolding relative to governed signal — is not controversial to any reader of organizational material. The exact ratio is under empirical validation.

---

## V. The Four-Part Atom Test

A claim is a GAQP atom if and only if it satisfies all four conditions:

1. **Standalone meaning** — it is understandable without reference to surrounding context
2. **Evaluability** — it can be assessed for truth, confidence, or reliability
3. **Classifiability** — it maps to exactly one of the 24 canonical GAQP claim types
4. **Composability** — it can be combined with other claims without first reconstructing its source document

If a statement passes all four, it is an atom. If it requires surrounding material to carry meaning, it is scaffolding. Scaffolding does not belong in the governed corpus — it belongs in the source record where provenance requires it.

This test is the operational definition of "atomic nugget." It is not a judgment call. It is a structural test.

---

## VI. Why This Became Possible Now

Claim-level granularity as a governance standard requires extraction capability. Manually decomposing documents into governed claims at scale is not operationally viable — the labor cost would exceed the value for all but the most critical documents.

AI-assisted extraction is what makes claim-level granularity practical for the first time. A governed AI runtime can decompose a document into candidate claims, classify each against the 24-type taxonomy, score confidence, assign durability, and populate the full metadata schema — in seconds, at scale, across every document an organization produces.

The intellectual standard — the claim as the natural atom of qualitative knowledge — has always been correct. The operational infrastructure to enforce it at enterprise scale is new. GAQP is the standard. Execalc is the enforcement runtime.

This is the same dynamic that made GAAP possible: double-entry bookkeeping had existed in principle for centuries. Standardized enforcement across enterprises became possible only when the organizational infrastructure to require and verify it existed. The standard predated the infrastructure. GAQP follows the same pattern.

---

## VII. Granularity and the Pitch

The granularity argument is the most defensible answer to "why hasn't this been done before?"

Because documents were the only practical container — and document-level granularity was the only operationally viable option. Knowledge management, search, summarization, and AI tools have all operated at document granularity because extracting and governing individual claims at scale was not possible.

It is now. GAQP defines the standard. Execalc enforces it. The document was never the right unit. It was the only available unit.

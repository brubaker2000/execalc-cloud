# EKE_MONOLITH_SEED_CORPUS_MANIFEST.md

## Status
Draft v0.1 — pre-classification

## Owner
Executive Knowledge Engine (EKE)

## Purpose
This manifest governs the EKE Monolith Seed Corpus — the initial heuristic dataset that forms the foundational content layer of Execalc's judgment engine.

The corpus data is stored in `EKE_MONOLITH_SEED_CORPUS.md` (this directory).

---

## What This Corpus Is

The seed corpus is the earliest structured inventory of strategic heuristics, frameworks, and principles intended to populate the EKE Monolith and associated cartridges.

It is not a reading list. It is a pre-admission dataset of candidate judgment assets.

**It is not yet governed.** No entry has passed the six-test admission filter. No entry has been formally classified under the EKE Heuristic Object Classification Model (`docs/architecture/EKE_HEURISTIC_OBJECT_CLASSIFICATION_MODEL.md`). Runtime activation of any entry is prohibited until admission and classification are complete.

---

## Source Breakdown

| Source Set | Entry Range | Count | Primary Authors |
|---|---|---|---|
| Historical Thought Leaders (HTL) | HTL-0001 to HTL-0145 | 145 | Covey, Musashi, Drucker, Sun Tzu, Willink, Munger, Buffett, Dalio, Bezos, Musk, Ravikant, Welch, Sinek, Grove, Boyd, Clausewitz, Kahneman, Taleb, Christensen, Porter, Voss |
| Contemporary Thought Leaders (CTL) | CTL-0001 to CTL-0041 | 41 | Grant, Ulwick, Bain/McKinsey, Minto, Holmes, Moore, Ries, Collins, Doerr, Kotter, Lencioni, Rumelt, Snowden, Meadows, Schein, Goldratt, Sutherland, Scott, Buckingham, Senge, Charan, Thaler, Ohno, Amabile, Davenport, Kim/Mauborgne, and others |
| Perry Marshall Carat Set (PM) | PM-0001 to PM-0038 | 38 | Perry Marshall |
| Jay Abraham Executive Module (JA) | JA-0001 to JA-0006 | 6 | Jay Abraham |
| **Total** | | **230** | |

---

## Schema (19 Columns)

| Column | Description |
|---|---|
| Source | Source set (HTL / CTL / PM / JA) |
| Heuristic ID | Stable corpus ID |
| Author / Source | Originating thinker or source |
| Heuristic (Concept) | Name and brief behavioral instruction |
| Use Case | Scenario context where this entry applies |
| Activation Context | Runtime surface where it should activate |
| Strategic Domain | Domain classification |
| Decision Type | Tactical / Strategic / Operational / Cognitive / Communication |
| Polarity Traits | Balanced / Aggressive / Deliberate / Contrarian / Stable / Adaptive |
| Conflict Pair(s) | Known conflict pairs with other entries or approaches |
| Confidence Score | Default / Proven / Timeless / Applied Expert / Theoretical / Emerging Practice / Trending / Widely Adopted |
| Contradiction Map Flag | Yes / No |
| Trigger Phrase(s) | Natural language signals that should activate this entry |
| Cartridge Inclusion | Yes = candidate for Execalc runtime cartridge packaging |
| Level of Abstraction | Conceptual / Operational / Model-Level / Meta-Theory |
| Historical Context | Era of origin |
| Tag Cluster | Keyword tags |
| Override Flag | Yes = this entry can override default behavior |
| Strategic Theme | Governing theme for clustering |

---

## Cartridge Inclusion Candidates

Entries marked `Cartridge Inclusion: Yes` are candidates for packaging into Execalc runtime cartridges. These require full Carat Registry Standard review before activation.

| Source Set | Cartridge-Eligible Count | Notes |
|---|---|---|
| HTL | ~15 entries | Primarily Sun Tzu, Boyd, Taleb, Voss |
| CTL | Several | Snowden (Cynefin), Sutherland (Scrum) |
| PM (all 38) | 38 | Entire Perry Marshall set flagged for cartridge |
| JA (all 6) | 6 | Entire Jay Abraham set flagged for cartridge |

---

## Override Flag Entries

Entries marked `Override Flag: Yes` can override default system behavior. These carry elevated governance risk and require priority review before any activation.

Known override-flagged entries: HTL-0036 (Munger — Invert), HTL-0048 (Dalio — Radical Transparency), CTL-0001 (Grant — Original Thinkers), CTL-0026 (Scott — Radical Candor).

---

## Ontological Classification Status

**Current status: UNRESOLVED.**

Per `EKE_HEURISTIC_OBJECT_CLASSIFICATION_MODEL.md`, every entry must be assigned a primary object class before runtime use:
- Heuristic
- Principle
- Mental Model
- Reflex
- Communication Stance

The Polarity and Decision Type columns in the raw schema provide partial signal for classification but do not substitute for formal classification.

**Reclassification priority order:**
1. Override Flag entries (highest activation risk)
2. Cartridge Inclusion entries (next highest activation risk)
3. HTL entries by Confidence Score: Timeless → Proven → Applied Expert
4. CTL entries
5. PM and JA entries

---

## EKE Stratum Mapping

| Source Set | Primary Stratum | Notes |
|---|---|---|
| HTL — Timeless/Proven | Monolith (Synthesized Pattern Engine) | Core shared baseline |
| HTL — Applied Expert | Monolith / Thought Leadership Nuggets | Author-attributed atomic insights |
| CTL | Thought Leadership Nuggets | Contemporary frameworks, modular |
| PM | Execalc Runtime Cartridges (candidate) | Carat-eligible; requires registry review |
| JA | Execalc Runtime Cartridges (candidate) | Carat-eligible; requires registry review |

---

## Strategic Theme Inventory

Themes present in the corpus (from Tag Cluster and Strategic Theme columns):

- Leadership Discipline
- Tempo Control
- Conflict Strategy
- Moral Authority
- Value Creation
- Systems Design
- Innovation Timing
- Strategic Positioning
- Cognitive Discipline
- Risk Logic
- Signal Management
- Platform Integrity
- Capital Discipline
- Contrarian Advantage
- Trust Positioning
- Revenue Design
- General Management Logic
- Strategic Architecture
- Execution Without Excuses
- Innovation Design

---

## Required Follow-On Actions

1. Complete ontological classification of all 230 entries (priority order above)
2. Formal admission review (six-test filter) for entries marked Cartridge Inclusion = Yes
3. Carat Registry Standard review for Perry Marshall and Jay Abraham sets
4. Conflict pair mapping — entries with known conflict pairs need arbitration rules
5. Trigger phrase audit — many entries have generic triggers ("strategy, execution, default") that need sharpening

---

## Maintenance Note

This manifest is the governance anchor for the corpus. The corpus data file (`EKE_MONOLITH_SEED_CORPUS.md`) is the content. If they conflict, this manifest governs.

Last updated: 2026-04-14

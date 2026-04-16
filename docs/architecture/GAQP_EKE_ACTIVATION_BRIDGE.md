# GAQP_EKE_ACTIVATION_BRIDGE.md

## Status
Draft v0.1 — Pre-Stage-9 architecture spec

## Owner
Architecture / Stage 9

## Purpose
This document defines the shared activation vocabulary and matching architecture that connects the GAQP extraction layer to the EKE corpus at artifact-level granularity — below the scenario level.

It exists because the current matching model is coarse: scenario detection routes to a scenario bucket, and all corpus entries tagged to that scenario load uniformly. This works but is imprecise. A specific causal claim about buyer trust erosion should activate trust-repair heuristics specifically — not every sales negotiation entry in the corpus.

The bridge closes that gap.

---

## The Problem in Precise Terms

Two systems currently operate on separate vocabularies:

**GAQP extraction produces:** typed artifacts (19 types) carrying metadata — domain, polarity, confidence, source. These describe *what kind of claim* was extracted.

**EKE corpus contains:** thought leader entries classified by object class (Heuristic, Principle, Mental Model, Reflex, Communication Stance). These carry scenario tags and thinker attribution. They describe *what kind of knowledge* is stored.

**They currently meet at:** the scenario level. Scenario detection identifies "this is a sales negotiation scenario" and loads all corpus entries tagged to that scenario. The GAQP-extracted artifacts are not yet part of the matching equation.

**The gap:** Two operators facing "sales negotiation" scenarios with structurally different problems receive the same corpus. One has a leverage problem. One has a trust problem. The scenario tag cannot distinguish them. The artifacts can.

---

## The Solution: Shared Activation Vocabulary

A controlled vocabulary applied consistently to both sides — so that GAQP-extracted artifacts and EKE corpus entries carry the same tags and can be matched at artifact granularity.

The vocabulary has three dimensions:

---

### Dimension 1: Situation Class

The class of situation the artifact describes or the corpus entry addresses.

**Controlled vocabulary (v0.1):**

| Tag | Description |
|---|---|
| `negotiation` | Structured exchange with a counterparty over terms, value, or commitment |
| `capital_allocation` | Decisions about how money, equity, or resources are deployed |
| `team_dynamics` | Relationships, trust, conflict, and performance among people |
| `market_positioning` | How the organization stands relative to competitors and customers |
| `competitive_pressure` | Active competitive threats or displacement risk |
| `organizational_friction` | Internal resistance, misalignment, or execution drag |
| `hiring_and_talent` | Acquiring, retaining, and deploying human capability |
| `execution_management` | Getting work done against a plan under constraints |
| `strategic_planning` | Determining direction, priorities, and allocation at the portfolio level |
| `risk_evaluation` | Assessing downside, probability, and exposure |
| `crisis_response` | High-pressure, time-compressed situations with elevated stakes |
| `governance` | Authority structures, decision rights, compliance, and audit |
| `customer_relationship` | Managing and evolving relationships with buyers or clients |
| `partnership` | Joint ventures, alliances, distribution agreements, co-development |

An artifact or corpus entry may carry more than one Situation Class tag. Multi-tagging is expected. An artifact about pricing during a negotiation carries both `negotiation` and `capital_allocation`.

---

### Dimension 2: Dynamic Class

The underlying structural dynamic the artifact describes or the corpus entry addresses. This is the most discriminating dimension — it identifies the pattern beneath the situation.

**Controlled vocabulary (v0.1):**

| Tag | Description |
|---|---|
| `information_asymmetry` | One party knows more than the other; knowledge gap is leverage |
| `incentive_misalignment` | Parties are optimizing for different objectives |
| `leverage` | One party holds structural power advantage over the other |
| `urgency` | Time pressure affecting decision quality or forcing premature commitment |
| `trust_deficit` | Insufficient confidence between parties; relationship risk |
| `resource_scarcity` | Hard constraints on capital, time, talent, or attention |
| `stakeholder_conflict` | Competing interests within the same organization or partnership |
| `commitment_escalation` | Sunk cost dynamics; pressure to continue a failing path |
| `uncertainty` | Insufficient information to act with confidence |
| `optionality` | Tension between preserving future choices and committing now |
| `market_timing` | Window-dependent decisions where timing changes the outcome |
| `execution_friction` | Internal resistance or capability gaps blocking implementation |
| `signal_noise` | Difficulty distinguishing material signal from irrelevant noise |
| `complexity` | Too many interdependent variables to reason linearly |
| `authority_ambiguity` | Unclear who has decision rights; governance gap |
| `alignment` | Building shared understanding and commitment to a direction |

---

### Dimension 3: Prime Directive Lens

Which Prime Directive lens does this artifact primarily concern?

| Tag | Description |
|---|---|
| `assets_liabilities` | Balance sheet impact; what this does to the position |
| `risk_reward` | Whether the risk/reward ratio is favorable and explicit |
| `supply_demand` | Whether a structural imbalance is being leveraged or exposed |

Every corpus entry should carry at least one PD lens tag. Untagged entries are not PD-aligned and cannot be activated in the Prime Directive gate.

---

## The Tag Schema

### On GAQP Artifacts

Every extracted and classified artifact acquires an `activation_tags` block after classification, before admission:

```json
{
  "claim_id": "claim-0047",
  "claim_type": "Causal_Claim",
  "claim_text": "Buyers who delay signing after a price anchor are signaling trust deficit, not budget constraint.",
  "activation_tags": {
    "situation_class": ["negotiation"],
    "dynamic_class": ["trust_deficit", "information_asymmetry"],
    "pd_lens": ["risk_reward"]
  }
}
```

The activation tagger runs after classification. It does not run during extraction (that would conflate operations — see GAQP Recognition Standard). Tagging is a classification-layer responsibility.

---

### On EKE Corpus Entries

Every corpus entry carries an `activation_tags` block alongside its existing scenario tags:

```json
{
  "entry_id": "CTL-0014",
  "thinker": "Voss",
  "object_class": "Heuristic",
  "fragment": "When the buyer goes silent after an anchor, wait. The first one to speak loses leverage.",
  "scenario_tags": ["sales_negotiation", "closing"],
  "activation_tags": {
    "situation_class": ["negotiation"],
    "dynamic_class": ["leverage", "information_asymmetry", "urgency"],
    "pd_lens": ["risk_reward"]
  }
}
```

Scenario tags and activation tags coexist. Scenario tags govern the existing scenario-based retrieval path. Activation tags govern the artifact-based retrieval path. Both can activate a corpus entry.

---

## The Scoring Model

When a GAQP artifact is extracted with activation tags, the corpus retrieval engine scores each corpus entry by tag-intersection depth.

### Scoring Formula

```
relevance_score = (0.45 × dynamic_match_score) +
                  (0.35 × situation_match_score) +
                  (0.20 × pd_lens_match_score)
```

Where each sub-score is:

```
sub_score = (matching_tags / max(artifact_tags, corpus_tags)) × quality_factor
```

`quality_factor` = 1.0 for exact tag matches, 0.7 for adjacent tags (defined in the tag adjacency map, see Section: Tag Adjacency).

### Weighting Rationale

**Dynamic Class (0.45):** The highest weight. Dynamic Class is the most discriminating tag — it identifies the structural pattern beneath the situation. Two different situations with the same dynamic (e.g., `trust_deficit` appears in both customer negotiations and board presentations) should activate the same corpus entries. Dynamic Class cuts across Situation Class boundaries.

**Situation Class (0.35):** The second weight. Provides context specificity. An entry tagged `negotiation` is more relevant than a generically tagged one, even if the dynamic matches.

**PD Lens (0.20):** The third weight. All entries should be PD-aligned; this dimension discriminates between entries that primarily address assets/liabilities vs. risk/reward vs. supply/demand.

---

### Activation Threshold

| Score Range | Action |
|---|---|
| ≥ 0.70 | High-confidence activation — include in context package |
| 0.50–0.69 | Candidate — include if token budget allows; surface to operator as "related" |
| < 0.50 | Below threshold — do not activate |

**Hard requirement:** At least one `dynamic_class` tag must match for any entry to cross the 0.50 threshold. A corpus entry with no dynamic match cannot activate via this pathway regardless of situation or PD lens match.

---

## Tag Adjacency Map

Some tags are structurally adjacent — a close enough match that it earns partial credit (0.7 × weight).

| Tag | Adjacent Tags |
|---|---|
| `leverage` | `information_asymmetry`, `authority_ambiguity` |
| `trust_deficit` | `alignment`, `stakeholder_conflict` |
| `urgency` | `market_timing`, `commitment_escalation` |
| `resource_scarcity` | `commitment_escalation`, `execution_friction` |
| `uncertainty` | `signal_noise`, `complexity` |
| `organizational_friction` | `execution_friction`, `stakeholder_conflict` |

Adjacency is not reciprocal by default — the map specifies the direction. `leverage` is adjacent to `information_asymmetry` (because leverage often derives from information asymmetry), but not vice versa (information asymmetry does not automatically imply leverage).

---

## Integration with Scenario Detection

The activation bridge is additive. It does not replace scenario detection.

### Existing pathway (unchanged):
```
Scenario detection → scenario_id → corpus entries tagged to that scenario loaded
```

### New pathway (additive):
```
GAQP artifact extraction → activation tagging → tag-intersection scoring → corpus entries above threshold loaded
```

### Combined activation logic:

A corpus entry may activate via either pathway. An entry that activates via both pathways receives an elevated priority score and is placed higher in the context package.

**Conflict handling:** If scenario-based retrieval and artifact-based retrieval produce overlapping entries, the overlap entries are loaded once at elevated priority. If they produce divergent entries (scenario retrieval suggests one set, artifact matching suggests another), both sets are included up to the token budget, with artifact-matched entries listed first.

---

## Corpus Tagging Requirement

Every EKE corpus entry must carry activation tags before it is eligible for runtime activation.

**Entries without activation tags:** dormant. They can be loaded via scenario-based retrieval only (legacy pathway). They cannot participate in artifact-level matching until tagged.

**Priority tagging order:** Reflexes first (highest activation risk), then Heuristics, then Principles, then Mental Models, then Communication Stances. This mirrors the reclassification protocol in `EKE_HEURISTIC_OBJECT_CLASSIFICATION_MODEL.md`.

**Corpus tagging is a Stage 9A prerequisite.** The 230 seed corpus entries must be activation-tagged before Stage 9B memory admission can be completed. Untagged corpus entries produce coarser outputs; the tag-intersection matching pathway does not engage.

---

## Extraction Tagging Requirement

Every GAQP artifact must be activation-tagged after classification and before admission.

The activation tagger is a classification-layer component:

```
Extraction → Classification (type assigned) → Activation Tagging (tags assigned) → Admission (seven-test filter)
```

The tagger is not the admission gate. Activation tags are assigned to candidates before admission. A candidate that fails admission is tagged but not admitted — its tags are not wasted; they inform the extraction pattern for future sessions.

**Tagger implementation options:**

- **Rule-based tagger (v1):** For each claim type, apply default Situation + Dynamic tags based on claim content keywords. Low precision but no LLM call required.
- **LLM-assisted tagger (v2):** A Haiku-class model assigns tags based on claim text + claim type. Higher precision. One lightweight LLM call per artifact.

v1 is sufficient for Stage 9. v2 is a Stage 10 improvement.

---

## How This Connects to the Normative Architecture

The activation bridge is the mechanism through which the normative layer reaches into the informed layer.

The Prime Directive (normative) tells the system what to evaluate. The activation bridge finds the corpus entries (informed) whose PD lens tags match the current evaluation. Without the bridge, the normative layer and the informed layer are connected only at the scenario level. With the bridge, they are connected at the artifact level — a much more precise coupling.

This is also how GAQP extraction becomes operationally meaningful beyond compliance. A GAQP-extracted causal claim about `trust_deficit` in a negotiation does not merely get stored and audited. It activates the Voss heuristics tagged `trust_deficit` and `negotiation`. The extraction feeds the activation, which feeds the synthesis. The three-layer system compounds.

---

## Required Follow-On Specs

1. **Activation Tag Governance Spec** — how new tags are added to the controlled vocabulary; who has authority; review protocol
2. **Tagger Implementation Spec** — rule-based v1 tagger logic for each claim type
3. **Corpus Tagging Runbook** — step-by-step tagging protocol for the 230 seed entries

---

## Design Principle

> The scenario tells the system what room it is in. The activation bridge tells it which tool to pick up. Without the bridge, the system always carries all the tools in that room. With the bridge, it carries the ones the specific situation requires.

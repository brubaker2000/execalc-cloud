# GAQP_ARTIFACT_RECOGNITION_AND_EXTRACTION_STANDARD.md

## Status
Draft v0.1 — Foundational GAQP doctrine

## Owner
GAQP / Architecture

## Position in GAQP
This is the recognition standard — the rules for identifying what in a piece of text constitutes a harvest-worthy artifact, and what type it is. It sits between the GAQP Founding Charter (which establishes the principles) and the admission pipeline (which governs whether a recognized artifact enters active memory).

---

## Part I: Foundations

### The Problem This Standard Solves

The GAQP Founding Charter establishes ten principles. The admission pipeline enforces the six-test filter. But neither answers the prior question:

> **When you are reading a piece of text, how do you know what is worth extracting — and what type of thing it is?**

This is the recognition problem. Without a recognition standard, extraction is intuitive and inconsistent. Two readers of the same document will extract different artifacts, classify them differently, and produce incompatible governing knowledge. That is not a standard — it is organized subjectivity.

This document establishes the standard.

---

### The Three Distinct Operations

These three operations are frequently confused. They are not the same thing and must not be collapsed.

```
EXTRACTION  →  CLASSIFICATION  →  ADMISSION
```

**Extraction** is recognition. Reading a piece of text and identifying that something in it is potentially harvest-worthy. Extraction does not evaluate quality — it identifies candidates.

**Classification** is typing. Determining what kind of artifact the extracted candidate is. An axiom and a result look different, behave differently, expire differently, and serve different purposes in the system. Classification determines which rules apply.

**Admission** is governance. Running the extracted and classified artifact through the six-test filter to determine whether it enters active memory. Most artifacts fail admission. Failure at admission does not mean the extraction was wrong — it means the artifact is not yet ready or not material enough for active memory.

**The critical rule:** These three operations happen in sequence. An artifact is extracted before it is classified. It is classified before it is evaluated for admission. Conflating them — for example, deciding during extraction whether something should be admitted — introduces bias into the extraction layer and causes material artifacts to be lost.

---

### What Makes Something Harvest-Worthy

Before classifying an artifact, the system must determine whether it is worth extracting at all. This is the extraction threshold — below which, text is noise.

An artifact is harvest-worthy if it satisfies at least one of the following:

1. **It could change a future decision.** If the right person read this at the right moment, would it alter what they decided? If no, it is noise.

2. **It encodes a pattern that recurs.** If this is the kind of thing that happens repeatedly, the pattern is worth capturing for future recognition.

3. **It records an outcome connected to a prior action.** Results and decision outcomes are harvest-worthy because they close the feedback loop.

4. **It names a constraint or objective that governs current decisions.** The decision space cannot be understood without these.

5. **It surfaces an assumption that is currently driving behavior but has not been established.** Untagged assumptions are a governance risk.

Anything that does not satisfy at least one of these is below the extraction threshold. It may be interesting language. It is not a governed artifact.

---

### Source Context Is Part of Extraction

The type of artifact you are likely to find depends heavily on the source. A system that does not know what it is reading will misclassify.

| Source Type | Dominant Artifact Types | Notes |
|---|---|---|
| Book / published work | Axiom, Principle, Mental Model, Heuristic, Stratagem, Tendency | Received wisdom; high durability; universal or domain-wide scope |
| Customer conversation | Observation, Assumption, Constraint, Diagnostic Signal | Specific, dated; tenant-scoped; often unvalidated |
| Internal meeting / transcript | Objective, Constraint, Assumption, Event, Tradeoff | Current-state; changes frequently; tenant-scoped |
| Decision post-mortem | Result, Causal Claim, Decision Outcome, Assumption (tested) | Feedback loop material; highest learning value |
| Market research / data | Tendency, Causal Claim, Event, Observation | Statistical; scope-bounded; requires confidence calibration |
| Strategy session | Objective, Stratagem, Tradeoff, Constraint | Forward-looking; often contains assumptions masquerading as facts |
| Competitor analysis | Observation, Diagnostic Signal, Causal Claim, Event | External; requires provenance and confidence tagging |

---

### The Two Families

All artifacts belong to one of two families. This is the most important distinction in the standard.

**Family A: Durable Knowledge**
Artifacts that are expected to remain valid and useful beyond the context in which they were found. They generalize. They travel across time, tenants, and situations. They belong in the EKE corpus, available to all tenants.

Examples: Axioms, Principles, Mental Models, Heuristics, Stratagems, Tendencies.

**Family B: Situated Intelligence**
Artifacts that are specific to a particular organization, time period, or context. They do not generalize. They expire or become historical. They belong in organizational memory, scoped to the tenant that produced them.

Examples: Observations, Events, Results, Constraints, Objectives, Assumptions, Causal Claims (when organization-specific), Decision Outcomes.

**The governance implication:** A Family A artifact from a book goes into the shared EKE corpus. The same artifact type expressed in an internal conversation about a specific organization goes into that organization's tenant-scoped memory. The type may be identical; the scope is not.

---

### Reconciliation: The Revised Unified Taxonomy

The repo currently contains two overlapping taxonomies that were never formally reconciled:

- **GAQP Claim Types (13):** Axiom, Definition, Principle, Heuristic, Best Practice, Tendency, Observation, Event, Constraint, Objective, Tradeoff, Causal Claim, Diagnostic Signal

- **EKE Object Classes (5):** Heuristic, Principle, Mental Model, Reflex, Communication Stance

**The resolution:**

The GAQP Claim Types are the **master ontology** — the complete set of artifact types governing all extraction and classification.

The EKE Object Classes are **runtime roles** — a subset of the GAQP types, refined for how they activate in the EKE at runtime. Every EKE Object Class maps to one or more GAQP Claim Types.

| EKE Object Class | GAQP Claim Type(s) | Notes |
|---|---|---|
| Heuristic | Heuristic | Exact match |
| Principle | Principle or Axiom | Distinguished by scope — Axiom is foundational/rarely disputed; Principle is broad but arguable |
| Mental Model | Principle + Causal Claim | A Mental Model is a Principle that contains an explanatory mechanism |
| Reflex | Heuristic + Diagnostic Signal | A Reflex is a Heuristic pre-loaded for automatic activation on a specific signal |
| Communication Stance | (new type — see Part IV) | No existing GAQP equivalent; governs output delivery, not knowledge content |

**Additions to the GAQP Claim Types** (types missing from the original 13, added by this standard):

| New Type | Rationale |
|---|---|
| Mental Model | Distinct from Principle — contains a causal mechanism, not just a behavioral rule |
| Stratagem | Distinct from Heuristic — a multi-move, positional action sequence, not just a decision rule |
| Assumption | Critical addition — unestablished claims that drive reasoning must be explicitly typed and surfaced |
| Result | Critical addition — the outcome of a prior decision; closes the Prime Directive feedback loop |
| Decision Outcome | New — the composite artifact connecting a Decision Artifact to its Result with retrospective PD evaluation |
| Communication Stance | Governs output delivery posture; must not enter the judgment chain |

**Revised GAQP Claim Type count: 19**

The full type definitions follow in Parts II, III, and IV.

---

## Part II: Pattern Artifacts — The Durable Knowledge Family

These artifacts are expected to remain valid and useful beyond the context in which they were found. They generalize across organizations, time periods, and situations. Primary home: the EKE corpus.

---

### 1. Axiom

**What it is:** A foundational claim accepted as established without requiring proof. The bedrock assumption from which other reasoning is built.

**Recognition signals in text:**
- Stated without qualification or hedging
- Used as a premise for other claims, not as a conclusion from evidence
- So foundational that challenging it would require challenging the entire framework
- Often framed as universal: "People respond to incentives." "Every organization is a reflection of its leadership."

**Distinguished from Principle:** A Principle can be argued for; it has justification. An Axiom is built upon. You don't debate an axiom — you decide whether to accept it as a foundation.

**Example:** "Markets have winners and losers." (foundational to competitive strategy; not argued, assumed)

**Durability:** Essentially permanent. Axioms do not expire.

**Confidence default:** High. If something is being used as an axiom but has contested empirical support, it should be reclassified as an Assumption.

**Runtime role:** Foundation of reasoning scaffolds. Activates at scenario framing, not during specific judgment steps.

---

### 2. Principle

**What it is:** A broad behavioral rule that holds across many contexts. Governs how to approach a domain or situation, not what specific action to take.

**Recognition signals in text:**
- Broader than a situation-specific recommendation
- Framed as a general rule: "always," "in general," "as a rule"
- Applies across many different scenarios
- Can be argued for — there is reasoning behind it, not just assertion

**Distinguished from Heuristic:** A Principle governs framing and approach. A Heuristic prescribes a specific action. "Begin with the end in mind" is a Principle — it tells you how to orient, not what move to make. "When the buyer goes silent, wait" is a Heuristic — it prescribes a specific action.

**Example:** "Preserve optionality until the decision must be made." (Covey/Munger)

**Durability:** Long. Principles survive context changes. They can become obsolete but rarely do quickly.

**Confidence default:** Medium-high. Can be corroborated by multiple thinkers.

**Runtime role:** Activates during scenario framing; shapes how the problem is structured before specific heuristics apply.

---

### 3. Tendency

**What it is:** A directional pattern that holds more often than not. Describes what usually happens — not what always happens, not what you should do.

**Recognition signals in text:**
- Probabilistic language: "tend to," "usually," "often," "more often than not"
- Describes patterns across cases, not rules for individual decisions
- Observational in character — based on what has been seen, not prescribed

**Distinguished from Heuristic:** Tendency is descriptive ("this is what usually happens"). Heuristic is prescriptive ("this is what to do when it happens"). They are frequently paired — the Tendency provides the empirical basis for the Heuristic.

**Example:** "Early-stage companies tend to underinvest in sales and overinvest in product." (observed pattern)

The companion heuristic would be: "Hire your first salesperson before you think you need one."

**Durability:** Medium. Tendencies can change as markets, technologies, or human behavior evolves. Should carry a time horizon tag.

**Confidence default:** Medium. Requires corroboration — a single source claiming a tendency is weaker than multiple independent observations.

**Runtime role:** Activates during scenario analysis; provides baseline expectations against which the current situation can be evaluated.

---

### 4. Heuristic

**What it is:** A reliable action rule under uncertainty. Tells you what to do in a defined situation. Reduces deliberation time. Bounded and fallible — it works reliably but not universally.

**Recognition signals in text:**
- Action-prescriptive: "when X, do Y"
- Bounded by context: does not claim universal applicability
- Derived from experience: usually traceable to someone's repeated practice
- Fast-activating: intended to shortcut analysis, not replace it

**Distinguished from Stratagem:** A Heuristic is a single-move rule. A Stratagem is a multi-move positional sequence. "When the buyer goes silent, wait" is a Heuristic. "Attack the center to draw their reserves, then flank from the left" is a Stratagem.

**Example:** "When the buyer goes silent after an anchor, wait. The first one to speak loses leverage." (Voss)

**Durability:** Medium-long. Heuristics survive until the context they were designed for changes significantly.

**Confidence default:** Medium. Heuristics should be empirically tracked — Decision Outcomes that reference a heuristic either validate or challenge it over time.

**Runtime role:** Activates during decision synthesis. Supplies a judgment shortcut. The most common EKE corpus activation type.

---

### 5. Mental Model

**What it is:** A structured representation of how a system works. Enables reasoning by providing an explanatory mechanism — not just a rule, but an understanding of the causal structure underneath it.

**Recognition signals in text:**
- Explains a mechanism: "this is how X works"
- Contains an implicit or explicit causal structure
- Transferable across domains: the same model applies in different fields
- Often has a named framework or analogy attached

**Distinguished from Principle:** A Principle says "do this." A Mental Model says "this is how the system works, and given that understanding, here is how to reason about it." First principles thinking is a Mental Model. "Begin with the end in mind" is a Principle.

**Example:** "Second-order thinking: before deciding, ask what the consequences of the consequences are." (Munger)

**Durability:** Long. Mental Models are among the most durable artifacts — they rarely expire because they describe structural realities rather than contextual patterns.

**Confidence default:** High for well-established models with broad corroboration.

**Runtime role:** Activates during analysis phase. Supplies the reasoning scaffold for working through the problem before heuristics are applied.

---

### 6. Stratagem

**What it is:** A specific multi-move sequence or positional approach effective under defined conditions. More tactical than a heuristic — it implies a sequence of moves with a positional goal, not just a single response rule.

**Recognition signals in text:**
- Implies a sequence of steps or positions, not a single action
- Contains a positional objective: "in order to achieve X, do A, then B, then C"
- Often military, negotiation, or competitive in character
- Conditions for activation are explicitly defined

**Distinguished from Heuristic:** A Heuristic is a single-move decision rule. A Stratagem is a chess-like sequence — it accounts for the opponent's response and positions for a subsequent move.

**Example:** "Attack where they are unprepared. When they reinforce that position, you have drawn their reserves — then strike the undefended flank." (Sun Tzu)

**Durability:** Medium-long. Stratagems survive as long as the competitive or negotiation dynamics they address remain structurally similar.

**Confidence default:** Medium. Stratagems are often domain-specific and require validation in the operator's context.

**Runtime role:** Activates in competitive, negotiation, or high-stakes scenario types. Provides a sequence template, not just a response rule.

---

### 7. Definition

**What it is:** A specification of what a term means within a specific context or framework. Not a universal dictionary definition — a governed operational definition for use within a reasoning system.

**Recognition signals in text:**
- Explicitly defines a term for use in the current context
- May narrow a broad term or give precise technical meaning
- Often followed by or preceded by reasoning that depends on the definition being accepted

**Example:** "For the purposes of this analysis, 'market leadership' means holding the largest share of a defensible, profitable segment — not total category volume." (operational definition)

**Durability:** Tied to the framework or context that uses it. Definitions within a specific analytical framework persist as long as the framework is active.

**Confidence default:** Not applicable — Definitions are not empirical claims.

**Runtime role:** Loads at scenario framing to ensure consistent use of terms across the judgment chain.

---

### 8. Best Practice

**What it is:** A method or approach that has been demonstrated through experience to produce superior outcomes in a defined context. An empirically validated heuristic — a Heuristic with a track record.

**Recognition signals in text:**
- References demonstrated outcomes: "organizations that do X consistently achieve Y"
- Often from research, case studies, or established operational experience
- Has a higher evidentiary basis than a bare heuristic

**Distinguished from Heuristic:** A Heuristic is a reliable rule derived from experience. A Best Practice has documented, comparative evidence of superior outcomes. The evidentiary bar is higher.

**Example:** "Post-mortems conducted within 48 hours of an incident produce higher-quality learning than those conducted two weeks later." (documented operational finding)

**Durability:** Medium. Best Practices can become outdated when conditions change significantly.

**Confidence default:** Medium-high. Higher than a Heuristic by definition — but can degrade if the conditions that produced the evidence no longer hold.

**Runtime role:** Same as Heuristic but with higher initial confidence weighting. May override a conflicting Heuristic during synthesis.

---

## Part III: Situated Intelligence — The Factual and Interpretive Families

These artifacts are specific to a particular organization, time period, or context. They do not generalize. They belong in organizational memory, tenant-scoped. Most have expiration characteristics.

---

### 9. Observation

**What it is:** Something directly perceived or witnessed. Raw, uninterpreted input — the earliest stage in the artifact lifecycle. An observation records what was seen or heard, not what it means.

**Recognition signals in text:**
- First-person or direct witness framing: "the CFO said," "we observed," "the data shows"
- Not yet interpreted — records the phenomenon, not its significance
- Source is specific and traceable

**The critical rule:** Observations must never be conflated with interpretations. "The CFO expressed concern about margins" is an Observation. "The company is facing a profitability crisis" is an Interpretation. GAQP requires these to be stored separately.

**Example:** "In the Q3 board meeting, the CFO stated that gross margins had compressed 400 basis points year-over-year." (direct, attributed, uninterpreted)

**Durability:** Short to medium. Observations are specific moments. Their factual content may be permanent but their relevance decays.

**Confidence default:** Tied to source reliability and directness. First-hand observation outweighs reported observation.

**Runtime role:** Raw input to the interpretation and analysis layers. Does not activate heuristics directly — Diagnostic Signals derived from Observations do.

---

### 10. Event

**What it is:** Something that happened at a specific time. Bounded, dated, specific. An Event is a completed occurrence — it cannot be undone.

**Recognition signals in text:**
- Specific time reference: "in Q3," "on the 14th," "last month"
- Completed action: something that already happened
- Bounded: has a start and implicitly an end

**Distinguished from Observation:** An Observation is what was perceived. An Event is what occurred. You observe an Event — but the Event exists independently of being observed. A competitor raising capital is an Event whether or not your team witnessed it.

**Example:** "Competitor raised $50M Series C in January, led by [firm], at a $250M post-money valuation."

**Durability:** Permanent as a historical record. Decreasing in decision relevance over time.

**Confidence default:** Tied to source quality. Public events (filings, press releases) are high confidence. Rumor-sourced events are low confidence and must be labeled as such.

**Runtime role:** Activates in competitive intelligence, due diligence, and crisis management scenarios. Provides temporal anchoring for causal reasoning.

---

### 11. Result

**What it is:** The recorded outcome of a prior action or decision. The feedback loop. What actually happened after a decision was executed.

**Why Results are the most undervalued artifact type:** Everyone captures principles and heuristics. Almost no organization systematically connects decisions to their outcomes. Without Results, the EKE corpus is received wisdom with no empirical correction. With Results, heuristics can be validated, challenged, or refined against organizational experience.

**Recognition signals in text:**
- References a prior action: "after we launched," "following the pivot," "since the policy change"
- States what actually happened: measurable, observable outcome
- Can be connected to the decision or action that preceded it

**Distinguished from Event:** An Event is something that happened. A Result is something that happened *as a consequence of a prior decision or action.* Results have a causal ancestry. Events may or may not.

**Example:** "We launched the Southeast expansion in Q1. By Q3, we had captured 6% market share in the region, below the 10% target, due to underestimation of the incumbent's distribution network."

**Durability:** Permanent as a historical record. Highest activation value when evaluating similar future decisions.

**Confidence default:** High for directly measured outcomes. Medium for partially observed or reported outcomes.

**Runtime role:** Feeds back into heuristic validation. Activates during scenario analysis when the current situation resembles a situation that produced a recorded result.

---

### 12. Constraint

**What it is:** A limitation on what is possible in the current decision context. Reduces the decision space. Constraints are not preferences — they are boundaries that cannot be crossed without consequence.

**Recognition signals in text:**
- Limiting language: "cannot," "must not," "is prohibited," "is required before"
- Structural: the constraint exists independent of what anyone prefers
- Often regulatory, financial, organizational, or contractual in nature

**Distinguished from Objective:** A Constraint is what limits what you can do. An Objective is what you are trying to achieve. Constraints are binary (you either respect them or you don't). Objectives are directional (you can be closer to or farther from them).

**Example:** "We cannot raise prices more than 8% without triggering the MFN clause in the enterprise contract."

**Durability:** Tied to the underlying condition that creates the constraint. Contractual constraints expire with the contract. Regulatory constraints change with regulation.

**Confidence default:** High for documented, formal constraints. Medium for informal or implied constraints.

**Runtime role:** Loads into the context package as a hard boundary. The Prime Directive evaluation must acknowledge active constraints.

---

### 13. Objective

**What it is:** A desired state or outcome that governs current decisions. The target against which alternatives are evaluated.

**Recognition signals in text:**
- Goal-oriented language: "we want to," "the target is," "the goal is," "we are trying to achieve"
- Forward-looking: describes a future state, not a current state
- Governs: other decisions and actions are evaluated against whether they advance this objective

**Distinguished from Constraint:** An Objective is what you are pursuing. A Constraint is what limits how you pursue it. They define the decision space together.

**Example:** "The governing objective for this fiscal year is to reach $10M ARR before raising the Series B."

**Durability:** Medium. Objectives change as circumstances change. Every Objective should carry an expected time horizon.

**Confidence default:** High when explicitly stated by the operator. Lower when inferred.

**Runtime role:** Loads into the Prime Directive evaluation frame. Every output is evaluated against whether it advances the active objective or conflicts with it.

---

### 14. Causal Claim

**What it is:** An assertion that X causes Y, or that X tends to cause Y. A directional relationship between two things. More specific than a Tendency (which observes correlation) — a Causal Claim asserts mechanism.

**Recognition signals in text:**
- Causal language: "caused," "led to," "because," "as a result of," "produced"
- Identifies a mechanism: explains why the relationship holds
- Can be organization-specific or domain-general

**The danger:** Causal Claims are frequently confused with correlations. "Our churn increased when we raised prices" is an Observation. "Raising prices caused our churn to increase" is a Causal Claim — it asserts mechanism, not just sequence. GAQP requires the distinction to be labeled.

**Example:** "The Q2 pricing increase caused SMB churn to rise because our SMB customers have lower switching costs and fewer integration dependencies than enterprise."

**Durability:** Medium. Causal relationships can change as markets, technology, or customer behavior evolves.

**Confidence default:** Medium. Causal Claims require more evidentiary support than Tendencies. Single-instance causation claims should be labeled provisional.

**Runtime role:** Activates during root cause analysis and strategic reasoning. Feeds the Proactive Solutions Architecture when a pattern matches a known causal chain.

---

### 15. Tradeoff

**What it is:** A structured relationship where advancing one objective or value requires giving up another. Not a preference — a genuine structural tension.

**Recognition signals in text:**
- Explicit tension: "to achieve X, we must sacrifice Y"
- Both sides are real values: neither is obviously wrong
- The tension is structural, not just preferential

**Tradeoffs are compositional:** They require at least two other artifacts (usually Objectives or Constraints) to define. You cannot have a Tradeoff without two things in tension.

**Example:** "Increasing deployment velocity reduces time-to-value for customers but increases exposure to undetected defects. This is not a solvable problem — it is a managed tension."

**Durability:** Often medium-term. The underlying tension may be permanent, but its balance point shifts as circumstances change.

**Confidence default:** High when both sides of the tension are clearly established.

**Runtime role:** Surfaces during Prime Directive evaluation as a structural tension requiring explicit acknowledgment. The Prime Directive does not require tradeoffs to be resolved — it requires them to be seen.

---

### 16. Diagnostic Signal

**What it is:** A pattern that reliably indicates an underlying condition — an early warning system. The signal itself may be observable; the underlying condition it indicates may not be directly visible.

**Recognition signals in text:**
- Pattern-indicator language: "when we see X, it usually means Y"
- Predictive: the signal precedes or accompanies the condition
- Actionable: detecting the signal should trigger a specific response

**Distinguished from Tendency:** A Tendency describes what usually happens. A Diagnostic Signal specifically functions as an early warning — it's a Tendency configured as an alert trigger.

**Example:** "When a key enterprise account reduces their active user count by more than 20% over 60 days without an explanation, they are evaluating alternatives. This precedes formal churn by 90–120 days."

**Durability:** Medium. Diagnostic Signals can become obsolete if the relationship between signal and condition changes.

**Confidence default:** Medium. Requires corroboration — a single observed correlation is not sufficient to establish a Diagnostic Signal.

**Runtime role:** Loads into the Proactive Solutions Architecture. When a session's input activates a Diagnostic Signal, PSA surfaces it as a proactive alert before the operator asks.

---

### 17. Assumption

**What it is:** A claim held as true for the purposes of reasoning, but not yet established through evidence. The most dangerous artifact type in governance terms — because Assumptions that are not labeled operate silently as if they were Axioms.

**Recognition signals in text:**
- Embedded premises: claims used in reasoning that are not themselves argued for
- Qualified belief: "we believe," "we expect," "our view is"
- Forward-looking claims presented as current fact
- Predictions dressed as observations

**The governance obligation:** Every Assumption must be labeled. An unlabeled Assumption inside a reasoning chain is a governance failure — it means the reasoning appears more certain than it is.

**Example (unlabeled):** "The market will consolidate in 18 months, so we should hold off on the acquisition." ← the consolidation claim is an Assumption masquerading as a fact.

**Example (correctly labeled):** "Assuming the market consolidates within 18 months [confidence: medium, source: CEO projection], the acquisition should be deferred."

**Durability:** Variable. Assumptions should be reviewed at defined intervals — and upgraded to established claims if corroborated, or revised downward if contradicted.

**Confidence default:** Low to medium by definition. An Assumption that has high confidence should be re-evaluated as a Best Practice, Tendency, or established Causal Claim.

**Runtime role:** Surfaces in the Prime Directive evaluation. Any recommendation that rests on an Assumption must disclose that Assumption explicitly. The Recursive Reintegration check verifies that Assumptions are labeled and not buried.

---

## Part IV: The Decision Artifacts — The Feedback Loop Family

These artifacts are unique to Execalc's architecture. They close the loop between decision and outcome — and are the mechanism through which the system becomes empirically smarter over time.

---

### 18. Decision Outcome

**What it is:** The composite artifact that connects a prior governed decision to its result, with a retrospective Prime Directive evaluation. The Decision Outcome closes the loop that most organizations never close.

**Structure:**

```
Decision Outcome
    ├── Reference: [original Decision Artifact ID]
    ├── Result: [what actually happened]
    ├── Retrospective PD Evaluation:
    │     ├── Value: Did this deliver value or clarity as predicted?
    │     ├── Risk/Reward: Was the risk/reward assessment accurate?
    │     ├── Assets/Liabilities: Did the balance sheet position play out as expected?
    │     └── Supply/Demand: Did the structural read hold?
    ├── Delta: [gap between prospective prediction and actual outcome]
    ├── Heuristics Applied: [which EKE corpus entries governed the decision]
    ├── Heuristic Validation: [did the outcome validate or challenge each applied heuristic?]
    └── Learning: [what governing logic should be updated as a result?]
```

**Why this is the most important artifact in the system:**

Every governed decision is a prediction. The Prime Directive evaluation at decision time predicts: "this will deliver value." The Decision Outcome answers whether that prediction was accurate.

Over time, the accumulation of Decision Outcomes creates an empirical track record:
- Which heuristics produced good outcomes in which scenarios
- Which Prime Directive evaluations were systematically miscalibrated
- Which assumptions were reliably wrong
- Which Tendencies held empirically in this organization's specific context

**The compounding value:** By Year 3, an organization operating with Execalc is not just using received wisdom from Sun Tzu, Voss, and Drucker. It is using that wisdom *calibrated against its own three-year empirical track record.* No competitor can replicate that. No consulting firm has it. It is institutional intelligence that cannot be purchased.

**Recognition:** Decision Outcomes are not extracted from text in the same way other artifacts are. They are generated by the system when:
- A prior Decision Artifact is retrieved
- A result has been observed that connects to it
- The operator records the result (or the system detects it through connected integrations)

**Durability:** Permanent as a historical record. Increasing in value over time as the corpus of Decision Outcomes grows.

**Confidence default:** Tied to the quality of the Result measurement.

**Runtime role:** Activates when the current scenario resembles a scenario that produced a Decision Outcome. PSA surfaces relevant Decision Outcomes as institutional precedent before the operator is asked to decide.

---

### 19. Communication Stance

**What it is:** A posture or register that governs how output is delivered in a specific context. Governs tone and framing — not analytical substance. A Communication Stance must never enter the judgment chain; it operates only at the output layer.

**Recognition signals in text:**
- Tone-defining: "in high-stakes situations, be direct"
- Delivery-oriented: about how to say something, not what to say
- Context-sensitive: different contexts call for different stances

**The critical boundary:** A Communication Stance should never influence the substance of an analysis. "Adopt a collaborative posture when delivering difficult findings" is a Communication Stance. If it causes the system to soften or omit a difficult finding, it has crossed into the judgment chain — which is a governance violation.

**Example:** "When delivering a recommendation that contradicts the operator's stated preference, lead with acknowledgment of the preference before presenting the divergent finding." (Voss — tactical empathy posture)

**Runtime role:** Output layer only. Loaded into the context package in the communication layer, not the analysis layer. Audit trail must confirm it did not alter analytical conclusions.

---

## Part V: The Canonical Artifact Map

### Complete Taxonomy (19 types, organized by family)

**Family A: Pattern Artifacts (Durable Knowledge — EKE corpus)**

| # | Type | Core Question | Expires? |
|---|---|---|---|
| 1 | Axiom | What is foundational? | Rarely |
| 2 | Principle | What is the broad rule? | Rarely |
| 3 | Tendency | What usually happens? | Slowly |
| 4 | Heuristic | What to do when? | Medium |
| 5 | Mental Model | How does the system work? | Rarely |
| 6 | Stratagem | What sequence wins? | Medium |
| 7 | Definition | What does this term mean here? | With context |
| 8 | Best Practice | What has been proven to work? | Medium |

**Family B: Situated Intelligence (Tenant-Scoped Memory)**

| # | Type | Core Question | Expires? |
|---|---|---|---|
| 9 | Observation | What was directly perceived? | Medium |
| 10 | Event | What happened, when? | Historical |
| 11 | Result | What was the outcome? | Historical |
| 12 | Constraint | What limits our options? | With condition |
| 13 | Objective | What are we trying to achieve? | With cycle |
| 14 | Causal Claim | What causes what here? | Medium |
| 15 | Tradeoff | What must we give up to gain X? | With context |
| 16 | Diagnostic Signal | What pattern means what? | Medium |
| 17 | Assumption | What are we treating as true? | Review required |

**Family C: Decision Artifacts (The Feedback Loop)**

| # | Type | Core Question | Expires? |
|---|---|---|---|
| 18 | Decision Outcome | Did the decision deliver value? | Never |
| 19 | Communication Stance | How should this be delivered? | With context |

---

### The Extraction Priority Order

When scanning text, extract in this priority sequence:

1. **Assumptions first** — the highest governance risk; they hide inside reasoning as if they were facts
2. **Constraints and Objectives** — define the decision space; everything else is evaluated against them
3. **Results and Decision Outcomes** — close the feedback loop; highest learning value
4. **Heuristics and Stratagems** — action rules; directly influence what gets recommended
5. **Diagnostic Signals** — early warning patterns; feed the Proactive Solutions Architecture
6. **Causal Claims** — mechanism assertions; require careful confidence labeling
7. **Principles and Axioms** — foundational; add to EKE corpus if not already present
8. **Tendencies** — directional patterns; validate or calibrate against Results over time
9. **Mental Models** — reasoning scaffolds; high durability, lower urgency
10. **Observations and Events** — raw input; capture but do not conflate with interpretations

---

## Design Principle

> The recognition standard is the foundation of governed intelligence. A system that cannot reliably identify what kind of artifact it is looking at will misclassify, misactivate, and eventually produce plausible-sounding outputs that violate the governing logic. The taxonomy is not bureaucracy — it is the difference between a system that accumulates wisdom and a system that accumulates noise.

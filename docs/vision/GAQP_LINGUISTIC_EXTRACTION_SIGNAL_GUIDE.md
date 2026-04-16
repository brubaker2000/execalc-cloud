# GAQP_LINGUISTIC_EXTRACTION_SIGNAL_GUIDE.md

## Status
Draft v0.1

## Owner
GAQP / Architecture

## Position in GAQP
This is the operational extraction guide — the practical signal reference for identifying candidate artifacts in text by their linguistic patterns. It sits below the recognition standard (GAQP_ARTIFACT_RECOGNITION_AND_EXTRACTION_STANDARD.md) and is intended for direct use by extraction layer implementations, human annotators, and LLM-assisted parsing.

---

## Purpose

The GAQP Artifact Recognition and Extraction Standard defines the 19 artifact types and the criteria for harvest-worthiness. It answers the question: *what is an artifact?*

This document answers the operational question: *how do you find one?*

Artifacts do not announce themselves. They appear inside paragraphs alongside noise, context, and transition language. The extraction layer — human or machine — needs a consistent method for identifying candidates before classification and admission can proceed.

That method is linguistic signal recognition: the systematic identification of phrase patterns and sentence structures that correlate with specific artifact types.

---

## How to Use This Guide

For each piece of text being evaluated:

1. Scan for the phrase families in Section 1 (Extraction Signal Families)
2. When a pattern fires, identify the candidate sentence or clause
3. Check whether the candidate meets harvest-worthiness criteria (from the Recognition Standard)
4. If harvest-worthy, proceed to classification using the Signal-to-Type Mapping in Section 2
5. If the candidate contains multiple signals, decompose before classifying

Do not classify based on a single word alone. A signal phrase is a trigger for examination, not a guarantee of artifact status.

---

## Section 1: Extraction Signal Families

These are the six phrase families that cover the majority of extractable artifacts. Each family is associated with one or more artifact types.

---

### Family 1: Truth Language

**What it signals:** Foundational claims, principles, definitions. Statements presented as durable, broadly applicable reality.

**Key phrases and structures:**

- "fundamentally..."
- "the truth is..."
- "in reality..."
- "it is always the case that..."
- "by definition..."
- "is defined as..."
- "means..."
- "refers to..."
- "we call this..."
- "at its core..."
- "the underlying principle is..."
- "what this actually is..."
- "[X] is [Y]" — naming or definitional sentences

**Associated artifact types:** Axiom, Principle, Definition, Mental Model

**Caution:** Not every "is" sentence is an artifact. "The sky is blue" contains truth language but is not harvest-worthy. The content must satisfy the harvest-worthiness criteria. Look for "is" sentences that assert a non-obvious structural reality about how a system, market, or domain behaves.

---

### Family 2: Rule Language

**What it signals:** Prescriptive action rules. What to do, what not to do, what must happen first. Decision guidance under defined conditions.

**Key phrases and structures:**

- "when [X], [do Y]"
- "if [X], then [Y]"
- "always [do X]"
- "never [do X]"
- "before you [do X]..."
- "must not..."
- "may not..."
- "only if..."
- "the right move is..."
- "best practice is to..."
- "start by..."
- "do not [X] until..."
- "rule of thumb..."
- "a good proxy is..."

**Associated artifact types:** Heuristic, Best Practice, Constraint, Stratagem (when a sequence is implied)

**Distinction:** If the rule implies a single response, it is a Heuristic or Best Practice candidate. If the rule implies a sequence of moves with a positional goal, it is a Stratagem candidate. If the rule narrows the decision space rather than directing action, it is a Constraint.

---

### Family 3: Probability Language

**What it signals:** Tendencies and observations. Directional patterns that hold more often than not. What usually happens, not what always happens.

**Key phrases and structures:**

- "tends to..."
- "often..."
- "usually..."
- "more often than not..."
- "is prone to..."
- "systematically [overreacts/underreacts]..."
- "in most cases..."
- "directionally..."
- "appears to..."
- "we're seeing..."
- "I notice..."
- "the pattern seems to be..."
- "historically..."

**Associated artifact types:** Tendency, Observation, Diagnostic Signal

**Distinction:** Tendency is a durable, cross-context pattern. Observation is a specific, situated instance. If the statement describes what has been observed in a specific context (with a specific actor, time, or organization), it is an Observation. If it describes a general pattern that holds across contexts, it is a Tendency.

---

### Family 4: Goal Language

**What it signals:** Objectives. Target states, desired outcomes, intent declarations.

**Key phrases and structures:**

- "the goal is..."
- "we want to..."
- "our objective is..."
- "success looks like..."
- "we're trying to..."
- "the aim is..."
- "what we're optimizing for..."
- "intended to..."
- "so that [X] can happen..."
- "in order to..."

**Associated artifact types:** Objective

**Caution:** Not every statement of desire is an Objective artifact. The Objective must be specific enough to govern decisions. "We want to grow" is too vague. "We want to reach 25% gross margin before raising our next round" has enough specificity to activate constraints and tradeoffs.

---

### Family 5: Causal Language

**What it signals:** Causal claims and tradeoffs. Statements that assert mechanism — that X drives Y, or that gaining X requires sacrificing Y.

**Key phrases and structures:**

*Causal:*
- "because..."
- "leads to..."
- "drives..."
- "results in..."
- "creates..."
- "causes..."
- "therefore..."
- "which means..."
- "produces..."
- "the reason [X] is..."

*Tradeoff:*
- "but at the cost of..."
- "in exchange for..."
- "however..."
- "on the other hand..."
- "versus..."
- "you cannot have [X] without [Y]..."
- "sacrifices..."
- "trades [X] for [Y]"
- "the downside of [X] is..."

**Associated artifact types:** Causal Claim, Tradeoff

**Distinction:** A Causal Claim asserts direction without necessarily quantifying the gain and cost. A Tradeoff explicitly names what is given up to obtain something. If both the gain and the loss are stated, it is a Tradeoff. If only the driver and outcome are stated, it is a Causal Claim.

---

### Family 6: Time-Anchor Language

**What it signals:** Events. Completed, time-bounded occurrences with strategic significance.

**Key phrases and structures:**

- "on [date]..."
- "in [Q/month/year]..."
- "last [week/quarter/year]..."
- "announced..."
- "closed..."
- "launched..."
- "raised..."
- "acquired..."
- "signed..."
- "then..."
- "[organization] [past-tense verb]..."
- "at the time of..."

**Associated artifact types:** Event, Result (when outcome-bearing)

**Distinction:** An Event is a completed occurrence. A Result is an Event that records the outcome of a prior decision or action. If the sentence describes what happened in consequence of a prior decision, it is a Result candidate. If it describes an independent occurrence, it is an Event candidate.

---

## Section 2: Signal-to-Type Mapping

Quick reference for classification after a candidate has been identified.

| Signal Family | Primary Candidate Type | Check For |
|---|---|---|
| Truth Language + universal scope | Axiom | Non-arguable foundation; used as premise, not conclusion |
| Truth Language + behavioral scope | Principle | Arguable; governs approach across many contexts |
| Truth Language + definitional structure | Definition | Names or scopes a term for operational use |
| Truth Language + mechanism explanation | Mental Model | Explains how a system works; contains causal structure |
| Rule Language + single action | Heuristic | One-move decision rule; bounded; fast-activating |
| Rule Language + documented outcomes | Best Practice | Heuristic with empirical validation |
| Rule Language + sequence of moves | Stratagem | Multi-move; positional goal; conditions stated |
| Rule Language + narrowing | Constraint | Limits decision space; does not direct action |
| Probability Language + durable/cross-context | Tendency | Pattern that generalizes; requires confidence rating |
| Probability Language + specific/situated | Observation | What was directly perceived; does not yet generalize |
| Probability Language + predictive indicator | Diagnostic Signal | Weak signal that something may be true; not yet a claim |
| Goal Language + decision-governing | Objective | Target state specific enough to activate constraints |
| Causal Language + mechanism | Causal Claim | X drives Y; applies in this context |
| Causal Language + gain/loss pair | Tradeoff | Named exchange; both sides explicitly stated |
| Time-Anchor Language + strategic occurrence | Event | Completed, dated, bounded |
| Time-Anchor Language + outcome of prior decision | Result | Closes a decision feedback loop |

---

## Section 3: Compound Signal Detection

Many sentences contain multiple signal families simultaneously. These require careful decomposition before classification.

### Compound pattern: Tendency + Causal Claim

> "Incumbents tend to underreact to disruptive entrants, because their incentive structures reward defending the core."

Two artifacts:
- **Tendency:** "Incumbents tend to underreact to disruptive entrants."
- **Causal Claim:** "Incumbents' incentive structures reward defending the core, causing underreaction to disruptors."

These are separate governed claims. Admitting them as one fuses an empirical pattern with a causal mechanism, which cannot be independently corroborated or challenged.

---

### Compound pattern: Objective + Constraint

> "We want to close this by Q3, but we cannot proceed without board approval."

Two artifacts:
- **Objective:** "Close by Q3."
- **Constraint:** "Board approval is required to proceed."

Again, separate. The constraint governs the achievability of the objective; they should be linked, not merged.

---

### Compound pattern: Heuristic + Tradeoff

> "Always confirm authority before beginning a negotiation — even if it slows the process."

Two artifacts:
- **Heuristic:** "Confirm authority before beginning a negotiation."
- **Tradeoff:** "Confirming authority slows the process; the tradeoff is process speed for negotiation validity."

---

### Rule: One claim per governed artifact

The admission pipeline handles single claims, not compound statements. If a sentence contains more than one artifact, it must be decomposed before either can be admitted. Admitting a compound statement as a single artifact produces a claim that cannot be cleanly corroborated, challenged, or composed.

---

## Section 4: Signals That Do Not Indicate Artifacts

Some phrase patterns look like artifact signals but are not. They require extra scrutiny before a candidate is elevated.

| Pattern | Risk | Resolution |
|---|---|---|
| Hedged opinions: "I think maybe..." | Fails disputability; fails stand-alone | Extract only if the claim beneath the hedge is concrete |
| Rhetorical questions: "But is this really...?" | Not a claim | May indicate an Assumption or Diagnostic Signal beneath the question |
| Pure analogies: "This is like..." | Not a claim; illustrative language | Look for the claim the analogy is supporting |
| Intensifiers without content: "It's really important that..." | Not a claim | Look at what follows the intensifier |
| Attribution without claim: "[Person] said..." | Not yet an artifact | What they said must be extracted as the artifact |
| Transition phrases: "Building on that..." | Not a claim | Skip; look at what follows |
| Slogans: "Move fast and break things" | Too compressed; often non-disputable without unpacking | Unpack the governing claim before admitting |

---

## Section 5: The Assumption Detection Protocol

Assumptions are the highest-priority artifact type under the extraction priority order (see Recognition Standard). They are also the hardest to detect, because they appear as facts inside reasoning — not as claims being made.

### How assumptions hide

Assumptions are not signaled by their own phrase family. They hide inside other families:

- Inside Causal Claims: "Because X always happens, Y follows." (Is X actually established?)
- Inside Objectives: "We want to double revenue." (Is doubling feasible given constraints? What assumes it is?)
- Inside Tendencies: "Markets tend to correct." (In what timeframe? Under what conditions?)
- Inside Heuristics: "When the buyer goes silent, wait." (Assumes the silence means what you think it means.)

### Detection questions

When reading any artifact candidate, ask:

1. What would have to be true for this to be correct?
2. Is that prerequisite itself established, or is it assumed?
3. If a skeptic pushed back on this, where would the first unestablished step be?

Any unestablished prerequisite that is load-bearing — meaning the artifact is false or inapplicable if the prerequisite is wrong — is an Assumption candidate.

### Assumption extraction format

> "This analysis assumes [prerequisite claim], which has not been established. If [prerequisite] is false, [consequence for the reasoning it supports]."

An assumption, once extracted, should immediately be linked to the artifact it supports and flagged for review.

---

## Section 6: Quick-Reference Extraction Checklist

When reading any document or conversation for artifacts:

- [ ] Scan for Truth Language → Axiom, Principle, Definition, Mental Model candidates
- [ ] Scan for Rule Language → Heuristic, Best Practice, Constraint, Stratagem candidates
- [ ] Scan for Probability Language → Tendency, Observation, Diagnostic Signal candidates
- [ ] Scan for Goal Language → Objective candidates
- [ ] Scan for Causal Language → Causal Claim, Tradeoff candidates
- [ ] Scan for Time-Anchor Language → Event, Result candidates
- [ ] Apply Assumption Detection Protocol to every causal chain and objective
- [ ] Decompose any compound-signal sentences before classifying
- [ ] Apply harvest-worthiness criteria to each candidate
- [ ] Apply seven-test admission filter to each admitted candidate

---

## Design Principle

> Signal families identify candidates. The admission tests govern what enters the system. Neither step should be skipped or conflated with the other. An extraction layer that also evaluates for admission will systematically under-extract. An admission layer that also classifies will systematically misclassify. The three operations — extraction, classification, admission — are sequential by doctrine.

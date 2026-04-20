# GAQP — Generally Accepted Qualitative Principles
## Founding Charter — v1.0

**Issued by:** Players Capital Group / Execalc  
**Status:** Founding declaration — open standard  

---

## Preamble

For centuries, the problem of qualitative reasoning has resisted standardization.

Numbers submitted to standard treatment. GAAP gave financial information a shared language — a classification system, a set of deliberative rules, and an output format that made financial statements legible, comparable, and trustworthy across organizations, jurisdictions, and time.

No equivalent standard exists for meaning.

Qualitative analysis — the synthesis of language, judgment, and structured reasoning — is performed privately, manually, and inconsistently. The best consulting firms do it well. McKinsey and BCG apply rigorous qualitative discipline internally. But that discipline lives in culture, training, and proprietary process — not in a portable, explicit standard. No one has published the methodology. No one has defined the unit. No one has created the decoding system that would allow one actor's extracted insight to be read, categorized, and reasoned with by another.

The arrival of large language models has made this gap consequential. LLMs perform qualitative synthesis by definition — they take language in and produce synthesized meaning out. But the synthesis is ungoverned: there is no standard for what enters the process, no standard for the deliberative unit being reasoned with, and no standard for what the output claims to be. The result is computation that resembles judgment without being accountable to any of judgment's requirements.

GAQP is the standard that fills this gap.

---

## Standard, Not Compliance

GAQP is a **standard**. It is not a compliance framework.

GAAP is compliance — public companies must follow it or their financials are invalid. That is a regulatory posture enforced by law.

GAQP is infrastructure — a shared decoding system that makes qualitative units legible, comparable, and composable across any system or actor that adopts it. No regulator requires it. No law mandates it. Its value is interoperability: if two systems both operate under GAQP, a deliberative unit produced by one is readable by the other without re-derivation.

The closest analogies are not accounting standards. They are:

- **Musical notation** — a standard that lets any musician read any composer's work across centuries and cultures without re-translating
- **The periodic table** — a classification system that makes elements legible across all of chemistry regardless of who is doing the experiment
- **HTML** — an open standard that created the web; the authors benefited from being first and from authorship, not from locking anyone out

GAQP is the periodic table for qualitative reasoning units.

---

## The Philosophical Foundation

We do not believe there is artificial intelligence. We believe there is the clever application of brute force computational power.

A large language model does not understand the Gettysburg Address. It has processed enough language to predict, at extraordinary resolution, what tokens follow other tokens. That is not intelligence. It is pattern-matching at a scale no human can match manually.

This matters because it clarifies where the value actually lives. It is not in the model. It is in the governed structure built above the model — the architecture that determines what enters the reasoning process, how it is classified, what rules govern the deliberation, and what the output is required to demonstrate.

The number 100 has factors: 4, 5, 10, 20, 25, 50. Those factors are objectively present in the number whether anyone extracts them or not. The methodology of factorization is what makes them usable.

The Gettysburg Address has its own factors: claims, principles, causal assertions, observations, implicit assumptions, explicit commitments. Those factors are objectively present in the text whether anyone extracts them or not. Most language processing treats the text as a whole and predicts responses to it. No one has built the factorization methodology for language.

GAQP is that methodology. The extracted factor is the atomic nugget. The system that performs the extraction and governs the reasoning is the operating system built on GAQP.

---

## What GAQP Defines

GAQP standardizes three layers of qualitative synthesis. All three are required for the standard to hold.

---

### Layer 1 — The Deliberative Unit

The atomic unit of governed qualitative reasoning is the **nugget** — a governed claim extracted from language that has passed admission criteria and been classified.

A nugget is not a sentence. It is not a summary. It is not a quote. It is the smallest durable unit of qualitative reasoning that can stand alone, be categorized, be attributed, and be composed with other nuggets to form higher-order conclusions.

**The boundary definition — this is a deliberative unit; that is not:**

A deliberative unit must satisfy all six admission criteria:

1. **Stand-alone** — It can be understood without its surrounding conversation or document.
2. **Disputable** — It can be challenged. A pure truism fails this test. What cannot be argued cannot be reasoned with.
3. **Governed** — It falls within a recognized claim type from the GAQP taxonomy.
4. **Activating** — There exists a scenario in which this claim would change a decision.
5. **Durable** — It is likely to remain relevant beyond its originating context.
6. **Composable** — It can combine with other nuggets to form higher-order reasoning.

A sentence that fails any one of these six tests is not a deliberative unit under GAQP. It may be language. It may be useful context. It is not a governed claim.

---

### Layer 2 — The Classification System

Every admitted nugget must be classified. Classification is the decoding key — what makes a nugget readable by any GAQP-compliant system or actor without re-deriving it from the source material.

**GAQP Claim Type Taxonomy — v1.0**

| Claim Type | Definition |
|---|---|
| **Axiom** | A foundational principle treated as self-evident within a domain; not derived from other claims |
| **Definition** | A statement that establishes the meaning of a term within a governed context |
| **Principle** | A governing rule that applies across multiple situations within a domain |
| **Heuristic** | A reliable but non-universal shortcut derived from experience |
| **Best Practice** | A consistently effective approach within a defined context |
| **Tendency** | A pattern that holds directionally but not universally |
| **Observation** | A factual record of something witnessed or measured, without interpretation |
| **Event** | A discrete occurrence with a defined time, actor, or outcome |
| **Constraint** | A boundary condition that limits the solution space |
| **Objective** | A declared desired outcome with a defined scope |
| **Tradeoff** | A claim that two desirable outcomes cannot be simultaneously maximized |
| **Causal Claim** | An assertion that one condition produces or influences another |
| **Diagnostic Signal** | A pattern that reliably indicates an underlying condition |

A nugget that does not fit any recognized claim type is not GAQP-classified. It may be admitted as a candidate pending taxonomy extension, but it does not carry the weight of a governed claim until classified.

The taxonomy is versioned. New claim types may be added through the governed amendment process defined below.

---

### Layer 3 — The Metadata Schema

Every classified nugget must carry metadata that preserves its interpretability across contexts, systems, and time. Without metadata, a nugget is an orphaned claim — possibly true, but unanchored.

**Required metadata fields — GAQP v1.0:**

| Field | Description |
|---|---|
| `claim_type` | From the GAQP taxonomy above |
| `source` | The originating document, conversation, or actor |
| `source_kind` | Original observation / derived interpretation / operator assertion / external attribution |
| `confidence` | high / medium / low / unknown — with explicit basis |
| `scope` | The domain or context within which the claim holds |
| `time_horizon` | Immediate / short-term / long-term / permanent |
| `activation_state` | Active (eligible to influence reasoning) / Dormant (stored; does not trigger reasoning) |
| `sensitivity` | Public / internal / confidential / restricted |
| `provenance` | The admission path — extraction event, admission gate, timestamp |
| `corroboration` | Independent claims that confirm this claim, if any |
| `conflicts` | Claims that contradict this claim, if any |

A nugget without required metadata fields is not GAQP-compliant, regardless of how well it satisfies the admission criteria.

---

## The Separation Principle

GAQP enforces a structural separation that most qualitative analysis violates:

> **Observation and interpretation must be stored and labeled separately.**

What was directly witnessed or measured is categorically different from what was concluded from it. Conflating the two is the most common failure mode in qualitative reasoning — a conclusion presented as a fact, an interpretation presented as an observation.

*"The CFO expressed concern about margins"* is an observation.  
*"The company is facing a profitability crisis"* is an interpretation.

GAQP-compliant systems maintain this separation as a structural requirement, not a stylistic preference. The `source_kind` field encodes it at the metadata level.

---

## The Ten Governing Principles

GAQP compliance is governed by ten principles. These principles are not rules about what systems must do — they are the standards against which qualitative reasoning is evaluated.

**1. Materiality**  
Only signal that changes what a decision-maker would rationally do is worth capturing. Not all language contains signal. GAQP-governed systems filter for claims that would materially affect a decision.

**2. Traceability**  
Every claim must trace back to its source, context, and admission path. A claim without provenance is not GAQP-compliant.

**3. Authenticity**  
Claims must reflect what was actually observed, not what was hoped. The system must preserve the difference between what was said and what was wanted to hear.

**4. Context**  
No claim is fully interpretable without its originating context. GAQP-compliant storage must preserve enough context to make the claim interpretable without access to the original document.

**5. Separation of Observation and Interpretation**  
Raw observation and derived interpretation must be stored and labeled separately. Conflation is a compliance failure.

**6. Corroboration**  
Claims gain weight through independent confirmation. Single-source claims carry lower confidence. GAQP-compliant systems track corroboration and assign confidence accordingly.

**7. Explicit Assumptions**  
Assumptions embedded in claims must be named, not hidden. Every analytical claim rests on assumptions; GAQP requires those assumptions to be surfaced and tagged.

**8. Revision**  
Claims must support structured revision with lineage preserved. Revision is not deletion. When a claim is updated, the prior version is retained with a notation of what changed and why.

**9. Governed Memory Admission**  
Not all claims are admitted to active reasoning. Capture and admission are separate acts. Admission requires passing an explicit evaluation against the six-test filter.

**10. Reconstructable Decision Lineage**  
Any decision output must be reconstructable from its admitted claims, applied frameworks, and governing logic. A GAQP-compliant decision can be audited end-to-end.

---

## What GAQP Does Not Govern

GAQP governs the extraction, classification, and metadata of deliberative units. It does not:

- Prescribe what reasoning must conclude
- Mandate which frameworks are applied to which situations
- Require a specific output format for decisions or recommendations
- Define what tools or systems perform the extraction

GAQP is a standard for the units of qualitative reasoning, not a system for performing it. Any compliant system may use its own architecture for the reasoning layer, provided the deliberative units it produces or consumes meet the standard.

---

## The Open Standard Declaration

GAQP is a public standard.

The taxonomy, admission criteria, metadata schema, separation principle, and ten governing principles defined in this charter are available to any individual, organization, or system that wishes to adopt them. No license is required. No permission is needed.

A GAQP-compliant system is any system that:
1. Applies the six-test admission filter before treating a claim as a deliberative unit
2. Classifies admitted claims using the GAQP taxonomy
3. Attaches required metadata to classified claims
4. Maintains the separation of observation and interpretation

The standard is versioned. Execalc maintains version history and publishes amendments.

---

## The Invitation

The market for governed qualitative synthesis does not yet exist as a recognized category. GAQP's purpose is to create it.

We invite competition.

Every organization that builds a GAQP-compliant system grows the market for governed qualitative synthesis. Every system that adopts the taxonomy makes the standard more entrenched. Every competitor that demonstrates GAQP compliance validates the framework that Execalc originated.

The moat is not exclusion. The moat is authorship.

Execalc is the first operating system built on GAQP — the reference implementation that demonstrates what governed qualitative synthesis looks like when the standard is applied end-to-end. Other systems that adopt the standard will serve the market that Execalc defines. That is not a threat. That is the plan.

---

## Versioning and Amendment

GAQP is a living standard. v1.0 defines the minimum viable framework.

Future versions will address:
- **Composition rules** — how nuggets combine into higher-order reasoning structures
- **Confidence calibration standards** — what "high confidence" means operationally
- **Attribution standards** — how thinker-sourced claims are attributed and weighted
- **Cross-system interoperability** — how GAQP-classified nuggets are exchanged between compliant systems
- **Audit standards** — how GAQP compliance is verified externally

Amendments require:
1. A documented case for the addition or change
2. A review period during which objections may be submitted
3. Publication of the versioned amendment with change rationale

No amendment may remove or weaken the six-test admission filter, the separation principle, or the required metadata fields without a superseding version declaration.

---

## Relationship to Execalc

Execalc does not own GAQP. It authors it. The distinction matters.

An owner controls access. An author advances the standard. Execalc's obligation is to maintain the integrity of the standard, publish amendments transparently, and build the reference implementation that demonstrates its value.

Every core Execalc capability maps to one or more GAQP principles:

| Execalc Capability | GAQP Layer / Principle |
|---|---|
| Governed claim admission | Layer 1 — Deliberative Unit / Materiality |
| Six-test admission filter | Layer 1 — Boundary Definition |
| Claim type taxonomy | Layer 2 — Classification |
| Provenance metadata | Layer 3 — Metadata / Traceability |
| Observation vs. interpretation labeling | Separation Principle |
| Corroboration tracking | Principle 6 — Corroboration |
| Assumption tagging | Principle 7 — Explicit Assumptions |
| Revision with lineage | Principle 8 — Revision |
| Memory promotion ladder | Principle 9 — Governed Memory Admission |
| Decision artifacts | Principle 10 — Reconstructable Decision Lineage |

---

## Founding Statement

> The number 100 has factors. The Gettysburg Address has factors too.  
> GAQP is the methodology for finding them.  
> Execalc is the first system built to use them.

GAQP will do for qualitative reasoning what GAAP did for financial reporting: create a shared, portable, explicit discipline that makes qualitative claims comparable, auditable, and trustworthy across organizations, time periods, and decision contexts.

The absence of GAQP has been invisible to most organizations because they have never had an alternative. Once the standard exists, the absence becomes legible — and the competitive advantage of operating under it becomes clear.

Players Capital Group is why this standard exists.  
Executive Calculus is how it is enforced.  
The market it creates belongs to everyone who builds on it.

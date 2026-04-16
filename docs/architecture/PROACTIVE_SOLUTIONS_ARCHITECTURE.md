# PROACTIVE_SOLUTIONS_ARCHITECTURE.md

## Status
Draft v0.2 — Expanded with execution design mode, cartridge connection, MDL handshake, and Recursive Analysis pairing

## Owner
Architecture / Core 7

## Position in Core 7
Framework 6 — Activates after the context package is assembled and the Judgment Call is underway. Immediately precedes Recursive Analysis (Framework 7), which audits the pathways PSA generates.

---

## Canonical Definition

Proactive Solutions Architecture is Execalc's governed forward-motion framework. It takes governed judgment and converts it into two things the operator needs: what they haven't asked about yet, and how to move on what they have decided.

PSA answers two questions:

> **What does the operator need to know that they have not yet asked about?**

> **Given a decision, what is the governed execution map — the pathways, owners, dependencies, and unlocks — that moves it into action?**

---

## Why This Exists

Most systems stop at analysis. PSA exists because analysis without motion is unfinished work.

An operator submits a query. A system that answers only within the stated scope is a sophisticated search tool. A governed judgment system carries obligations beyond the stated question — the governing frameworks frequently surface implications the operator has not named, and once a decision is reached, the work of designing how to execute it is as important as the work of reaching it.

PSA is what prevents Execalc from being a reflective intelligence only. It is the layer that asks not just "what is true?" but "what should move next, in what order, with what dependencies, and before what risk metastasizes?"

---

## The Two Operational Modes

PSA operates in two distinct modes that address different phases of the decision cycle:

**Mode 1 — Detection and Surfacing**
Scans for implications beyond the stated question. Surfaces material signals the operator has not asked about. Fires during every judgment cycle.

**Mode 2 — Execution Design**
Converts governed judgment into structured execution pathways. Fires when a decision has been reached and the next question is how to move on it.

Mode 1 is about what the operator needs to know before or alongside the recommendation. Mode 2 is about what happens after the decision. Together they prevent the two most common failure modes: acting on incomplete information, and failing to act on complete information.

---

## Mode 1: Detection and Surfacing

### Stage 1: Implication Scan

After the context package is assembled — compliance constraints, Carats, scenario logic, reflexes, corpus entries, operator memory — PSA scans for implications that extend beyond the stated question.

| Implication Type | Description |
|---|---|
| **Latent risk** | Evidence implies a risk the operator has not named |
| **Emerging opportunity** | Signal pattern suggests a window that will not persist |
| **Assumption conflict** | Operator's framing rests on an assumption the corpus or memory contradicts |
| **Decision dependency** | The stated question cannot be answered correctly without resolving a prior unaddressed question |
| **Temporal urgency** | Evidence implies a time constraint the operator has not acknowledged |

---

### Stage 2: Materiality Gate

Not every implication warrants surfacing. PSA applies the GAQP Materiality principle: **only signal that changes what a decision-maker would rationally do is worth surfacing.**

Materiality test for each detected implication:

1. Would a fully informed senior advisor mention this before answering the stated question?
2. If acted on, would this implication materially change the recommended action?
3. Does the implication affect a Prime Directive lens the stated question did not evaluate?

Implications that fail the materiality test are logged but not surfaced.

---

### Stage 3: Proactive Signal Assembly

Implications that pass the materiality gate are assembled into a structured proactive signal set:

```json
{
  "proactive_signals": [
    {
      "type": "latent_risk",
      "description": "Cash runway under current burn implies 4.2 months before the proposed competitive response becomes financially untenable.",
      "evidence_source": ["MEM-0042 (admitted Q3 burn rate)", "HTL-0123 (Taleb: fragility threshold)"],
      "prime_directive_lens": "risk_reward",
      "materiality": "high",
      "recommended_disclosure": "Surface before recommendation"
    },
    {
      "type": "decision_dependency",
      "description": "The proposed response assumes pricing authority. Operator memory does not confirm this authority is uncontested.",
      "evidence_source": ["MEM-0031 (CFO approval required for price moves >15%)"],
      "prime_directive_lens": "assets_liabilities",
      "materiality": "medium",
      "recommended_disclosure": "Surface as qualifying condition"
    }
  ],
  "total_signals": 2,
  "suppressed_signals": 1
}
```

---

### Stage 4: Judgment Call Integration

The proactive signal set is passed to the Judgment Call alongside the operator's stated question:

```
[GOVERNING OBSERVATION — surfaces before recommendation if materiality = high]
Before addressing your question, one item demands attention: [signal description]

[RECOMMENDATION]
Given the above, the recommended course of action is...

[QUALIFYING CONDITIONS]
This recommendation assumes: [list of decision dependencies and medium-materiality signals]
```

---

### Proactive Signal Persistence and Governance Gaps

A proactive signal that is surfaced but not resolved becomes a **pending implication** — it follows the operator into the next session.

If the operator resolves the signal (acts on it, or explicitly acknowledges it and chooses not to act), the resolution is admitted to memory as a governed decision artifact.

If the operator does not address it, it re-surfaces in the next relevant session at higher priority weight.

A signal surfaced **three times without resolution** is flagged as a **governance gap**:

```
[GOVERNANCE GAP — Third Instance]
This implication has been surfaced in three sessions without resolution.
It may represent a decision the organization has been deferring.
```

---

### PSA vs. The Reflex System

| Component | When | What |
|---|---|---|
| Reflex System (Stage 3, Activation Pathway) | Before the Judgment Call | Pre-loads known response patterns for the detected scenario type |
| PSA Mode 1 (Core 7, F6) | During Judgment Call reasoning | Surfaces implications from specific evidence that the stated question did not address |

Reflexes are pre-encoded patterns: "when you see Scenario 7 (Negotiation), always assess BATNA." PSA is inference from evidence: "given what the memory and corpus jointly imply about this operator's situation, there is a risk that has not been named."

Reflexes are scenario-class responses. PSA Mode 1 is situation-specific inference.

---

## Mode 2: Execution Design

### What It Does

Once a decision has been reached, the next question is how to execute it. PSA Mode 2 takes governed judgment and converts it into structured execution pathways — multiple viable routes with time horizon, risk profile, monetization angle, resource requirements, owners, dependencies, and immediate unlocks.

This is not task management. It is governed execution design: each pathway inherits the Prime Directive framing from the judgment that produced it, the Polymorphia dimensions that were active, and the corpus entries that governed the reasoning. The execution map is traceable to its analytical foundation.

---

### The MDL Handshake

Multi-Dimensional Logic (Framework 2) produces multiple valid readings of the situation — the Polymorphia dimensional map. PSA Mode 2 converts those dimensions into executable routes.

The relationship is direct:

```
MDL produces:  D1 (dominant)  →  PSA produces:  Pathway A (execute on D1 reading)
               D2 (secondary) →                 Pathway B (hedge for D2 possibility)
```

A Polymorphia map with two dimensions does not just mean "we see two ways to read this." It means PSA can generate two execution pathways, each defensible under its dimension, allowing the operator to choose the path that matches their risk posture or to design a hybrid that survives either dimension.

This is the bridge between analysis and motion. Without Mode 2, Polymorphia produces insight that stops at the recommendation. With Mode 2, it produces insight that continues through to executable options.

---

### Pathway Generation

Each generated pathway is a structured execution object:

```json
{
  "pathway_id": "P1",
  "label": "Accelerated differentiation — defend premium segment",
  "polymorphia_dimension": "D1",
  "time_horizon": "90 days",
  "risk_profile": "medium — requires product velocity the current team may not support",
  "monetization_angle": "Preserve margin in premium; accept share loss in commoditized segment",
  "required_resources": ["2 senior engineers", "marketing budget reallocation", "CEO bandwidth for 3 key accounts"],
  "immediate_unlocks": ["Confirm product roadmap authority with CTO", "Identify 3 anchor customers to defend first"],
  "dependencies": ["Pricing authority confirmed", "Q4 budget approved"],
  "prime_directive_check": {
    "assets_liabilities": "Positive — defends highest-margin segment",
    "risk_reward": "Acceptable — asymmetric upside if differentiation holds",
    "supply_demand": "Favorable — premium segment still supply-constrained"
  }
}
```

Every pathway carries a Prime Directive check. PSA Mode 2 does not produce execution options that haven't been evaluated against the three lenses. Governed execution design, not free-standing motion.

---

### Role and Sequence Design

Beyond pathway generation, Mode 2 assigns ownership and sequencing:

- **Who** owns which decision or action on this pathway
- **What** must be resolved before the next step unlocks
- **Which** resources are required at each stage
- **When** each stage must complete for the pathway to remain viable

This is the answer to the market problem: "hard to turn ideas into action." The friction is rarely analysis — it is the gap between a good recommendation and a clear answer to "what do I do Monday morning, and in what order?" PSA Mode 2 closes that gap.

---

### Operational Packaging

Mode 2 output can be packaged into operational artifacts:

| Artifact | Description |
|---|---|
| **Execution pathway document** | Multi-pathway comparison with pros, cons, and selection criteria |
| **Milestone map** | Sequenced checkpoints for a selected pathway |
| **Dependency map** | Which decisions unlock which actions |
| **Owner assignment matrix** | Who owns what, with accountability structure |
| **Risk register** | Named risks per pathway with mitigation options |

---

### Cartridges as Field-Grade PSA Expression

Cartridges are the most concrete operational expression of PSA Mode 2.

A cartridge is a governed execution logic package for a recurring situation — M&A diligence, capital raise preparation, board meeting, hiring process, competitive response. It pre-loads the milestones, deliverable structure, owner assignments, red-flag signals, and drafting routines that PSA Mode 2 would generate if the operator started from scratch.

The difference: for novel situations, PSA Mode 2 generates the execution structure at runtime. For recurring situations, a cartridge pre-packages that structure so the operator can activate it immediately.

Cartridges are not static templates. They are living under PSA governance — which means they are also subscribed to Recursive Analysis (Framework 7). When conditions change, Recursive Analysis detects it and flags whether the cartridge's assumptions still hold.

---

## Relationship to Recursive Analysis

PSA and Recursive Analysis are explicitly paired. They are the forward-and-back mechanism of the Core 7:

- **PSA generates motion** — surfaces implications, designs execution pathways, packages operational logic
- **Recursive Analysis audits motion** — checks whether the generated pathways and prior judgments remain valid over time

Every execution pathway PSA generates inherits a Recursive Analysis subscription. If the assumptions that justified Pathway A change — if the market conditions, resource availability, or competitive posture shift — Recursive Analysis Mode 2 detects the drift and injects a corrective reflex.

PSA without Recursive Analysis produces momentum. Together they produce calibrated momentum: motion that self-corrects rather than persists blindly into changed conditions.

---

## Relationship to Heuristic Coding

Encoded heuristics are one of PSA's primary activation inputs. When PSA scans for implications (Mode 1) or generates execution pathways (Mode 2), it draws on the heuristic library for pre-encoded decision logic.

The relationship: Heuristic Coding creates reusable logic units. PSA is one of the primary frameworks that deploys them in the field — proactively, before the operator manually invokes them.

A heuristic tagged with the activation tags `{dynamic: urgency, situation: negotiation}` fires in PSA Mode 1 when those conditions are detected in the context, even if the operator has not asked about negotiation tactics. That is what makes PSA proactive rather than reactive.

---

## Relationship to the Organizational Perception Thesis

PSA Mode 1 is the operational mechanism of the organizational perception thesis:

> The biggest advantage of governed AI may not be speed. It may be that the organization can finally perceive patterns that were previously invisible to human cognition.

Human working memory is bounded. When an operator submits a question, they bring to it whatever they can hold in mind at that moment. PSA operates on the full assembled context — memory, corpus, Carats, compliance constraints — simultaneously. The patterns it surfaces are not patterns the operator could necessarily have seen. They become visible only when all the evidence is held in view at once and the governing logic is applied to the complete picture.

This is not a side benefit. It is the primary value proposition of governed AI.

---

## What PSA Does Not Do

PSA does not:
- Override the operator's stated question — it supplements, not replaces
- Make decisions on behalf of the operator — it surfaces; the operator decides
- Surface implications without evidence — every PSA signal must trace to a source in the context package
- Generate execution pathways that have not passed Prime Directive evaluation
- Apply indiscriminately — the materiality gate filters noise before it reaches output

---

## Audit Requirements

Every PSA Mode 1 activation must produce an audit record:
- All implications detected in the implication scan
- Which implications passed and failed the materiality gate, with suppression notes
- Final proactive signal set delivered to the Judgment Call
- Whether any signals became governance gaps and the current gap count

Every PSA Mode 2 activation must produce an audit record:
- Polymorphia dimensions that informed pathway generation
- Pathways generated with their Prime Directive check results
- Owner assignments and dependency structure
- Whether a cartridge was activated or a new pathway was generated at runtime

---

## Design Principle

> PSA is the difference between a system that answers questions and a system that governs decisions.

A system that answers questions is a sophisticated search tool. A system that governs decisions surfaces what the evidence implies, designs how to act on what has been decided, and packages that motion into governed execution structures the organization can actually use.

The governing standard for Mode 1: **if a competent senior advisor would have mentioned it before answering the question, PSA must have surfaced it.**

The governing standard for Mode 2: **if a decision has been reached, PSA must be able to answer "what do we do Monday morning, in what order, and who owns what."**

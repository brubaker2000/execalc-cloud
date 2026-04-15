# PROACTIVE_SOLUTIONS_ARCHITECTURE.md

## Status
Draft v0.1

## Owner
Architecture / Core 7

## Position in Core 7
Framework 6 — Activates during Activation Pathway assembly (Stage 4 of the Reflex and Activation System), before the Judgment Call.

---

## What Proactive Solutions Architecture Is

Proactive Solutions Architecture (PSA) is the Core 7 component that surfaces emerging risks and latent opportunities before the operator asks about them.

It is not a recommendation engine. It is a **forward-looking signal amplifier** — the component that ensures the governed judgment cycle does not limit itself to answering the operator's stated question when the governing logic implies there is something more important they have not asked.

The question PSA answers is:

> **What does the operator need to know that they have not yet asked about?**

---

## Why This Exists

An operator submits a query. The query defines a scope. A system that answers only within that scope is a search engine with better vocabulary.

A governed judgment system operates differently. The governing frameworks — Prime Directive, Polymorphia, memory, EKE corpus — frequently surface implications that extend beyond the stated question. If the operator asks "how should we respond to this competitive threat?" and the activated corpus and memory jointly imply a cash runway risk that makes the proposed response financially untenable, the governing obligation is to surface the cash runway risk — even though it was not asked about.

PSA is the mechanism that does this. It is not optional and it is not a courtesy feature. In a governed system, surfacing the implications of the evidence is part of the governance obligation.

---

## PSA vs. The Reflex System

This distinction matters:

| Component | When | What |
|---|---|---|
| Reflex System (Stage 3, Activation Pathway) | Before the Judgment Call | Pre-loads known response patterns for the detected scenario type |
| Proactive Solutions Architecture (Core 7, F6) | During Judgment Call reasoning | Surfaces implications from the specific evidence that the stated question did not ask about |

Reflexes are pre-encoded patterns: "when you see Scenario 7 (Negotiation), always ask about BATNA." PSA is inference from evidence: "given what the memory and corpus jointly imply about this operator's situation, there is a risk that has not been named."

Reflexes are scenario-class responses. PSA is situation-specific inference.

---

## Runtime Operation

### Stage 1: Implication Scan

After the context package is assembled (compliance constraints, Carats, scenario logic, reflexes, corpus entries, operator memory), PSA scans the assembled context for implications that extend beyond the stated question.

Implication types PSA detects:

| Implication Type | Description |
|---|---|
| Latent risk | Evidence in the context implies a risk that the operator has not named |
| Emerging opportunity | Signal pattern suggests a window that will not persist; operator may not have noticed |
| Assumption conflict | Operator's stated framing rests on an assumption that the corpus or memory contradicts |
| Decision dependency | The stated question cannot be answered correctly without resolving a prior question the operator has not addressed |
| Temporal urgency | Evidence implies a time constraint on the decision that the operator has not acknowledged |

---

### Stage 2: Materiality Gate

Not every implication warrants surfacing. PSA applies the GAQP Materiality principle: **only signal that changes what a decision-maker would rationally do is worth surfacing.**

Materiality test for each detected implication:

1. Would a fully informed senior advisor mention this before answering the stated question?
2. If acted on, would this implication materially change the recommended action?
3. Does the implication affect a Prime Directive lens that the stated question did not evaluate?

Implications that fail the materiality test are logged but not surfaced. The operator's attention is not diffused with noise.

---

### Stage 3: Proactive Signal Assembly

Implications that pass the materiality gate are assembled into a **proactive signal set** — a structured set of items the judgment call must address in addition to the stated question.

```
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

The proactive signal set is passed to the Judgment Call alongside the operator's stated question. The model is instructed:

> Address the proactive signals as part of your response. Do not wait to be asked. If a proactive signal materially changes the recommended action, surface it before the recommendation. If it qualifies the recommendation, surface it as a condition.

The output structure for a judgment call with active PSA signals:

```
[GOVERNING OBSERVATION — surfaces before recommendation if materiality = high]
Before addressing your question, one item demands attention: [signal description]

[RECOMMENDATION]
Given the above, the recommended course of action is...

[QUALIFYING CONDITIONS]
This recommendation assumes: [list of decision dependencies and medium-materiality signals]
```

---

## Relationship to Organizational Perception

PSA is the mechanism through which the organizational perception thesis becomes operational.

> The biggest advantage of governed AI may not be speed. It may be that the organization can finally perceive patterns that were previously invisible to human cognition.

Human cognition is bounded by working memory, attentional scope, and the ability to hold multiple complex implications simultaneously. When an operator submits a question, they are bringing to that question whatever they can hold in their mind at that moment.

PSA operates on the assembled context — which includes admitted memory, corpus entries spanning decades of institutional knowledge, and active Carats — simultaneously. The patterns it identifies are not necessarily patterns the operator could have seen. They are patterns that only become visible when all the evidence is held in view at once and the governing logic is applied to the full picture.

This is not a side benefit. It is the primary value proposition of governed AI over raw LLM access.

---

## Proactive Signal Persistence

A proactive signal that is surfaced but not resolved in a session becomes a **pending implication** — a memory candidate that follows the operator into the next session.

If the operator addresses the signal and resolves it (by acting on it, or by explicitly acknowledging it and choosing not to act), the resolution is admitted to memory as a governed decision artifact.

If the operator does not address the signal, it re-surfaces in the next relevant session with higher priority weight.

A signal that has been surfaced three times without resolution is flagged as a **governance gap** — a known implication that the operator has repeatedly not addressed. Governance gaps are disclosed to the operator explicitly:

```
[GOVERNANCE GAP — Third Instance]
This implication has been surfaced in three sessions without resolution.
It may represent a decision the organization has been deferring.
```

---

## What PSA Does Not Do

PSA does not:
- Override the operator's stated question — it supplements, not replaces
- Make decisions on behalf of the operator — it surfaces, the operator decides
- Surface implications without evidence — every PSA signal must trace to an evidence source in the context package
- Apply to every session indiscriminately — the materiality gate filters noise before it reaches the output

---

## Audit Requirements

Every PSA activation must produce an audit record containing:
- All implications detected in the implication scan
- Which implications passed and which failed the materiality gate
- Suppression notes for failed implications
- Final proactive signal set delivered to the Judgment Call
- Whether any signals became governance gaps and the gap count

---

## Design Principle

> PSA is the difference between a system that answers questions and a system that governs decisions.

A system that answers questions is a sophisticated search tool. A system that governs decisions surfaces what the evidence implies, not only what was asked. PSA is the operational expression of that distinction.

The governing standard: **if a competent senior advisor would have mentioned it before answering the question, PSA must have surfaced it.**

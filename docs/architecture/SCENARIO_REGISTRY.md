# SCENARIO_REGISTRY.md

## Status
Draft v0.1 — runtime-ready structure; activation logic and Carat mapping pending

## Owner
Executive Knowledge Engine (EKE)

## Purpose
This registry defines the 25 canonical executive-grade scenarios that form the primary trigger layer of Execalc's cognition engine.

These scenarios answer the first and most important question the runtime must resolve:

> **What situation are we actually in?**

Everything else follows from that answer:

```
Scenario → Activation Pathway → Carats / EKE Corpus → Prime Directive → Decision Artifact
```

Each scenario is defined as a triggerable object with activation logic, not a category label.

---

## Current Code Gap

The existing `engine.py` implementation contains only two hardcoded scenario types:
- `draft_trade`
- `feasibility`

This registry replaces that stub with the full governed scenario classification layer.

---

## Registry Structure

Each scenario entry contains:
- **Definition** — what situation this scenario describes
- **Trigger Conditions** — what circumstances cause this scenario to be active
- **Primary Output** — what the runtime is expected to produce
- **Activation Signals** — natural language phrases that indicate this scenario

---

## I. Growth & Opportunity Scenarios

### 1. Market Expansion

**Definition:** Entering new markets, geographies, or customer segments.

**Trigger Conditions:** Growth plateau, new demand signals, competitor expansion.

**Primary Output:** Entry strategy, risk map, resource allocation.

**Activation Signals:** "expand into," "new market," "international," "new segment"

---

### 2. Revenue Acceleration

**Definition:** Increasing top-line growth within the current business model.

**Trigger Conditions:** Growth targets unmet, scaling opportunity identified.

**Primary Output:** Levers for growth (pricing, channel, product mix).

**Activation Signals:** "increase revenue," "growth stalled," "scale faster"

---

### 3. Pricing and Positioning

**Definition:** Determining value capture and market perception.

**Trigger Conditions:** Margin pressure, commoditization risk, repositioning need.

**Primary Output:** Pricing strategy, positioning narrative, elasticity analysis.

**Activation Signals:** "pricing," "discounting," "premium vs volume"

---

### 4. Product Strategy

**Definition:** Deciding what to build, enhance, or retire.

**Trigger Conditions:** Feature sprawl, unclear roadmap, competitive gaps.

**Primary Output:** Product roadmap, prioritization, tradeoffs.

**Activation Signals:** "roadmap," "feature," "product direction"

---

### 5. Go-To-Market Strategy

**Definition:** How the product reaches and converts customers.

**Trigger Conditions:** Low conversion, misaligned channels, weak pipeline.

**Primary Output:** Channel mix, messaging, funnel optimization.

**Activation Signals:** "GTM," "sales funnel," "lead conversion"

---

## II. Deal and Capital Scenarios

### 6. Deal Origination

**Definition:** Identifying and sourcing opportunities (M&A, partnerships, trades).

**Trigger Conditions:** Strategic growth need, market scanning.

**Primary Output:** Target list, deal theses, outreach strategy.

**Activation Signals:** "looking for deals," "targets," "opportunities"

---

### 7. Negotiation

**Definition:** Structuring and closing agreements under tension.

**Trigger Conditions:** Active deal discussions, conflicting interests.

**Primary Output:** Leverage map, concession strategy, BATNA analysis.

**Activation Signals:** "offer," "counter," "terms," "leverage"

---

### 8. Due Diligence

**Definition:** Validating assumptions and uncovering hidden risks.

**Trigger Conditions:** Pending deal or major decision.

**Primary Output:** Risk audit, assumption validation, red flags.

**Activation Signals:** "verify," "diligence," "concerns," "unknowns"

---

### 9. Capital Allocation

**Definition:** Deploying financial resources across opportunities.

**Trigger Conditions:** Budgeting decisions, investment tradeoffs.

**Primary Output:** ROI ranking, capital deployment plan.

**Activation Signals:** "where to invest," "budget," "allocation"

---

### 10. Exit Strategy

**Definition:** Planning liquidity events or strategic exits.

**Trigger Conditions:** Maturity stage, acquisition interest.

**Primary Output:** Timing, valuation strategy, buyer targeting.

**Activation Signals:** "sell," "exit," "acquisition," "IPO"

---

## III. Organizational and Execution Scenarios

### 11. Team Building

**Definition:** Hiring, structuring, and upgrading talent.

**Trigger Conditions:** Skill gaps, scaling team, underperformance.

**Primary Output:** Hiring plan, org design, role clarity.

**Activation Signals:** "hire," "team," "roles," "talent gap"

---

### 12. Executive Alignment

**Definition:** Resolving leadership misalignment and internal friction.

**Trigger Conditions:** Conflicting priorities, political tension.

**Primary Output:** Alignment map, decision clarity, authority structure.

**Activation Signals:** "disagreement," "misaligned," "leadership conflict"

---

### 13. Execution Infrastructure

**Definition:** Fixing broken systems, workflows, or operating models.

**Trigger Conditions:** Bottlenecks, missed deadlines, inefficiency.

**Primary Output:** System redesign, process correction.

**Activation Signals:** "slow," "broken process," "inefficiency"

---

### 14. Strategic Drift

**Definition:** Loss of focus or deviation from core mission.

**Trigger Conditions:** Scattered initiatives, unclear priorities.

**Primary Output:** Refocus plan, priority reset.

**Activation Signals:** "too many things," "unclear direction"

---

### 15. Judgment Compression

**Definition:** Overload of decisions requiring prioritization.

**Trigger Conditions:** Decision fatigue, too many simultaneous choices.

**Primary Output:** Ranked decisions, simplified options.

**Activation Signals:** "too many decisions," "overwhelmed"

---

## IV. Risk and Defense Scenarios

### 16. Crisis Management

**Definition:** Responding to immediate threats or failures.

**Trigger Conditions:** PR issues, operational breakdowns.

**Primary Output:** Containment strategy, communication plan.

**Activation Signals:** "urgent," "crisis," "problem now"

---

### 17. Risk Mitigation

**Definition:** Identifying and reducing exposure to downside.

**Trigger Conditions:** Uncertain environment, vulnerability detected.

**Primary Output:** Risk map, mitigation plan.

**Activation Signals:** "risk," "exposure," "downside"

---

### 18. Competitive Threat

**Definition:** Responding to competitor moves.

**Trigger Conditions:** New entrant, pricing pressure, innovation threat.

**Primary Output:** Counter-strategy.

**Activation Signals:** "competitor," "they launched," "losing share"

---

### 19. Regulatory and Compliance

**Definition:** Navigating legal and regulatory constraints.

**Trigger Conditions:** Policy changes, compliance risk.

**Primary Output:** Compliance strategy, risk avoidance.

**Activation Signals:** "regulation," "legal," "compliance"

*Note: When a Compliance Cartridge is active (see `COMPLIANCE_CARTRIDGE_ARCHITECTURE.md`), this scenario inherits elevated priority and the compliance gate runs before any other evaluation.*

---

### 20. Reputation and PR

**Definition:** Managing perception and brand integrity.

**Trigger Conditions:** Public scrutiny, brand risk.

**Primary Output:** Messaging strategy, reputation defense.

**Activation Signals:** "press," "brand," "reputation"

---

## V. Strategic Insight and Optimization Scenarios

### 21. Opportunity Discovery

**Definition:** Identifying unseen upside.

**Trigger Conditions:** Ambiguous situation, unexplored space.

**Primary Output:** Opportunity map.

**Activation Signals:** "what are we missing," "hidden opportunity," "untapped"

---

### 22. Resource Optimization

**Definition:** Improving efficiency and output.

**Trigger Conditions:** Underperformance, waste detected.

**Primary Output:** Optimization plan.

**Activation Signals:** "inefficient," "waste," "optimize"

---

### 23. Scenario Planning

**Definition:** Modeling future possibilities.

**Trigger Conditions:** Uncertainty, long-term decisions.

**Primary Output:** Scenario trees, probability paths.

**Activation Signals:** "what if," "future," "forecast"

---

### 24. Innovation and Disruption

**Definition:** Creating new models or breaking existing ones.

**Trigger Conditions:** Stagnation, disruptive opportunity.

**Primary Output:** Innovation strategy.

**Activation Signals:** "new model," "disrupt," "reinvent"

---

### 25. Partnership Strategy

**Definition:** Forming alliances to create leverage.

**Trigger Conditions:** Capability gaps, scaling need.

**Primary Output:** Partner identification, deal structure.

**Activation Signals:** "partner," "collaboration," "joint venture"

---

## Scenario Index

| # | Name | Bucket | Key Signals |
|---|---|---|---|
| 1 | Market Expansion | Growth | expand into, new market |
| 2 | Revenue Acceleration | Growth | increase revenue, scale faster |
| 3 | Pricing and Positioning | Growth | pricing, discounting |
| 4 | Product Strategy | Growth | roadmap, feature |
| 5 | Go-To-Market Strategy | Growth | GTM, sales funnel |
| 6 | Deal Origination | Deal & Capital | looking for deals, targets |
| 7 | Negotiation | Deal & Capital | offer, counter, leverage |
| 8 | Due Diligence | Deal & Capital | verify, diligence, unknowns |
| 9 | Capital Allocation | Deal & Capital | budget, allocation |
| 10 | Exit Strategy | Deal & Capital | sell, exit, IPO |
| 11 | Team Building | Org & Execution | hire, talent gap |
| 12 | Executive Alignment | Org & Execution | misaligned, leadership conflict |
| 13 | Execution Infrastructure | Org & Execution | broken process, inefficiency |
| 14 | Strategic Drift | Org & Execution | too many things, unclear direction |
| 15 | Judgment Compression | Org & Execution | too many decisions, overwhelmed |
| 16 | Crisis Management | Risk & Defense | urgent, crisis |
| 17 | Risk Mitigation | Risk & Defense | risk, exposure, downside |
| 18 | Competitive Threat | Risk & Defense | competitor, losing share |
| 19 | Regulatory and Compliance | Risk & Defense | regulation, legal, compliance |
| 20 | Reputation and PR | Risk & Defense | press, brand, reputation |
| 21 | Opportunity Discovery | Strategic Insight | what are we missing |
| 22 | Resource Optimization | Strategic Insight | inefficient, optimize |
| 23 | Scenario Planning | Strategic Insight | what if, forecast |
| 24 | Innovation and Disruption | Strategic Insight | disrupt, reinvent |
| 25 | Partnership Strategy | Strategic Insight | partner, joint venture |

---

## Runtime Architecture Notes

### Multi-Scenario Detection
A single session may activate multiple scenarios simultaneously. The runtime must support:
- primary scenario designation
- secondary scenario designation
- conflict detection when two scenarios produce contradictory recommendations
- audit visibility into which scenarios were detected but not activated as primary

### Scenario Confidence
Scenario detection should carry a confidence score. Low-confidence detection should surface the ambiguity to the operator rather than silently routing to an incorrect scenario.

### Escalation Path
If no scenario can be confidently classified, the runtime defaults to Opportunity Discovery (Scenario 21) as the broadest safe container and requests clarifying input from the operator.

---

## Required Follow-On Work

1. **Carat mapping** — attach relevant Carats and heuristics to each scenario (highest priority next step)
2. **Confidence weighting logic** — how certain must signal detection be before routing to a scenario
3. **API endpoint mapping** — map each scenario to its decision artifact template and execution path
4. **Deep-spec layer** — full input/output contracts, Prime Directive overlays, and execution logic for each scenario (recommend prioritizing top 10 first)
5. **Multi-scenario arbitration rules** — what happens when scenarios conflict

---

## Relationship to Existing Code

The current `engine.py` `CRITICAL_FIELDS_BY_SCENARIO` dict contains two entries (`draft_trade`, `feasibility`) that predate this registry. Those entries should be deprecated in Stage 8 and replaced by this registry as the authoritative scenario source.

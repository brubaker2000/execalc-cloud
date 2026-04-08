# Executive Knowledge Engine Corpus Schema

## Purpose

This document defines the canonical schema for storing, organizing, tagging, and invoking the Executive Knowledge Engine corpus.

The corpus is not merely a reading list. It is a governed inventory of reusable executive logic.

---

## Core Hierarchy

The corpus is organized as:

```
Pillar
  └── Framework
        └── Strategy
              └── Detail
```

---

## Object Definitions

### Pillar

A top-level executive reasoning domain.

Examples:
- Playing to Win
- Growth Mastery
- Execution Without Excuses
- Risk, Resilience, and Playing the Long Game
- Competitive Domination
- Leadership That Moves Mountains
- Winning the Future

### Framework

A named reasoning instrument within a pillar.

Examples:
- Strategy Diamond
- Ansoff Matrix
- Hoshin Kanri X-Matrix
- Porter's Five Forces
- VRIO Framework
- CEO Scorecard

### Strategy

A sub-logic or application pattern within a framework.

Examples:
- Market Penetration
- Product Development
- Buyer Power analysis
- Catch-ball process

### Detail

The atomic nugget within the strategy layer.

Examples:
- specific principles
- operating notes
- decision cues
- explanatory logic
- activation hints

---

## Required Metadata

Every framework object should carry:

| Field | Description |
|---|---|
| `framework_id` | Unique identifier |
| `title` | Human-readable name |
| `pillar` | Parent pillar |
| `summary` | One-paragraph description of purpose and use |
| `activation_triggers` | Scenario signals that should activate this framework |
| `applicable_scenarios` | Named executive scenarios where this applies |
| `core_questions` | The structured questions this framework is designed to answer |
| `expected_outputs` | What decision-grade outputs this framework produces |
| `related_frameworks` | Other frameworks that complement this one |
| `conflicting_frameworks` | Frameworks that may produce contradictory conclusions |
| `complementary_frameworks` | Frameworks that amplify this one when combined |
| `memory_tags` | Classification tags for retrieval |
| `use_cases` | Concrete examples of past or archetypal application |
| `source_provenance` | Original source or lineage of the framework |
| `confidence_level` | How well-validated this framework is within the corpus |

---

## Runtime Role

The corpus is activated through governed operations, not ad hoc recall.

Key runtime relationships:

- `FRAME()` — chooses the relevant framework(s)
- `THINKER()` — activates a doctrine source or logic family
- `PRECEDENT()` — connects the current case to historical analogues
- `SYNTHESIZE()` — converts selected framework logic into decision-grade output

---

## Design Principles

1. **Frameworks should be callable, not merely searchable.**  
   Each framework must carry explicit triggers and expected use cases so the runtime can activate it deterministically.

2. **Each framework should carry explicit triggers and expected use cases.**  
   Activation should be scenario-driven, not keyword-driven.

3. **Conflicts between frameworks should be visible, not hidden.**  
   When two frameworks give contradictory answers, that tension is itself a signal.

4. **Framework outputs should remain traceable to the selected logic source.**  
   Execalc must be able to explain which framework was applied and why.

5. **The corpus should be modular, extensible, and tenant-safe.**  
   Tenants may carry private cartridges. The Monolith is the shared corpus baseline.

---

## Corpus Layers

The EKE corpus has two primary layers:

### The Monolith
The shared baseline corpus of executive frameworks, heuristics, and reasoning instruments available across all tenants. Curated and maintained by Execalc.

### Cartridges
Tenant-specific or scenario-specific bundles of logic, context, and frameworks that extend or override the Monolith within a tenant namespace. May include:
- client-specific heuristics
- proprietary frameworks
- domain-specific reasoning instruments
- operator-supplied knowledge

Cartridges are tenant-scoped and never bleed across tenant boundaries.

---

## Thesis

The Executive Knowledge Engine corpus is the inventory layer of Execalc's governed cognition stack: a structured ontology of executive reasoning that can be selectively activated at runtime.

It is not a library. It is a callable knowledge system.

The difference: a library stores for passive retrieval. The EKE corpus activates for governed application.

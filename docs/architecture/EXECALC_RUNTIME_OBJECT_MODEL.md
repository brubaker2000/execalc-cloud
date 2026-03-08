# Execalc Runtime Object Model

## Purpose

This document defines the core runtime objects that move through the Execalc system.

The goal is to translate the architectural reasoning stack into concrete, governable objects that the system can process, store, route, and evaluate.

These runtime objects form the implementation bridge between:

- user interaction
- knowledge activation
- diagnostics
- reflexes
- decision artifacts
- governed execution

---

# Why Runtime Objects Matter

Without explicit runtime objects, Execalc risks becoming a loose collection of features and ideas.

With explicit runtime objects, the system gains:

- architectural clarity
- implementation discipline
- testable interfaces
- clearer persistence rules
- cleaner governance boundaries

Each major capability in Execalc should ultimately map to one or more runtime objects.

---

# Core Runtime Object Families

The current architecture suggests the following primary runtime object families:

1. Scenario
2. Signal
3. KnowledgeAsset
4. Cartridge
5. Nugget
6. Diagnostic
7. Reflex
8. DecisionArtifact
9. AuthorizationObject

These objects do not all need to be fully implemented immediately, but they should be recognized as first-class architectural concepts.

---

# 1. Scenario

## Definition

A Scenario is the primary framing object for strategic reasoning.

It represents a defined situation requiring evaluation, planning, comparison, or action.

## Typical fields

- scenario_id
- tenant_id
- operator_id
- scenario_type
- domain
- governing_objective
- facts
- constraints
- urgency
- source_surface
- created_at

## Purpose

The Scenario object is the main entry point into governed reasoning.

It tells Execalc what kind of situation it is dealing with.

## Examples

- negotiation
- due diligence
- capital allocation
- hiring decision
- operational bottleneck
- monetization opportunity

---

# 2. Signal

## Definition

A Signal is a detected pattern, event, or observation that may or may not rise to the level of a scenario.

Signals are often ambient and may originate from monitored surfaces.

## Typical fields

- signal_id
- tenant_id
- source_surface
- signal_type
- signal_strength
- related_entities
- summary
- recommended_surface_level
- observed_at

## Purpose

Signals allow Execalc to notice potentially important developments before formal scenario invocation.

## Examples

- repeated mention of a stakeholder in email
- competitor movement on LinkedIn
- Slack friction around a project
- calendar clustering around a sensitive initiative

---

# 3. KnowledgeAsset

## Definition

A KnowledgeAsset is the generic parent object for any governed knowledge unit available to the Executive Knowledge Engine.

It is the abstraction layer above specific types such as nuggets, cartridges, datasets, and external sources.

## Typical fields

- asset_id
- asset_type
- name
- source
- domain
- scope
- trust_weight
- tenant_scope
- activation_conditions
- status
- created_at

## Purpose

KnowledgeAsset provides a common registry model so the runtime can reason about available knowledge in a uniform way.

---

# 4. Cartridge

## Definition

A Cartridge is a modular strategic overlay that injects structured reasoning logic into runtime analysis.

## Typical fields

- cartridge_id
- cartridge_type
- name
- scope
- domain
- trigger_conditions
- linked_reflexes
- linked_diagnostics
- tenant_scope
- status

## Purpose

Cartridges allow Execalc to apply scenario-specific reasoning packages.

## Examples

- negotiation cartridge
- due diligence cartridge
- SWOT overlay
- client policy cartridge

---

# 5. Nugget

## Definition

A Nugget is an atomic strategic insight derived from a thought leader or canonical source.

## Typical fields

- nugget_id
- source_name
- title
- domain
- trigger_context
- confidence_weight
- publication_status
- attribution
- status

## Purpose

Nuggets allow small, targeted units of reasoning to be activated by reflexes or diagnostics.

## Examples

- signal-to-noise principle
- jobs-to-be-done framing
- asymmetry recognition heuristic

---

# 6. Diagnostic

## Definition

A Diagnostic is a callable analytical procedure that directs Execalc to evaluate a situation through a defined set of lenses or rules.

## Typical fields

- diagnostic_id
- name
- category
- invocation_phrase
- frameworks_used
- domain
- scope
- expiration
- status

## Purpose

Diagnostics are active analysis routines, not passive knowledge.

## Examples

- Ten-Point Diagnostic
- Negotiation Leverage Diagnostic
- NHL Draft Rules Diagnostic

## Typical fields

- diagnostic_id
- name
- category
- invocation_phrase
- frameworks_used
- domain
- scope
- expiration
- status

## Purpose

Diagnostics are active analysis routines, not passive knowledge.

## Examples

- Ten-Point Diagnostic
- Negotiation Leverage Diagnostic
- NHL Draft Rules Diagnostic

---

# 7. Reflex

## Definition

A Reflex is an automatic runtime trigger that detects a pattern and activates logic without requiring an explicit operator command.

## Typical fields

- reflex_id
- name
- trigger_pattern
- domain
- scope
- linked_assets
- action_type
- priority
- status

## Purpose

Reflexes provide the automatic pattern-detection and response capability of Execalc.

## Examples

- Blind/Deaf Reflex
- Free Agent Reflex
- Compromise Awareness Reflex
- governance checkpoint reflexes

---

# 8. DecisionArtifact

## Definition

A DecisionArtifact is the structured output of governed reasoning.

It is what Execalc produces after scenario framing, knowledge activation, and analytical procedure execution.

## Typical fields

- artifact_id
- scenario_id
- tenant_id
- operator_id
- executive_summary
- confidence
- sensitivity_analysis
- next_actions
- supporting_rationale
- created_at

## Purpose

DecisionArtifact is the principal executive-facing output object of the system.

It turns reasoning into a durable strategic deliverable.

---

# 9. AuthorizationObject

## Definition

An AuthorizationObject represents governed permission for downstream execution.

It exists to ensure that action only proceeds after passing through the appropriate reasoning and governance layers.

## Typical fields

- authorization_id
- tenant_id
- operator_id
- linked_scenario_id
- action_type
- authorization_status
- rationale
- issued_at
- expires_at

## Purpose

AuthorizationObject is the bridge between reasoning and execution.

It prevents unguided or unauthorized automation.

---

# Object Relationships

The runtime objects are not isolated. They relate to one another in structured ways.

Typical flow:

Signal
→ Scenario
→ KnowledgeAsset selection
→ Cartridge / Nugget / Diagnostic / Reflex activation
→ DecisionArtifact
→ AuthorizationObject when execution is permitted

This flow gives Execalc a coherent runtime model.

---

# Design Principles

## 1. Objects should be explicit
If a concept matters at runtime, it should eventually have an object model.

## 2. Objects should be governable
Each object should have clear ownership, scope, and lifecycle rules.

## 3. Objects should be tenant-aware
Any client-scoped object must respect strict tenant isolation.

## 4. Objects should be composable
Objects should work together through clean interfaces rather than ad hoc logic.

## 5. Objects should support persistence where appropriate
Scenarios, signals, and decision artifacts are especially likely to require durable storage.

---

# Summary

The Runtime Object Model gives Execalc a concrete implementation spine.

It defines the principal objects that move through the system:

- Scenario
- Signal
- KnowledgeAsset
- Cartridge
- Nugget
- Diagnostic
- Reflex
- DecisionArtifact
- AuthorizationObject

These objects translate high-level architecture into implementable and governable runtime structure.

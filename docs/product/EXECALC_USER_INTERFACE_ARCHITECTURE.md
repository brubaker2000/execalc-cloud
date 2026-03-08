# EXECALC USER INTERFACE ARCHITECTURE

## Purpose

This document defines the user interface architecture for Execalc.

The UI is not the product by itself.
It is the governed surface structure through which the operator experiences the deeper reasoning system.

This document explains:
- the major interface surfaces
- how those surfaces relate to one another
- the three primary operating modes
- what kinds of objects and behaviors belong in each surface
- how governed reasoning should appear without exposing unnecessary internal machinery

---

## Core Principle

Execalc is a strategic operating system, not a single chat screen.

Its user interface must therefore be designed as a multi-surface executive workspace.

These surfaces are not separate products.
They are interface zones inside one governed environment.

Every major capability should have a clear surface.
No important capability should exist only as hidden backend logic.

---

## Interface Architecture Goals

The interface architecture should allow the operator to:

- think clearly
- receive relevant signals
- invoke structured procedures
- review decision artifacts
- move from discussion to planning
- govern the system itself where authorized
- work across multiple executive surfaces without fragmentation

The UI should make governed cognition usable.

---

## Primary Surface Families

The current and planned UI architecture includes the following primary surface families:

- Chat Workspace
- Decision Views
- Diagnostic Views
- Planning Interfaces
- Monitoring Surfaces
- Admin / Control Surfaces
- future modules

These are coordinated surfaces inside a common operating environment.

---

## The Three Operating Modes

The UI should be understood through three operating modes.

### 1. Workbench Mode

Workbench Mode is where the operator actively thinks, asks, compares, plans, and decides.

Typical surfaces:
- chat workspace
- decision views
- diagnostic views
- planning interfaces
- comparison interfaces

Primary purpose:
convert live executive thought into governed judgment and usable outputs.

### 2. Monitoring Mode

Monitoring Mode is where Execalc observes relevant environments for strategic signals.

Typical surfaces:
- email-linked views
- Slack-linked views
- calendar-linked views
- LinkedIn or feed-linked views
- digest or alert surfaces

Primary purpose:
surface actionable developments without requiring the operator to hunt for them manually.

### 3. Control Tower Mode

Control Tower Mode is where the operator or administrator governs the system itself.

Typical surfaces:
- admin panel
- permissions
- cartridge and policy management
- registry views
- audit views
- governance controls

Primary purpose:
maintain disciplined operation, visibility, and trust boundaries.

These three modes together define the UI architecture at the highest level.

---

## Surface 1: Chat Workspace

### Role

The Chat Workspace is the primary workbench surface.

It is where the operator should be able to:
- think in natural language
- frame situations
- request analysis
- invoke diagnostics
- compare options
- receive signal surfacing
- review decision artifacts
- transition into planning

### UI requirements

The chat surface should support:
- natural operator input
- structured response formatting
- decision artifact previews
- lightweight signal presentation
- diagnostic recommendation and invocation
- continuity across related lines of reasoning

### Constraint

The chat surface should not become a dumping ground for every system function.
It is the central workbench, but not the only surface.

---

## Surface 2: Decision Views

### Role

Decision Views are the structured surfaces where governed reasoning outputs can be inspected more deliberately.

Examples of content:
- executive summaries
- tradeoff views
- recommendation rationale
- confidence and sensitivity sections
- comparison results
- durable decision artifacts

### UI requirements

Decision Views should make it easy to:
- read a conclusion quickly
- inspect the logic structure behind it
- compare alternatives
- revisit prior decision artifacts
- preserve continuity over time

### Constraint

Decision Views should present structured reasoning clearly without exposing raw internal machinery unnecessarily.

---

## Surface 3: Diagnostic Views

### Role

Diagnostic Views provide deliberate access to analytical procedures.

Examples:
- Ten-Point Diagnostic
- Negotiation Leverage Diagnostic
- Strategic Position Diagnostic
- future domain diagnostics

### UI requirements

Diagnostic Views should allow the operator to:
- choose or invoke a diagnostic
- understand the practical purpose of the diagnostic
- inspect structured findings
- move from findings into a decision artifact or next-step plan

### Constraint

Diagnostics should appear as deliberate tools, not hidden magic and not opaque automation.

---

## Surface 4: Planning Interfaces

### Role

Planning Interfaces turn governed reasoning into sequence and execution support.

Examples:
- next-step plans
- preparation checklists
- phased sequences
- meeting preparation structures
- comparison-driven action plans

### UI requirements

Planning Interfaces should make it easy to:
- convert strategy into sequence
- distinguish immediate steps from later steps
- preserve reasoning context
- connect plans back to the decision artifact or scenario that produced them

### Constraint

Planning should remain governed by the underlying decision logic, not drift into free-floating task clutter.

---

## Surface 5: Monitoring Surfaces

### Role

Monitoring Surfaces provide visibility into signals from monitored environments.

Examples:
- alert and digest surfaces
- email-derived signals
- Slack-derived signals
- calendar clustering signals
- feed or market observation surfaces

### UI requirements

Monitoring Surfaces should:
- surface signals in proportion to action relevance
- remain non-intrusive by default
- make urgency visible when warranted
- allow the operator to drill into why a signal matters
- connect surfaced signals back to scenarios, recommendations, or decisions where relevant

### Constraint

The UI must not reward novelty over consequence.
A signal should surface only if it changes what the operator would rationally do.

---

## Surface 6: Admin / Control Surfaces

### Role

Admin and Control Surfaces govern the system itself.

Examples:
- tenant settings
- permissions
- audit views
- registry views
- policy surfaces
- cartridge management
- future canon/governance controls

### UI requirements

These surfaces should allow authorized users to:
- inspect system configuration
- review audit history
- govern access and permissions
- manage approved runtime instruments
- maintain trust, clarity, and boundary enforcement

### Constraint

These surfaces are for governance and administration, not for routine operator thinking.

---

## Cross-Surface Design Rules

### 1. Every major capability needs a surface
If a capability matters to runtime behavior, it should eventually have a corresponding UI surface or visible interaction point.

### 2. Surfaces should be coordinated, not siloed
The operator should be able to move logically from:
- signal
- to discussion
- to diagnostic
- to decision artifact
- to plan
without losing context.

### 3. Surface behavior should follow action relevance
What appears where should depend on what helps the operator act rationally.

### 4. Internal structure should remain mostly behind the curtain
The UI should benefit from strong internal object models without narrating them unnecessarily.

### 5. Different surfaces may show the same underlying object differently
A Scenario, Signal, or DecisionArtifact may appear in multiple surfaces, but each surface should present it according to its use case.

---

## Relationship to Runtime Objects

The UI architecture should eventually map cleanly to the runtime object model.

Typical mappings include:

- Chat Workspace → Scenario intake, signal surfacing, decision artifact discussion
- Decision Views → DecisionArtifact inspection and comparison
- Diagnostic Views → Diagnostic invocation and result review
- Monitoring Surfaces → Signal visibility and triage
- Admin / Control Surfaces → AuthorizationObject, registry visibility, audit surfaces

The UI is therefore not separate from the runtime object model.
It is how runtime objects become operationally usable.

---

## Relationship to the Intelligent Front Door

The Intelligent Front Door is a separate but interlocking perimeter product.

It should not be collapsed into the main Execalc UI architecture as if it were just another internal panel.

Relationship:
- IFD handles perimeter intake and triage
- Execalc handles internal governed cognition and decision work

Interlock:
- IFD can feed structured objects into Execalc
- Execalc can review, reason over, and act on the outputs of IFD
- UI boundaries should preserve the distinction between perimeter triage and internal executive work

This distinction protects product clarity and future build flexibility.

---

## Surface Presentation Rules

Across all surfaces, the UI should aim for:

- clarity over spectacle
- strategic usefulness over decorative complexity
- structured outputs over vague conversational drift
- signal discipline over noise
- continuity over fragmentation

The UI should not:
- expose internal IDs for self-justification
- dramatize routine system behavior
- bury important decisions inside loose chat alone
- confuse monitoring with decision-making
- overload the operator with every possible surface at once

---

## Recommended Near-Term UI Spine

A practical near-term UI spine would likely emphasize:

1. Chat Workspace  
2. Decision Views  
3. Diagnostic invocation surfaces  
4. Lightweight monitoring/alert surfaces  
5. Admin and audit views for governance

This sequence reflects current implementation leverage and operator value.

---

## Future-Compatible Extension Areas

The architecture should remain open to future additions such as:

- richer comparison interfaces
- journal and artifact libraries
- cartridge browsers
- scenario dashboards
- organization-wide synthesis views
- richer signal triage boards
- planning boards linked to decision artifacts

These should extend the same surface logic rather than creating disconnected mini-products.

---

## Summary

Execalc's user interface architecture is a governed multi-surface executive workspace.

It is organized around three operating modes:
- Workbench Mode
- Monitoring Mode
- Control Tower Mode

Within those modes, the main surfaces include:
- chat workspace
- decision views
- diagnostic views
- planning interfaces
- monitoring surfaces
- admin and control surfaces

The purpose of the UI is not to decorate the system.
It is to make governed reasoning visible, usable, and operationally valuable without exposing unnecessary internal mechanics.

That is how the interface supports Execalc as a strategic operating system rather than a simple chatbot.

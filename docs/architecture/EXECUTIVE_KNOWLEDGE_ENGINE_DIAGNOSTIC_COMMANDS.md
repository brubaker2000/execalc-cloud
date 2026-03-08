# EXECUTIVE KNOWLEDGE ENGINE DIAGNOSTIC COMMANDS

## Purpose

This document defines diagnostic commands as a governed class of callable analytical procedures inside Execalc.

Diagnostics are not passive knowledge. They are active procedures that tell the system how to evaluate a situation through a structured sequence of lenses, checks, or rules.

This document exists to bridge doctrine into implementation. It defines:
- what a diagnostic command is
- how diagnostic commands differ from other runtime objects
- how they are invoked
- how they are governed
- how they should map into runtime scaffolding and future services

---

## Core Definition

A diagnostic command is a callable analytical procedure that directs Execalc to examine a situation using a predefined evaluation method.

A diagnostic command may:
- apply a fixed framework
- run a sequence of structured questions
- compare present facts against explicit criteria
- force disciplined evaluation when freeform reasoning would be too loose
- produce a structured decision artifact

Diagnostic commands belong to the analytical procedure layer of the reasoning stack.

They are procedure, not content.

---

## Why Diagnostic Commands Exist

Execalc is not only a knowledge system. It is a governed reasoning system.

Knowledge alone is insufficient for executive-grade judgment. The system also needs repeatable methods for:
- pressure-testing assumptions
- forcing complete evaluation
- comparing options
- identifying leverage, weakness, risk, or drift
- generating stable, auditable decision procedures

Diagnostic commands supply that procedural discipline.

They reduce drift, inconsistency, and unstructured improvisation.

---

## Distinction From Other Runtime Objects

### Diagnostic command vs Nugget
A nugget is a discrete unit of strategic thought.
A diagnostic command is a procedure for evaluating a situation.

Nuggets provide insight.
Diagnostics provide method.

### Diagnostic command vs Reflex
A reflex is an automatic trigger that fires when a pattern is detected.
A diagnostic command is a callable procedure that performs a structured analysis.

Reflexes detect.
Diagnostics evaluate.

A reflex may recommend or invoke a diagnostic command, but the two are not the same object.

### Diagnostic command vs Cartridge
A cartridge is a broader strategic overlay or contextual logic package that shapes reasoning in a given domain or scenario.

A diagnostic command is narrower.
It is a specific evaluative routine that may run inside a cartridge-governed context.

Cartridges shape posture.
Diagnostics shape procedure.

### Diagnostic command vs Scenario
A scenario describes the kind of executive situation currently present.

A diagnostic command does not classify the situation.
It evaluates the situation once the relevant framing is known.

Scenarios identify the game.
Diagnostics evaluate the board position.

---

## Canonical Characteristics

A proper diagnostic command should be:

1. Callable  
   It can be explicitly invoked by operator command or authorized runtime logic.

2. Structured  
   It follows a known procedure, not ad hoc improvisation.

3. Governed  
   It is subject to Strategic Mesh controls, authorization rules, and scope boundaries.

4. Auditable  
   Its invocation and outputs can be logged and traced.

5. Domain-aware  
   It may be general or domain-specific, but domain scope must be explicit.

6. Output-oriented  
   It should produce a usable artifact, not just freeform commentary.

7. Bounded  
   Temporary or narrow diagnostics may expire or be session-bound.

---

## Diagnostic Command Categories

Diagnostic commands may be organized into categories such as:

### 1. Core executive diagnostics
Reusable procedures applicable across many business contexts.

Examples:
- Ten-Point Diagnostic
- Strategic Position Diagnostic
- Judgment Compression Diagnostic

### 2. Negotiation diagnostics
Used to evaluate leverage, asymmetry, concession risk, and bargaining posture.

Examples:
- Negotiation Leverage Diagnostic
- Compromise Risk Diagnostic

### 3. Scenario-linked diagnostics
Attached to a specific executive-grade scenario.

Examples:
- Capital Raise Readiness Diagnostic
- Strategic Drift Diagnostic
- Executive Alignment Diagnostic

### 4. Domain diagnostics
Applied only within a clearly bounded subject area.

Examples:
- NHL Draft Rules Diagnostic
- Public Adjuster Lienholder Workflow Diagnostic
- Multi-Tenant Isolation Review Diagnostic

### 5. Temporary or tactical diagnostics
Session-bound or low-frequency procedures used when a narrow contextual need exists.

These should be explicitly tagged as temporary, sandboxed, or expiring objects.

---

## Canonical Examples

The repo already recognizes the following examples as canonical or near-canonical diagnostic types:

- Ten-Point Diagnostic
- Negotiation Leverage Diagnostic
- Strategic Position Diagnostic
- temporary domain diagnostics such as NHL Draft Rules

These examples should be treated as procedural classes, not merely prompt names.

---

## Invocation Model

Diagnostic commands should support two invocation modes.

### 1. Explicit operator invocation
The operator deliberately requests a diagnostic procedure.

Examples:
- run the Ten-Point Diagnostic
- apply the Negotiation Leverage Diagnostic
- evaluate this using the Strategic Position Diagnostic

This is the preferred default mode for most diagnostics.

### 2. Governed runtime suggestion or invocation
The runtime may suggest a diagnostic or invoke one automatically when authorized by policy.

Examples:
- a reflex detects a compromise pattern and recommends leverage review
- a scenario classifier detects strategic drift and proposes a relevant diagnostic
- a governed workflow calls a required diagnostic before producing a recommendation

Automatic invocation should be limited and policy-controlled.
High-visibility or introspective diagnostics should not run silently without authorization.

---

## Governance Model

Diagnostic commands are governed through the Strategic Mesh.

### Cognitive Engine
Defines the reasoning purpose and intellectual legitimacy of the diagnostic:
- which frameworks it uses
- what questions it asks
- what type of judgment it is meant to support

### Operational Control Layer / Support Stack
Controls runtime behavior:
- when diagnostics may be invoked
- how outputs are formatted
- whether the diagnostic can chain to another procedure
- whether the run is logged, throttled, or session-bound

### Security Enforcement Layer
Controls access and exposure:
- which roles may invoke which diagnostics
- whether the diagnostic can inspect restricted data
- whether internal state or debugging outputs are visible
- whether the diagnostic is tenant-safe and scoped correctly

This aligns with the repo rule that diagnostic invocation may require explicit invocation and may be limited to privileged operator roles.

---

## Diagnostic Command Lifecycle

A diagnostic command should move through a controlled lifecycle.

### 1. Definition
The command is defined as a governed evaluative procedure.

### 2. Registration
The command is added to a registry or equivalent runtime catalog with metadata.

### 3. Authorization
Invocation rules are attached:
- who can run it
- in what context
- against which data scopes
- whether automatic runtime invocation is allowed

### 4. Execution
The diagnostic procedure runs against the current situation, context bundle, and authorized knowledge set.

### 5. Artifact generation
The run produces a structured output, such as:
- executive summary
- scored or tiered assessment
- leverage map
- risks
- next actions
- confidence and sensitivity notes

### 6. Logging and review
The system records invocation metadata and, where appropriate, stores the resulting decision artifact.

### 7. Expiration or persistence
Some diagnostics are permanent and reusable.
Others are temporary and should expire after the relevant session or domain event.

---

## Runtime Flow Placement

In the seven-layer reasoning stack, diagnostic commands sit in the analytical procedure layer.

Canonical flow:

1. Interface Layer  
   Input arrives from operator or ambient signal

2. Context and Memory Layer  
   Relevant historical, tenant, and situational context is loaded

3. Detection and Framing Layer  
   The system identifies scenario, domain, urgency, and task type

4. Governance Layer  
   Prime Directive, Strategic Mesh constraints, and authorization are applied

5. Knowledge Layer  
   Relevant nuggets, cartridges, and supporting knowledge strata are activated

6. Analytical Procedure Layer  
   Diagnostic command executes the structured evaluation procedure

7. Decision and Action Layer  
   Structured guidance and a decision artifact are produced

This placement is essential.
Diagnostics do not replace knowledge activation or governance.
They operate after framing and under governance.

---

## Recommended Runtime Object Mapping

Diagnostic commands should map cleanly to the `Diagnostic` runtime object already defined in the runtime object model.

### Minimum object fields
- diagnostic_id
- name
- category
- invocation_phrase
- frameworks_used
- domain
- scope
- expiration
- status

### Recommended additional fields
- description
- allowed_roles
- invocation_mode
- input_requirements
- output_schema
- linked_scenarios
- linked_reflexes
- linked_cartridges
- session_bound
- tenant_scope
- audit_required
- internal_visibility_level

These additional fields will make future implementation safer and easier.

---

## Recommended Output Shape

A diagnostic command should produce a structured result instead of a loose narrative whenever possible.

Recommended output sections:
- diagnostic_name
- invocation_reason
- situation_summary
- evaluation_framework
- key findings
- risks or weaknesses
- strengths or advantages
- tradeoffs
- confidence
- sensitivity analysis
- next actions

Where needed, a diagnostic may also emit:
- scorecards
- ranked options
- leverage tiers
- red/yellow/green states
- unresolved questions
- escalation recommendations

---

## Relationship to Decision Artifacts

Diagnostic commands should usually terminate in a `DecisionArtifact` or feed one.

The goal is not merely to “run analysis.”
The goal is to create an executive-useful output that can be:
- reviewed
- compared
- audited
- persisted
- acted upon under governance

This creates the bridge between procedural reasoning and practical executive value.

---

## Design Rules

### 1. Diagnostics must stay procedural
Do not collapse diagnostics into generic prompts or static knowledge pages.

### 2. Diagnostics must stay governed
No unrestricted introspection, debugging, or hidden system-state exposure.

### 3. Diagnostics must stay scoped
A diagnostic should know its domain, role permissions, and data boundaries.

### 4. Diagnostics must stay distinguishable
Do not blur the line between reflexes, cartridges, nuggets, and diagnostics.

### 5. Diagnostics should be implementation-ready
Every major diagnostic should be specifiable as a runtime object and eventually executable by a service layer.

---

## Near-Term Implementation Guidance

The following implementation path is recommended:

### Phase 1: documentation hardening
Create full specifications for the initial diagnostic command family:
- Ten-Point Diagnostic
- Negotiation Leverage Diagnostic
- Strategic Position Diagnostic

### Phase 2: runtime scaffolding
Define a registry/interface for diagnostics inside runtime scaffolding.

Possible future concepts:
- diagnostic registry
- diagnostic executor
- diagnostic authorization check
- diagnostic artifact builder

### Phase 3: service integration
Bind diagnostic commands to:
- scenario detection
- reflex recommendations
- decision artifact persistence
- comparison workflows

### Phase 4: UI and operator surface
Expose diagnostics as deliberate operator tools, not hidden magic.

Examples:
- command palette
- structured evaluation menu
- scenario-aware recommendations
- post-analysis artifact review

---

## Non-Goals

This document does not define:
- the full internal logic of each individual diagnostic
- UI mockups
- persistence schema details
- automatic invocation policy for every future diagnostic

Those should be defined in subsequent implementation and product specs.

---

## Summary

Diagnostic commands are a core procedural mechanism inside Execalc.

They exist because executive-grade reasoning requires more than stored knowledge. It requires governed, repeatable analytical procedures.

A diagnostic command is:
- callable
- structured
- governed
- auditable
- domain-aware
- output-oriented

In runtime terms, diagnostics are the disciplined procedures that convert knowledge and context into structured evaluation.

They are one of the clearest ways Execalc becomes a strategic operating system rather than a simple chatbot.

# CARAT_REGISTRY_STANDARD.md

## Status
Draft v0.1

## Owner
Executive Knowledge Engine (EKE)

## Purpose
This document defines the minimum standard for representing, governing, and invoking **Carats** inside Execalc.

Carats are modular strategic overlays. Their role is to sharpen judgment within an already-classified situation. They do not replace scenario detection, they do not override governance, and they do not function as standalone decision engines.

This document exists so the Executive Knowledge Engine does not claim precision or runtime completeness that has not yet been formally specified.

## Working Definition
A **Carat** is a bounded packet of strategic logic that may be activated when a recognized scenario, context, or signal pattern calls for a specific strategic emphasis.

A Carat may influence:
- what gets emphasized
- what gets scrutinized
- what gets surfaced as leverage, risk, or opportunity
- what posture the system adopts during synthesis

A Carat may not independently produce final governed judgment.

## Runtime Position
Current intended runtime cascade:

`Scenario -> Activation Pathway -> Carats / Thinkers -> Prime Directive`

This means:
1. the situation must be classified first
2. the activation pathway must be selected
3. Carats may then be loaded as overlays
4. final judgment must still clear the Prime Directive
5. any action handoff remains subject to authority and execution boundaries

## Core Constraints
Carats are not scenarios.

Carats are not thinkers.

Carats are not memory objects.

Carats are not prompts.

Carats are not allowed to bypass the Prime Directive.

Carats are influence modules, not sovereign decision authorities.

## Minimum Carat Registry Object
Every Carat must be representable as a governed object with the following fields.

### Required Fields
- `carat_id`
- `name`
- `status`
- `purpose`
- `scope`
- `activation_criteria`
- `exclusions`
- `eligible_scenarios`
- `expected_influence`
- `governance_status`
- `version`

### Recommended Fields
- `polarity`
- `risk_posture`
- `priority`
- `linked_thinkers`
- `linked_heuristics`
- `evidence_requirements`
- `conflict_rules`
- `owner`
- `created_at`
- `updated_at`

## Field Definitions

### `carat_id`
Stable unique identifier for the Carat.

### `name`
Canonical name used across runtime, docs, and audit trails.

### `status`
Lifecycle state. Initial allowed values:
- `draft`
- `candidate`
- `approved`
- `deprecated`
- `retired`

### `purpose`
Plain-language statement of why the Carat exists and what strategic value it adds.

### `scope`
Defines the boundary of valid use. Scope must be narrow enough to prevent conceptual sprawl.

### `activation_criteria`
The conditions under which the Carat may be invoked. These may include scenario type, trigger signals, context structure, or governing objectives.

### `exclusions`
Conditions under which the Carat must not fire, even if partial activation signals are present.

### `eligible_scenarios`
List of scenario classes where the Carat is allowed to participate.

### `expected_influence`
Description of how the Carat should alter synthesis. This should describe influence, not outcome guarantees.

### `governance_status`
Statement of whether the Carat is fully governed, partially governed, or still awaiting supporting doctrine.

### `version`
Version string for auditability and controlled evolution.

## Activation Rule
A Carat may activate only after scenario classification or an equivalent governed routing step.

No Carat may self-activate purely from keyword presence.

Activation must be explainable in the audit trail.

At minimum, the runtime should be able to answer:
- why this Carat fired
- why it was eligible
- which scenario allowed it
- what influence it was expected to contribute

## Precedence Rule
Scenario classification outranks Carat activation.

Prime Directive evaluation outranks Carat influence.

Authority boundaries outrank any Carat recommendation related to execution.

If a Carat conflicts with the Prime Directive, the Prime Directive wins.

## Conflict Handling
If multiple Carats are eligible at once, the runtime must not silently blend them without control.

At minimum, the system must support:
- primary Carat designation
- secondary Carat designation
- suppression when two Carats meaningfully conflict
- audit visibility into which Carats were considered but not loaded

Until formal arbitration rules exist, conflicting Carats should default to conservative activation and explicit audit notation.

## Relationship to Thinkers
Thinkers and Carats are separate runtime classes.

Thinkers contribute perspective or judgment patterns associated with a source.

Carats contribute strategic overlays associated with a use-case emphasis.

A Thinker may inform a Carat.

A Carat may reference one or more Thinkers.

A Carat may not be treated as equivalent to a Thinker unless formally canonized as both classes under separate governance.

## Relationship to Memory
Carats are not stored memory claims.

However, a Carat invocation may generate memory candidates if the session produces governed signal worth preserving.

Carat usage itself should be auditable even when no memory is created.

## Audit Requirements
Every Carat invocation should be traceable.

Minimum audit fields:
- Carat selected
- version used
- triggering scenario
- triggering signals
- exclusions checked
- whether the Carat materially influenced the output

This is required so Carats remain governed overlays rather than invisible prompt behavior.

## Versioning Standard
Carats must be versioned.

A change to purpose, scope, activation criteria, exclusions, or expected influence should trigger a version update.

Deprecated Carats must remain historically readable in audit records even after retirement.

## Current Limitation
The following are not yet fully specified:
- canonical Carat list
- weighting model
- arbitration model
- test suite
- packaging standard beyond this starter registry
- runtime serialization contract

Accordingly, EKE may currently claim only that Carats are a governed strategic overlay class in draft form, not a fully mature runtime class with completed activation mechanics.

## Next Required Follow-On Specs
The following documents should follow this one:
1. `CARAT_ARBITRATION_RULES.md`
2. `CARAT_TESTING_DOCTRINE.md`
3. `CARAT_PACKAGE_TEMPLATE.md`
4. `CARAT_RUNTIME_SERIALIZATION.md`

## Initial Design Principle
Carats should make Execalc sharper, not noisier.

If a proposed Carat does not create a distinct, governable strategic influence, it should not exist as a Carat.

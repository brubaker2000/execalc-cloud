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

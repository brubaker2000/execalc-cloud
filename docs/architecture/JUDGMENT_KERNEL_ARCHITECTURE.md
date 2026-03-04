# Judgment Kernel Architecture

The Judgment Kernel is the deterministic orchestration layer that governs how Execalc reasons. The LLM produces language; the Kernel controls the decision process.

## Kernel Contract
Given (tenant_id, user_id, scenario input), the Kernel must:
- classify the situation (scenario routing)
- activate reflexes (instinct layer)
- select strategic overlays (carats)
- retrieve relevant nuggets (atomic logic units)
- evaluate through the Prime Directive
- emit a structured executive report envelope

## Deterministic Order of Operations
1. Ingress normalization
2. Scenario detection and routing
3. Reflex scan and activation
4. Overlay selection (carats)
5. Nugget retrieval and reasoning assembly
6. Prime Directive evaluation and constraints
7. Executive report generation
8. Decision journal envelope creation (optional persistence)

## Auditability Requirements
The Kernel must be able to record:
- which scenario was detected
- which reflexes fired (and why)
- which overlays were applied
- which nuggets were selected
- what assumptions were used
- confidence level and key sensitivities

## Model Independence
The Kernel logic must remain stable across LLM changes. The LLM is used for interpretation and explanation, not for deciding whether governance steps execute.

## Expected Output Shape (Minimum)
- executive_summary
- recommendation
- rationale
- key_risks
- alternatives
- confidence
- sensitivity
- next_actions

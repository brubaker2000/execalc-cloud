# Scenario Constructor

## Purpose
The Scenario Constructor converts raw operator input into a typed, governed, executable scenario object.

It is the bridge between:
- live chat / raw intake
- structured Execalc reasoning
- decision artifact generation

Without this layer, scenario activation is ad hoc.
With this layer, input becomes structured, governable, and executable.

---

## Definition

The Scenario Constructor is the system that determines:

1. what kind of situation is present
2. what signals are embedded in the input
3. what scenario type should be activated
4. what additional context is required
5. whether the scenario is draft, confirmed, or executing

It answers:
- What kind of situation is this?
- What logic path should fire?
- What data is still missing?

---

## Product Behavior

### 1. Passive Mode (Always On)
During normal chat, the system continuously evaluates operator input for situational structure.

Example:
- raw input: "Nick wants to change how public adjusters work with lenders"
- system detects:
  - market structure
  - incentive misalignment
  - business model redesign

The Scenario Constructor silently produces a draft scenario object.

This mode must be always on.

### 2. Active Mode (Operator-Triggered)
The operator may explicitly promote a discussion into a formal scenario.

Examples:
- "Turn this into a scenario"
- "Make this a decision"
- "Run this as a structured scenario"

In this case, the Scenario Constructor locks the scenario and requests or infers missing fields as needed.

### 3. Hybrid Mode (System Suggestion + Operator Confirmation)
The system may suggest likely scenario classifications when confidence is high enough.

Example:
- "This appears to be a Market Structure Opportunity scenario. Confirm?"

This mode reduces friction while preserving operator control.

---

## Design Rules

The Scenario Constructor must be:

- always on for passive detection
- user-overridable
- low-friction
- consistent across domains
- capable of inferring structure from messy input
- capable of remaining in draft state when confidence is incomplete

The operator must never be forced to manually structure every situation before reasoning can begin.

---

## Scenario Object (Conceptual Schema)

A scenario object should contain:

- scenario_id
- scenario_type
- confidence
- governing_objective
- prompt
- constraints
- detected_signals
- source_surface
- status
- created_at

### Example Conceptual Shape

```python
@dataclass
class Scenario:
    scenario_id: str
    scenario_type: str
    confidence: float
    governing_objective: Optional[str]
    prompt: str
    constraints: Dict[str, Any]
    detected_signals: List[str]
    source_surface: str
    status: Literal["draft", "confirmed", "executing"]
    created_at: datetime

```

---

## Core Runtime Flow

```text
Chat Input / Surface Input
        ↓
Scenario Constructor
        ↓
Scenario Object
        ↓
Decision Engine / Cognitive Engine
        ↓
Decision Artifact / Right-Rail Output
```

This layer sits between raw human input and governed system reasoning.

---

## Signal Detection Responsibilities

The Scenario Constructor must detect:

- deal activity
- incentive misalignment
- negotiation context
- capital allocation questions
- structural redesign opportunities
- crisis or fragility indicators
- planning or sequencing needs
- operator-signaled importance

Signal detection may begin with simple deterministic heuristics and evolve later into richer classification logic.

---

## Classification Responsibilities

Based on detected signals, the Scenario Constructor assigns a scenario type.

Illustrative examples:

- deal_origination
- market_structure
- negotiation
- crisis_management
- planning
- capital_stack
- strategic_drift
- execution_infrastructure

This classification controls what downstream logic paths may activate.

---

## Status Model

Scenario status should progress through:

### draft
A scenario has been inferred but not fully confirmed.

### confirmed
The scenario has enough confidence and structure to be treated as active.

### executing
The scenario is actively being run through a reasoning or decision pathway.

This preserves operator control while allowing passive intelligence.

---

## Why This Matters

The Scenario Constructor is the system's understanding layer.

If the Real-Time Decision Artifact Engine is what the operator sees, the Scenario Constructor is what the system understands.

It is the entry point for:
- scenario-driven reasoning
- governed activation
- consistent decision artifact generation
- future multi-surface intelligence behavior

---

## Future Extensions (Stubbed)

- confidence scoring refinement
- multi-signal weighting
- scenario conflict detection
- multi-objective scenario construction
- integration with right-rail artifact generation
- scenario versioning across chat history
- tenant-specific scenario dictionaries
- cartridge-triggered scenario enrichment

---

## Canonical Principle

Execalc does not merely respond to prompts.

Execalc recognizes situations and activates governed logic paths.

The Scenario Constructor is the system component that makes this possible.

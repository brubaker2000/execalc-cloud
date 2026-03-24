# Executive Rail Workspace Spec

Status: Proposed product architecture note  
Purpose: Canonize the intended Execalc workspace layout and define the Executive Rail as a separate operator surface driven by governed runtime state.

---

## Why this note exists

The current product notes already establish that:

- chat is the primary workbench surface for operator interaction
- orchestration runtime is the source of truth
- the Executive Rail is a display surface fed by governed runtime state

What is not yet written explicitly is the fuller workspace concept:

- project and chat navigation on the left
- active chat in the center
- a dedicated Executive Rail on the right
- one rail per active chat
- the rail composed of atomic nuggets and governed state rather than loose prose summary

This note canonizes that product shape.

---

## Canonical workspace layout

The intended Execalc workspace is a three-pane layout:

### 1. Left pane — Project and chat navigation
The left pane is the organizational index.

It should eventually allow the operator to:
- select a project
- see the chats inside that project
- move across active threads
- return to prior work without losing context

This pane is for navigation and organization, not runtime authority.

### 2. Center pane — Active chat
The center pane is the live conversational work surface.

This is where the operator:
- thinks out loud
- frames problems
- asks for judgment
- evaluates options
- requests plans
- pressures assumptions
- reviews decision artifacts
- initiates action-oriented work

The chat remains natural-language first, but the runtime beneath it remains governed.

### 3. Right pane — Executive Rail
The right pane is the Executive Rail.

The rail is a separate surface from chat.
It is tied to the currently active chat and shows the governed state of that chat in compact form.

The rail is not the source of truth.
It is a window into runtime truth.

---

## One rail per chat

Every active chat should have its own rail.

Why:
- each chat has its own governing objective
- each chat may have different constraints
- each chat may have a different decision path
- each chat may contain distinct action proposals, warnings, and open loops

The rail is therefore chat-specific, not generic.

At the project level, a later project-wide rail may also exist, but that is separate from the per-chat rail defined here.

---

## What the Executive Rail is for

The Executive Rail exists to give the operator fast access to the durable strategic atoms of the conversation without rereading the entire chat.

Its job is to surface:
- current objective
- key constraints
- decisions made
- important facts
- unresolved issues
- action proposals
- review state
- warnings
- next likely move

It should function as an operator instrument panel, not a decorative summary.

---

## The rail should not be a prose blob

A weak rail would merely paraphrase the chat in narrative form.

A strong rail should be composed of atomic nuggets and governed state objects.

This means the rail should prefer compact, typed units such as:
- objective nugget
- constraint nugget
- decision nugget
- fact nugget
- proposal nugget
- warning nugget
- evidence nugget
- open-loop nugget

These are not yet fully implemented as typed runtime objects in the UI, but this note establishes the intended direction.

---

## Rail layering model

The rail should be structured into layers rather than presented as a single undifferentiated summary.

### Top layer — Current state
Shows the immediate state of the active chat, such as:
- governing objective
- active mode
- current decision state
- latest boundary or review state

### Middle layer — Atomic nuggets
Shows the durable strategic atoms extracted from the conversation, such as:
- key decisions
- constraints
- facts
- assumptions
- evidence handles
- major insights

### Bottom layer — Operational next steps
Shows what is still in motion, such as:
- pending proposals
- review items
- warnings
- anomalies
- open loops
- next likely move

---

## Canonical authority rule

The workspace must obey this rule:

- chat is the interaction surface
- rail is the visibility surface
- runtime is the authority surface

This means:
- the chat does not become the system of record
- the rail does not become the system of record
- the runtime remains the source of truth
- the rail reflects governed runtime state for operator use

---

## Runtime relationship

The intended flow is:

`Operator input -> Chat surface -> Orchestration/runtime -> State payload + response text + rail-ready updates -> Executive Rail`

This means:
- the runtime leads
- the rail reflects
- the chat delivers

The rail must not invent state that the runtime has not produced.

---

## Product implications

The Executive Rail is important because it may eventually become the main place where the operator sees:
- state compression
- signal surfacing
- runtime warnings
- action readiness
- cross-turn continuity

This makes the rail one of the most important operator-facing surfaces in the future product, even though it is not the authority layer.

---

## Non-goals for this note

This note does not yet define:
- final UI styling
- final nugget schemas
- project-wide rail behavior
- persistence implementation details
- notification logic
- exact React component structure

Its purpose is to canonize the workspace concept and the intended role of the Executive Rail.

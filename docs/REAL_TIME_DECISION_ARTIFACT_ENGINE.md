# Real-Time Decision Artifact Engine (RDAE)

## Purpose
The Real-Time Decision Artifact Engine (RDAE) continuously converts live conversational input into structured, operator-grade decision artifacts displayed in a right-hand rail alongside the chat interface.

This system exists to:
- collapse cognitive load
- preserve high-value signal
- provide real-time executive awareness
- eliminate the need to manually summarize long conversations
- convert live thinking into durable, reusable knowledge assets

RDAE is not a summary tool.
It is a continuous synthesis layer attached to live cognition.

---

## Core Role

RDAE functions as:

- a live executive brief
- a decision memory layer
- a heuristic capture mechanism
- a cognitive acceleration tool
- a real-time review surface for the active conversation

It is not optional UI polish.
It is a core Execalc intelligence layer.

---

## Core Behavior

RDAE operates continuously during a chat session and produces structured artifacts consisting of:

1. Core Thesis
2. Executive Brief
3. Key Insights (ranked)
4. Decision Signal

Artifacts are:

- continuously updated as the conversation evolves
- displayed in the right-hand rail
- readable in a few minutes, not seconds or dozens of minutes
- structured enough to sharpen operator thinking
- compressed enough to eliminate the need to scroll back through the chat
- persisted as structured records, not raw text blobs

---

## Product Behavior

### 1. Continuous Executive Layer
As a conversation unfolds, RDAE maintains a parallel executive layer.

The operator is not just looking at:
- the live chat

The operator is also looking at:
- the continuously updated executive understanding of that chat

This creates two streams:

1. Conversation Stream
   - raw exploration
   - iterative thinking
   - noise and signal mixed together

2. Executive Stream
   - distilled signal
   - active conclusions
   - important unresolved issues
   - reusable strategic insight

### 2. Real-Time Updating
RDAE must:

- revise the executive brief as the conversation evolves
- promote stronger insight when the conversation sharpens
- downgrade or remove outdated conclusions
- avoid stacking contradictory versions when the current state has changed

The right rail must feel alive, not static.

### 3. Hybrid Capture Model
RDAE uses both automatic and operator-directed capture.

#### Automatic Capture
The system automatically promotes content into the artifact layer when it detects:
- decisions
- structural insights
- strategic models
- durable heuristics
- repeated or reinforced high-signal conclusions

#### Operator Override
The operator may explicitly force capture with commands like:
- "save that"
- "that's important"
- "capture this"
- "note that"
- "the point about X, save that"

Operator override is authoritative.
If the operator flags it, it must be captured.

---

## Output Format

The right-rail artifact should not be ultra-compressed bullet noise.
It should also not be a long-form memo.

The correct balance is:
- enough detail to think
- not enough detail to slow the operator down

### Required Sections

#### Core Thesis
A 1–2 line statement of the central idea or governing conclusion.

#### Executive Brief
A short narrative synthesis that orients the operator quickly.
This should explain:
- what has emerged
- why it matters
- where the conversation now stands

#### Key Insights
A ranked list of the most important non-trivial takeaways.
These are not generic notes.
They are the points most likely to matter later.

#### Decision Signal
A concise judgment about the state of the idea, decision, or discussion.

Examples:
- structurally sound, execution risk high
- high-potential, needs validation
- strategically correct, operationally incomplete
- not yet ready for commitment

---

## Output Constraints

Artifacts must:

- be readable in approximately 2–3 minutes
- be more detailed than a bullet summary
- be more compressed than a formal memo
- support active reasoning during the chat
- preserve the causal logic of the discussion
- remain structured and domain-agnostic

The right rail should help the operator think faster while the conversation is still happening.

---

## What Qualifies for Capture

### Tier 1 — Must Capture Automatically
These should always be promoted:

- decisions
- structural insights
- models / frameworks
- durable heuristics
- operator-declared key points

### Tier 2 — High-Confidence Capture
These may be promoted automatically when confidence is sufficient:

- strategic nuggets
- causal observations
- reusable formulations
- stakeholder / incentive mappings
- important unresolved tensions

### Tier 3 — Optional / Lower-Priority
These may remain in chat unless reinforced:

- tactical notes
- partial thoughts
- undeveloped lines of inquiry
- speculative side branches

The system should prefer:
- missing some signal
over
- flooding the right rail with junk

Accuracy is more important than frequency.

---

## Relationship to Other System Components

### Scenario Constructor
The Scenario Constructor is what the system understands.
RDAE is what the operator sees.

Flow:

Chat Input
→ Scenario Constructor
→ Decision / Reasoning Engine
→ RDAE Output
→ Right-Hand Rail

### Decision Journal / Comparative Memory
RDAE is the live synthesis layer during the conversation.
The Decision Journal is the durable archive across conversations.

### Heuristic Capture
When a point is durable enough to become a heuristic, RDAE may surface it and route it into heuristic storage logic.

---

## System Value

RDAE exists to solve the chat entropy problem.

In ordinary chat systems:
- signal decays over time
- important ideas are buried under later output
- the operator must scroll and reconstruct what mattered

In Execalc with RDAE:
- high-value signal is continuously harvested
- the conversation is reviewed while it is still happening
- the operator can think with the summary, not after it
- value compounds instead of decays

This is not just summarization.
It is real-time cognitive compression and preservation.

---

## Canonical Principle

Chats are where thinking happens.
Artifacts are where thinking becomes durable.

RDAE ensures that valuable thinking does not disappear into scrollback.
It converts live cognition into structured, reviewable, reusable executive artifacts in real time.

Execalc should not require the operator to ask, "summarize this chat."
The right-hand rail should already be performing that function continuously at a higher level.

---

## Future Extensions (Stubbed)

- artifact version history within a single chat
- comparison of right-rail artifacts across chats
- promotion from right-rail artifact to formal memo / report
- confidence scoring for auto-captured insights
- artifact tagging by domain, scenario, and strategic role
- tenant-aware persistence and retrieval
- export to decision journal / board memo / CRM notes
- user-tunable capture aggressiveness
- collapse / expand narrative vs structured sections

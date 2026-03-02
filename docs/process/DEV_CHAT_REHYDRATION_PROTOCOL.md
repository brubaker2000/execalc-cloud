# Dev Chat Rehydration Protocol (Copy/Paste Standard)

Purpose:
- Ensure every new dev chat rehydrates instantly with zero drift.
- Keep speed high by moving “truth” into the repo and using chat only for execution.
- Prevent lost context when tokenization or latency rises.

Status:
- Active operating protocol.
- Applies to every dev chat and every handoff.

---

## A) Trigger: When to start a new dev chat
Start a new dev chat when any of the following occur:
- Responses become slow or token-heavy.
- Context is getting messy or fragmented.
- We are switching from Q&A mode back to build mode after long discussion.
- We need a clean runway for a new stage or a major change set.

---

## B) Rehydration Inputs (What the new dev chat must read first)
In the new dev chat, the assistant must begin by using the repo as source of truth and rehydrate from:

1) Stage map (canonical)
- docs/vision/STAGE_MAP.md

2) Daily execution spine
- docs/NEXT_ACTIONS.md

3) Invariants (non-negotiables)
- docs/EXECALC_INVARIANTS.md
- docs/invariants/INV-001_ai_is_subroutine.md

4) Customer experience contract (anti-drift)
- docs/product/EXECALC_CUSTOMER_EXPERIENCE_CHARTER.md

5) Editor-only development protocol
- docs/EDITOR_ONLY_DEV_PROTOCOL.md

6) Governance upgrade register (design-locked, deferred enforcement)
- docs/governance/FUTURE_GOVERNANCE_EXPANSIONS.md
- docs/governance/STAGE_SLOT_MAP_GOVERNANCE_UPGRADES.md

---

## C) First Message Template (What the operator says in the new dev chat)
Copy/paste this into the new dev chat:

“Rehydrate from repo canon. Read:
- docs/vision/STAGE_MAP.md
- docs/NEXT_ACTIONS.md
- docs/EXECALC_INVARIANTS.md
- docs/invariants/INV-001_ai_is_subroutine.md
- docs/product/EXECALC_CUSTOMER_EXPERIENCE_CHARTER.md
- docs/EDITOR_ONLY_DEV_PROTOCOL.md

Then tell me:
1) Where we are (stage + current objective)
2) The next 3 actions (copy/paste terminal commands)
3) Any open risks or drift concerns.”

---

## D) Execution Rules (How the new dev chat must operate)
- The repo is authoritative. Chat is not authoritative.
- One command at a time. The operator only copy/pastes.
- No assumptions about GitHub UI or tooling knowledge; give exact navigation steps.
- No stage skipping.
- Governance before intelligence.
- If a decision is made in chat, it becomes a repo artifact the same day.

---

## E) Handoff Rule (How to close a dev chat)
Before switching chats, the assistant must produce a short handoff containing:
- Current branch name
- Current objective
- Last successful check/run
- Next command to run
- Any unresolved blockers


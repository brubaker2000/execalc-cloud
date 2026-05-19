# Right Rail Capture UX Specification

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-19  
**Authority:** Execalc Product Standards

---

## I. Purpose

This document defines the visual treatment, card types, interaction behaviors, and display rules for the Qualitative Capture right rail — the live signal surface of the Execalc workspace.

For the pipeline that feeds the rail, see `docs/product/QUALITATIVE_CAPTURE_RUNTIME_SPEC.md`.  
For the workspace layout context, see `docs/product/EXECUTIVE_RAIL_WORKSPACE_SPEC.md`.

---

## II. Governing UX Principles

**The rail is for reading. Metadata is for audit.**

Every card must expose one clean conclusion by default. Supporting evidence, source anchors, provenance, and classification live behind the card — accessible on demand, never displayed by default.

**The rail is not a summary panel.** It is a live instrument surface fed by governed runtime state. It does not paraphrase the chat. It surfaces durable signal extracted from it.

**Memorialized items are visually distinct from auto-extracted items at a glance.** An operator scrolling the rail should distinguish human judgment from system detection without reading metadata.

**Card density should not overload.** The rail is not a transcript. If more than 12 cards are visible at once without operator action, the system should offer automatic grouping or archiving of lower-priority cards.

---

## III. Rail Card Types

Eight canonical rail card types are defined. Every card displayed on the right rail is exactly one of these types.

| # | Card Type | Source | What it surfaces |
|---|---|---|---|
| 1 | **Executive Conclusion** | Auto-extracted | Highest-signal reconstruction across recent nuggets |
| 2 | **Preserved Idea** | Human-memorialized | Operator-recognized exceptional language |
| 3 | **Risk** | Auto-extracted | Active cautionary or negative signal |
| 4 | **Opportunity** | Auto-extracted | Time-sensitive external positive signal |
| 5 | **Contradiction** | Auto-extracted | Conflict between a current claim and a corpus claim |
| 6 | **Open Question** | Auto-extracted or human | Unresolved issue requiring future attention |
| 7 | **Promotion Candidate** | System-nominated or human | Conclusion nominated for Canon elevation |
| 8 | **Doctrine Update** | Auto-extracted or human | Statement that should update or extend an existing doctrine |

These eight types are the closed set for V1. New types require a product spec revision.

---

## IV. Card Anatomy

Every card has two states: **collapsed** (default) and **expanded** (operator-triggered).

### Collapsed State

```
┌─────────────────────────────────────────┐
│ [TYPE BADGE]          [ACTION ICONS]    │
│                                         │
│ Card conclusion text — clean, one or    │
│ two sentences maximum.                  │
│                                         │
│ [timestamp]              [expand ›]     │
└─────────────────────────────────────────┘
```

- Type badge: small colored label in upper left (see Section V for colors)
- Action icons: Preserve / Pin / Dismiss / Route / Promote (see Section VI)
- Card text: the conclusion only — no metadata visible
- Timestamp: when the card was generated
- Expand control: opens the expanded state

### Expanded State

```
┌─────────────────────────────────────────┐
│ [TYPE BADGE]          [ACTION ICONS]    │
│                                         │
│ Card conclusion text — clean, one or    │
│ two sentences maximum.                  │
│                                         │
│ ─ Supporting Claims ──────────────────  │
│ • [claim 1 — abbreviated]               │
│ • [claim 2 — abbreviated]               │
│                                         │
│ ─ Provenance ─────────────────────────  │
│ Source: [session / document anchor]     │
│ Type: [GAQP claim type]                 │
│ Confidence: [score + label]             │
│ Durability: [class]                     │
│ Generated: [timestamp]                  │
│                                         │
│ [collapse ‹]                [audit →]  │
└─────────────────────────────────────────┘
```

The audit link opens the full audit object — all metadata fields, generation lineage, activation history.

---

## V. Visual Treatment

### Type Badge Colors

| Card Type | Badge Color | Rationale |
|---|---|---|
| Executive Conclusion | Blue | Primary intelligence output |
| Preserved Idea | Gold / Amber | Human-validated; highest provenance |
| Risk | Orange-Red | Cautionary; demands attention |
| Opportunity | Green | Positive; action-loading |
| Contradiction | Red | Alert; conflicts existing corpus |
| Open Question | Grey-Blue | Unresolved; neutral urgency |
| Promotion Candidate | Purple | Elevated; Canon-adjacent |
| Doctrine Update | Deep Blue | Governing; authoritative |

### Memorialized vs. Auto-Extracted

Every card that originated from a human Memorialize action receives:

- A gold left border (full height of the card)
- A small human-origin icon in the type badge area
- Visual position above auto-extracted cards of the same type and domain

This treatment is permanent — it cannot be removed by the system, only by the operator who created it.

### Rail Density States

| Card count | Rail behavior |
|---|---|
| 1–6 | Full cards displayed |
| 7–12 | Full cards displayed; scroll enabled |
| 13+ | System offers to group lower-priority cards by type into collapsed stacks |

---

## VI. Operator Actions

Five actions are available on every card.

| Action | Icon position | Behavior |
|---|---|---|
| **Preserve** | Top right | Elevates an auto-extracted card to memorialized status. Fires the full Memorialize pipeline (confidence → Strong, durability → Enduring, bypass sliders, promote to corporate pool). Not available on cards already memorialized. |
| **Pin** | Top right | Anchors the card to the top of the rail regardless of new content or re-ranking. Pinned cards have a pin icon indicator. Maximum 3 pinned cards. |
| **Dismiss** | Top right | Removes the card from the rail view. Does NOT delete the underlying object from the corpus. The nugget and rail artifact remain; only the rail projection is cleared. |
| **Route** | Top right | Opens a routing panel: send to a named user, project, or decision artifact. Creates a linked reference in the destination. |
| **Promote** | Top right | Nominates the card's underlying conclusion for Canon elevation. Creates a `promotion_candidate` record. Requires explicit human confirmation before any doctrine is updated. |

The action icons are compact (icon-only, no labels). Tooltips appear on hover. No action is irreversible without confirmation — Promote shows a confirmation dialog.

---

## VII. Rail Display Order

Within the rail, cards are ordered by the following priority hierarchy:

1. Pinned cards (operator-pinned, in pin order)
2. Preserved Ideas (human-memorialized, newest first)
3. Contradictions (always surfaces immediately — cannot be buried)
4. Promotion Candidates
5. Executive Conclusions (ranked by reconstruction confidence score, descending)
6. Risks (ranked by assessed severity)
7. Opportunities (ranked by time sensitivity)
8. Doctrine Updates
9. Open Questions (oldest unresolved first)

This ordering is the default. Operators may filter the rail by type using a type filter control at the top of the rail pane.

---

## VIII. Rail Filter Controls

At the top of the right rail pane, a compact filter bar allows the operator to show/hide card types without dismissing them.

```
[All] [Conclusions] [Preserved] [Risks] [Opportunities] [Contradictions] [Questions]
```

Filter state is per-chat, not global. Switching chats resets to [All].

---

## IX. Empty Rail State

When no cards have been generated in the current chat:

```
┌─────────────────────────────────────────┐
│                                         │
│   No signal captured yet.               │
│                                         │
│   The rail will populate as the         │
│   conversation produces governed        │
│   qualitative signal.                   │
│                                         │
│   To capture something immediately,     │
│   select text and right-click →         │
│   Memorialize.                          │
│                                         │
└─────────────────────────────────────────┘
```

No spinner, no animation. Static, instructional, minimal.

---

## X. Relationship to Memorialize and Nugget Trigger

The right-click → Memorialize action and the "Nugget" keyboard trigger both produce Preserved Idea cards on the rail. The card appears within one second of the operator action. Visual confirmation is the card appearing — no toast, no modal, no separate confirmation step.

See `docs/product/EXECALC_MEMORIALIZE_SPEC.md` for the full Memorialize pipeline.  
See `docs/product/EXECALC_NUGGET_CAPTURE_SYSTEM.md` for the keyboard trigger.

---

## XI. Not in Scope for V1

The following are excluded from this specification and require separate design work:

- Project-wide rail (aggregates signal across multiple chats)
- Cross-tenant synthesis view
- Rail export or sharing
- Rail card commenting or annotation
- Notification or alert behaviors triggered by rail events
- Mobile or narrow-viewport rail treatment

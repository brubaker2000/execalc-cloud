# Execalc Memorialize Feature Specification

**Status:** Canonized
**Version:** 1.0
**Date:** 2026-05-02
**Authority:** Execalc Product Standards

---

## I. Purpose

The Memorialize feature solves the most acute information-loss problem in governed AI conversations: valuable language — a precisely stated insight, a perfectly articulated principle, a clarity that has never been expressed that cleanly before — appears in the middle of a conversation and disappears into scroll within minutes.

The conversation generates at an estimated 44:1 noise-to-signal ratio. The Memorialize feature is the human-operated capture mechanism for the signal the user recognizes in real time.

---

## II. The Problem It Solves

In a normal conversation workflow:

```
Conversation generates exceptional language
  → User recognizes value
  → Conversation continues
  → Language disappears into scroll
  → Ten minutes later: fifty pages back
  → Signal lost
```

Auto-extraction running on the executive rail captures what the system identifies as governed claims. Memorialize captures what the human recognizes as exceptional. These are complementary mechanisms operating at different levels of judgment. Neither replaces the other.

---

## III. The Interaction

**Trigger:** User selects text in the chat panel (any portion of any message) and right-clicks.

**Context menu:** Two options only — **Memorialize** and **Copy**. No other options. The two-option constraint preserves the two-second guarantee: the time between "I see it" and "it is preserved forever" must not exceed a single deliberate click.

**On Memorialize:**
- Selected text is immediately added to the executive rail with visual distinction from auto-extracted nuggets
- GAQP classification runs in the background (claim type assigned from the 24 canonical types)
- Full metadata schema populated at ingress
- Nugget is stored with `selection_method: human_memorialized`
- Corporate pool promotion fires immediately — bypassing Knowledge Policy sliders
- User sees confirmation on the rail within one second

---

## IV. GAQP Classification

A memorialized nugget maps to exactly one of the 24 canonical GAQP claim types. Memoralization does not create a new category outside the taxonomy — it creates a distinct provenance class within it.

Examples:
- A precisely stated cause-effect relationship → **Causal Claim**
- An institutional truth articulated for the first time → **Doctrine**
- A decision shortcut too good to lose → **Heuristic**
- A tipping point stated with rare precision → **Threshold Condition**
- A competitive capability confirmed → **Strength**
- A time-sensitive external value window → **Opportunity**

The claim type tells the system what it is. The provenance tells the system how to treat it.

---

## V. Weight and Priority Rules

Memoralization is a human governance act. The system treats it accordingly — not by preserving the nugget, but by **prioritizing** it.

| Property | Auto-Extracted Nugget | Memorialized Nugget |
|---|---|---|
| Confidence at entry | Seed (0.50) | Strong (0.91) |
| Durability | Assigned by type | Always Enduring |
| Promotion | Subject to Knowledge Policy sliders | Bypasses sliders — always promotes |
| Retention | Subject to expiry/purge policy | Perpetual — never expires, never purged |
| Retrieval priority | Standard | Surfaces before auto-extracted claims of same type/domain |
| Rail display | Standard queue | Visual priority above auto-extracted signal |
| Synthesis weight | Standard | Higher weight in decision artifact construction |
| Search ranking | Standard | Ranks above auto-extracted at same confidence/domain |

**The system's posture toward a memorialized nugget:** *"A human recognized this as important — make sure it gets seen when it is relevant."* Not passive preservation. Active prioritization.

---

## VI. Second Memoralization Rule

If a second user in the same organization independently memorializes the same or closely related language, the system detects the corroboration and promotes the nugget to Structural confidence (1.00) automatically.

Two independent humans in the same organization stopping to preserve the same idea is not coincidence. It is institutional recognition. The system treats it as such.

---

## VII. Corporate Pool Contribution

Every memorialized nugget flows immediately to the corporate knowledge pool under the organization's tenant namespace. This is not subject to the Knowledge Policy slider configuration — the human has already made the governance decision. The sliders govern automated extraction. They have no authority over deliberate human acts.

The aggregate of all memorialized nuggets across all users in an organization is the highest-quality knowledge corpus the organization can produce:

- Every item was individually validated by a human present in the moment
- Every item was recognized as exceptional, not merely extractable
- Every item carries full GAQP classification, metadata, and provenance
- Every item is permanent

This is human-curated, governed, institutional memory at scale. Auto-extraction is the floor. The memorialized corpus is the ceiling.

---

## VIII. Visual Treatment

Memorialized nuggets must be visually distinct from auto-extracted nuggets on the executive rail. The distinction communicates provenance at a glance:

- A distinct color treatment or border indicating human origin
- A small icon indicating memoralization source
- Position: above auto-extracted nuggets of the same type and domain in the rail display

The visual system should allow a user scrolling the rail to immediately distinguish human judgment from system detection without reading the metadata.

---

## IX. Keyboard Complement

The right-click Memorialize interaction is the mouse-native path. A keyboard-native complement exists via the "Nugget" trigger word in the chat input (see `docs/product/EXECALC_NUGGET_CAPTURE_SYSTEM.md`). Both feed the same pipeline. The trigger word is faster; the right-click is more precise. An executive will use both without thinking about it.

---

## X. Relationship to the 44:1 Ratio

The 44:1 noise-to-signal compression ratio (observed working benchmark, pending formal validation) is the structural problem the entire GAQP system addresses. The Memoralize feature is the human-operated expression of that same problem: in a ten-minute governed conversation generating fifty pages of text, the user recognizes perhaps two or three sentences of exceptional value. Without Memoralize, those sentences are lost to scroll. With it, they are permanent within two seconds of recognition.

The Memoralize feature is not a convenience. It is the capture mechanism for the signal that makes the 44:1 ratio actionable at the human level.

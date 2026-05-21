# GAQP Temporal Decay Rules

**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

---

## I. Purpose

Not all claims remain valid indefinitely. A market thesis from 2022 may be wrong in 2026. A regulatory constraint may have been repealed. A competitive advantage may have eroded. The temporal decay system governs when claims should be reviewed, flagged, or expired — and what triggers those transitions.

Temporal decay is not automatic deletion. It is a governed review process. Claims are not removed from the corpus; they are reclassified and flagged. The historical record is preserved. The activation status is updated.

---

## II. The Durability Class and Its Implications

Every GAQP claim carries a `durability_class`. This field is set at admission and governs the default decay timeline.

| Durability Class | Default Review Trigger | Action if Not Renewed |
|---|---|---|
| `enduring` | Explicit operator retraction or contradiction only | Remains active indefinitely |
| `medium_term` | 12 months after creation, or on a named event | Flagged for review; activation suspended pending decision |
| `ephemeral` | `expires_at` timestamp (required) | Automatically archived at expiry |

**Enduring claims do not decay on a schedule.** They are only retired through operator action or when a `supersedes` relationship is committed by an authorized actor. A claim cannot decay from `enduring` to `medium_term` automatically — only a canon revision can change the durability class.

---

## III. Freshness Class and Its Relationship to Decay

The `freshness_class` field modifies how the claim is treated during retrieval, independent of the durability class.

| Freshness Class | Retrieval behavior |
|---|---|
| `timeless` | No staleness signal — always retrieved at full weight |
| `date_sensitive` | A staleness warning is surfaced if the claim is older than 90 days without corroboration |
| `event_bound` | Staleness warning surfaces immediately after the bound event resolves |
| `expiring` | Retrieval weight decreases linearly as `expires_at` approaches; claim is archived at expiry |

A claim may be `durability_class: enduring` and `freshness_class: date_sensitive`. This is the correct classification for a claim that should be retained permanently but should be reviewed periodically to confirm it still reflects current conditions.

---

## IV. Decay Triggers

The following events trigger a decay review notification:

| Trigger | Affected claims |
|---|---|
| **Time trigger** | `medium_term` claims older than 12 months; `date_sensitive` claims without corroboration in 90 days |
| **Event resolution** | `event_bound` claims where the named event has resolved |
| **Contradiction admission** | Any claim that receives a `contradicts` link from a newly admitted claim |
| **Confidence downgrade** | If a `corroborates` source is retracted, the corroboration count decreases and confidence may drop |
| **Supersession** | A `supersedes` link is committed — the superseded claim is archived |
| **Canon revision** | A GAQP canon revision changes a claim type's definition — existing claims of that type are flagged for reclassification |

---

## V. Decay Review Outcomes

When a claim enters decay review, an authorized operator must choose one of four outcomes:

| Outcome | Effect |
|---|---|
| **Renew** | Durability class confirmed; review timer resets; no other changes |
| **Reclassify** | Durability class or freshness class updated to reflect current understanding |
| **Supersede** | A new claim replaces this one; the old claim is archived with a `supersedes` link |
| **Retire** | The claim is archived without replacement; marked `activation_state: reference_only` |

Decay review is not a deletion decision. It is a classification decision. The corpus record is permanent. The activation state reflects current validity.

---

## VI. Activation State and Decay

The `activation_state` field in PEM memory objects and the `admission_status` field in GAQP claims together govern whether a claim is surfaced in live reasoning:

| State | Retrieval behavior |
|---|---|
| `active` / `admitted` | Surfaces normally |
| `deferred` | Held; not surfaced unless explicitly requested |
| `reference_only` | Surfaced only in full-corpus audits; not in live reasoning |
| `archived` (soft-delete) | Not surfaced in any context; history preserved |

A claim that fails decay review without a renewal decision transitions to `deferred`. An operator must explicitly archive or retire it. The system does not auto-delete.

---

## VII. The Canon Exception

Claims at structural confidence (1.00) that have been elevated to Canon are exempt from automatic decay triggers. Canon claims are governed by the Canon Revision Process (`GAQP_FOUNDING_CHARTER.md`), which requires explicit human authorization to modify. A Canon claim cannot be flagged for decay by the automated system — only by an authorized canon revision proposal.

---

## VIII. Governing Rule

> Temporal decay is not entropy. It is a governed review discipline. The corpus grows richer by retiring obsolete claims cleanly — not by pretending everything in it is still current. An unreviewed corpus is a misleading corpus.

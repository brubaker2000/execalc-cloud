# GAQP Corpus Object Contract

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-19  
**Authority:** Execalc Product Standards

---

## I. Purpose

This document defines the full object contracts for all nine database objects that implement the Qualitative Capture pipeline. Each object maps to a specific intelligence tier and must not be collapsed with others.

For the pipeline architecture that uses these objects, see `docs/product/QUALITATIVE_CAPTURE_RUNTIME_SPEC.md`.  
For the atomic nugget metadata schema, see `docs/gaqp/GAQP_METADATA_SCHEMA.md`.  
For the rail card visual spec, see `docs/product/RIGHT_RAIL_CAPTURE_UX_SPEC.md`.

---

## II. Tier Map

| Object | Tier | Role |
|---|---|---|
| `conversation_events` | 0 — Raw archive | Every message event, untouched |
| `atomic_nuggets` | 1–2 — Captured + Structured | GAQP-classified claims |
| `preserved_ideas` | 1–2 — Captured + Structured | Human-memorialized items |
| `executive_conclusions` | 3 — Executive | Reconstructed operator-facing intelligence |
| `right_rail_cards` | 3 — Executive | Rail display projection |
| `rail_artifacts` | 3 — Executive | Persisted rail cards (first-class objects) |
| `promotion_candidates` | 3→4 — Candidate | Doctrine elevation nominees |
| `runtime_activations` | 2–3 — Activation log | Nugget firing records |
| `audit_events` | All | Full audit trail |

**Architectural constraint:** These nine objects are the implementation of nine distinct concerns. No two should share a table. No field from one object should appear in another except as a foreign key reference.

---

## III. Object Contracts

---

### 1. `conversation_events`

The raw archive. Stores every message event from every chat session. This table is the Tier 0 source of truth. Nothing is ever deleted from it.

| Field | Type | Required | Description |
|---|---|---|---|
| `event_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace — strict isolation |
| `session_id` | UUID | Yes | The chat session this event belongs to |
| `user_id` | UUID | Yes | The user who sent the message |
| `role` | enum | Yes | `operator` / `system` / `agent` |
| `message_text` | text | Yes | Full message content, unmodified |
| `token_count` | integer | No | Approximate token count of the message |
| `created_at` | timestamptz | Yes | Wall-clock time of the event |
| `capture_queued_at` | timestamptz | No | When the event entered the capture queue |
| `capture_completed_at` | timestamptz | No | When deconstruction finished for this event |
| `metadata` | jsonb | No | Arbitrary structured metadata; not indexed by default |

**Retention:** Perpetual. No purge policy. This is the archive.  
**Indexes:** `(tenant_id, session_id)`, `(tenant_id, created_at)`

---

### 2. `atomic_nuggets`

The primary GAQP corpus object. Every machine-extracted or keyboard-triggered claim lives here. The full metadata schema from `docs/gaqp/GAQP_METADATA_SCHEMA.md` applies. This table extends that schema with pipeline-specific fields.

| Field | Type | Required | Description |
|---|---|---|---|
| `nugget_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `session_id` | UUID | Yes | Source session |
| `source_event_id` | UUID | Yes | FK → `conversation_events.event_id` |
| `claim_text` | text | Yes | The self-contained claim statement |
| `claim_type` | enum | Yes | One of the 24 canonical GAQP types |
| `domain` | string | Yes | strategy / capital / operations / human behavior / governance |
| `subdomain` | string | No | More specific classification within domain |
| `confidence_level` | enum | Yes | Seed / Developing / Strong / Structural |
| `confidence_score` | float | Yes | 0.50 / 0.72 / 0.91 / 1.00 |
| `provenance_source` | string | Yes | Session, document, or institution of origin |
| `provenance_author` | string | No | Individual or body that produced the claim |
| `activation_scope` | enum | Yes | Universal / Domain-specific / Situational / Tenant-specific |
| `activation_triggers` | jsonb | No | Conditions that cause this nugget to fire |
| `polarity` | enum | Yes | Positive / Cautionary / Negative / Neutral / Mixed |
| `durability_class` | enum | Yes | Enduring / Medium-term / Ephemeral |
| `evidence_status` | enum | Yes | Observed / Argued / Inferred / Corroborated / Unverified |
| `freshness_class` | enum | Yes | Timeless / Date-sensitive / Event-bound / Expiring |
| `composability_score` | integer | No | 0–100 |
| `origin` | enum | No | Internal / External / Mixed (required for types 21–24) |
| `counterclaim_links` | UUID[] | No | FKs → other `atomic_nuggets.nugget_id` |
| `supporting_claim_links` | UUID[] | No | FKs → other `atomic_nuggets.nugget_id` |
| `scenario_tags` | string[] | No | Named scenarios that invoke this claim |
| `rail_candidate` | boolean | No | Flagged for rail elevation |
| `selection_method` | enum | Yes | `machine_extracted` / `keyboard_trigger` / `human_memorialized` / `second_order` |
| `generation_depth` | integer | Yes | `1` for first-order (from conversation); `2+` for second-order (from rail artifacts) |
| `source_rail_artifact_id` | UUID | No | FK → `rail_artifacts.artifact_id` (populated for second-order nuggets only) |
| `created_at` | timestamptz | Yes | When the nugget was created |
| `expires_at` | timestamptz | No | Null for Enduring; populated for Ephemeral/Medium-term |

**Retention:** Perpetual for Enduring durability class. Ephemeral nuggets may be archived after `expires_at`.  
**Indexes:** `(tenant_id, claim_type)`, `(tenant_id, domain)`, `(tenant_id, confidence_score DESC)`, `(tenant_id, session_id)`

---

### 3. `preserved_ideas`

Human-memorialized items. Every record here is the result of a deliberate human capture act — right-click → Memorialize or keyboard trigger elevated to Memorialize status. All preserved ideas also exist as records in `atomic_nuggets` — this table provides additional provenance and priority metadata for the human-capture path.

| Field | Type | Required | Description |
|---|---|---|---|
| `idea_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `nugget_id` | UUID | Yes | FK → `atomic_nuggets.nugget_id` |
| `session_id` | UUID | Yes | Source session |
| `source_event_id` | UUID | Yes | FK → `conversation_events.event_id` |
| `selected_text` | text | Yes | The exact text the operator selected and memorialized |
| `memorialized_by` | UUID | Yes | FK → users table — who memorialized it |
| `memorialized_at` | timestamptz | Yes | When the act occurred |
| `corroborated_by` | UUID[] | No | Array of user IDs who independently memorialized the same or closely related text |
| `corroboration_count` | integer | Yes | Default 1; increments on each independent corroboration |
| `structural_threshold_crossed_at` | timestamptz | No | When corroboration_count triggered Structural confidence (≥2 independent users) |
| `rail_card_id` | UUID | No | FK → `right_rail_cards.card_id` — the card this idea appeared on |

**Retention:** Perpetual. No expiry. No purge. A preserved idea is permanent.  
**Indexes:** `(tenant_id, memorialized_by)`, `(tenant_id, memorialized_at DESC)`

---

### 4. `executive_conclusions`

Reconstructed operator-facing intelligence. Generated by the reconstructor when a cluster of high-signal atomic nuggets crosses the reconstruction threshold. These are Tier 3 objects — they are not raw claims but synthesized conclusions drawn from multiple claims.

| Field | Type | Required | Description |
|---|---|---|---|
| `conclusion_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `session_id` | UUID | Yes | Source session |
| `conclusion_text` | text | Yes | The clean operator-facing conclusion — one or two sentences |
| `source_nugget_ids` | UUID[] | Yes | FKs → `atomic_nuggets.nugget_id` — the claims that produced this conclusion |
| `claim_types_present` | string[] | Yes | The GAQP claim types represented in the source cluster |
| `reconstruction_confidence` | float | Yes | Aggregate confidence score across source nuggets |
| `domain` | string | Yes | Primary domain of the conclusion |
| `polarity` | enum | Yes | Positive / Cautionary / Negative / Neutral / Mixed |
| `rail_card_type` | enum | Yes | Which rail card type this maps to (Executive Conclusion / Risk / Opportunity / etc.) |
| `generated_at` | timestamptz | Yes | When reconstruction ran |
| `promoted_to_artifact_id` | UUID | No | FK → `rail_artifacts.artifact_id` — set when this conclusion becomes a persisted artifact |

**Retention:** Retained as long as source nuggets exist. May be regenerated if source nugget confidence changes.  
**Indexes:** `(tenant_id, session_id)`, `(tenant_id, generated_at DESC)`, `(tenant_id, rail_card_type)`

---

### 5. `right_rail_cards`

Display projection objects. These are the view-layer records that tell the rail what to show. They are not the system of record — they are a projection of `executive_conclusions` and `preserved_ideas` into a displayable form. A rail card may be dismissed (removed from view) without deleting any underlying corpus object.

| Field | Type | Required | Description |
|---|---|---|---|
| `card_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `session_id` | UUID | Yes | The chat session this card belongs to |
| `card_type` | enum | Yes | One of the 8 canonical rail card types |
| `card_text` | text | Yes | The conclusion text displayed on the card |
| `source_conclusion_id` | UUID | No | FK → `executive_conclusions.conclusion_id` (auto-extracted cards) |
| `source_idea_id` | UUID | No | FK → `preserved_ideas.idea_id` (memorialized cards) |
| `is_memorialized` | boolean | Yes | True if this card originated from a human Memorialize act |
| `is_pinned` | boolean | Yes | True if the operator has pinned this card |
| `is_dismissed` | boolean | Yes | True if the operator has dismissed this from view |
| `pin_order` | integer | No | Order among pinned cards; null if not pinned |
| `display_rank` | integer | Yes | Current computed position in the default rail order |
| `created_at` | timestamptz | Yes | When the card was generated |
| `dismissed_at` | timestamptz | No | When the operator dismissed it |
| `artifact_id` | UUID | No | FK → `rail_artifacts.artifact_id` — set when this card is persisted as an artifact |

**Retention:** Retained for session lifetime. Dismissed cards remain in the table with `is_dismissed = true`.  
**Indexes:** `(tenant_id, session_id, is_dismissed, display_rank)`, `(tenant_id, session_id, is_pinned)`

---

### 6. `rail_artifacts`

Persisted rail cards — first-class corpus objects. Every card that is preserved, promoted, routed, or that crosses a significance threshold becomes a rail artifact. Rail artifacts are not ephemeral display objects; they are permanent intelligence records that feed the second-order deconstruction process.

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `session_id` | UUID | Yes | Source session |
| `source_card_id` | UUID | Yes | FK → `right_rail_cards.card_id` |
| `artifact_text` | text | Yes | The conclusion text at time of artifact creation |
| `card_type` | enum | Yes | The rail card type this artifact preserves |
| `is_memorialized` | boolean | Yes | Inherited from source card |
| `operator_action` | enum | Yes | `preserved` / `promoted` / `routed` / `system_auto` — what caused artifact creation |
| `actioned_by` | UUID | No | FK → users table — who triggered artifact creation (null for system_auto) |
| `actioned_at` | timestamptz | Yes | When the artifact was created |
| `second_order_deconstruction_status` | enum | Yes | `pending` / `in_progress` / `complete` / `skipped` |
| `second_order_nugget_ids` | UUID[] | No | FKs → `atomic_nuggets.nugget_id` — populated after deconstruction |
| `deconstructed_at` | timestamptz | No | When second-order deconstruction completed |
| `promotion_candidate_id` | UUID | No | FK → `promotion_candidates.candidate_id` — if this artifact is a promotion nominee |

**Retention:** Perpetual. Rail artifacts are never deleted.  
**Indexes:** `(tenant_id, session_id)`, `(tenant_id, second_order_deconstruction_status)`, `(tenant_id, actioned_at DESC)`

---

### 7. `promotion_candidates`

Doctrine elevation nominees. A promotion candidate is a rail artifact or executive conclusion that has been nominated for Canon elevation. Promotion requires explicit human approval — the system nominates, a human authorizes.

| Field | Type | Required | Description |
|---|---|---|---|
| `candidate_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `source_artifact_id` | UUID | No | FK → `rail_artifacts.artifact_id` |
| `source_conclusion_id` | UUID | No | FK → `executive_conclusions.conclusion_id` |
| `candidate_text` | text | Yes | The proposed doctrine statement |
| `proposed_claim_type` | enum | Yes | The GAQP claim type for the proposed canon entry |
| `nominated_by` | enum | Yes | `system_auto` / `operator` |
| `nominated_by_user_id` | UUID | No | FK → users table (null for system_auto) |
| `nominated_at` | timestamptz | Yes | When nomination occurred |
| `nomination_rationale` | text | No | Why this was nominated |
| `review_status` | enum | Yes | `pending` / `approved` / `rejected` / `deferred` |
| `reviewed_by` | UUID | No | FK → users table — who made the review decision |
| `reviewed_at` | timestamptz | No | When the review decision was made |
| `rejection_reason` | text | No | Why the nomination was rejected |
| `canon_nugget_id` | UUID | No | FK → `atomic_nuggets.nugget_id` — the promoted canon entry (set on approval) |

**Retention:** Perpetual regardless of review_status.  
**Indexes:** `(tenant_id, review_status)`, `(tenant_id, nominated_at DESC)`

---

### 8. `runtime_activations`

Records of nugget firings. Every time a nugget activates in a reasoning context — triggers a rail card, contributes to a conclusion, fires in a reflex — a runtime activation is recorded. This table is the audit trail of how corpus knowledge influenced live reasoning.

| Field | Type | Required | Description |
|---|---|---|---|
| `activation_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `nugget_id` | UUID | Yes | FK → `atomic_nuggets.nugget_id` |
| `session_id` | UUID | Yes | Session in which the nugget fired |
| `activation_context` | enum | Yes | `reconstruction` / `reflex` / `diagnostic` / `retrieval` / `contradiction_check` |
| `triggered_object_type` | enum | No | `executive_conclusion` / `rail_card` / `governance_flag` / `contradiction` |
| `triggered_object_id` | UUID | No | FK to the triggered object |
| `activation_score` | float | No | How strongly this nugget contributed to the triggered output |
| `activated_at` | timestamptz | Yes | When the activation occurred |

**Retention:** Retained for audit and corpus analysis. May be archived after 12 months but never deleted.  
**Indexes:** `(tenant_id, nugget_id)`, `(tenant_id, session_id)`, `(tenant_id, activated_at DESC)`

---

### 9. `audit_events`

Full audit trail across all tiers and all objects. Every significant state change in the pipeline produces an audit event. This table is the forensic record.

| Field | Type | Required | Description |
|---|---|---|---|
| `audit_id` | UUID | Yes | Primary key |
| `tenant_id` | UUID | Yes | Tenant namespace |
| `event_type` | string | Yes | Namespaced event identifier (e.g. `nugget.created`, `idea.memorialized`, `conclusion.generated`, `artifact.created`, `candidate.approved`) |
| `actor_type` | enum | Yes | `system` / `operator` / `agent` |
| `actor_id` | UUID | No | User or agent ID (null for system events) |
| `object_type` | string | Yes | The type of object affected |
| `object_id` | UUID | Yes | The ID of the affected object |
| `prior_state` | jsonb | No | Relevant prior field values before the change |
| `new_state` | jsonb | No | Relevant new field values after the change |
| `session_id` | UUID | No | Associated session if applicable |
| `occurred_at` | timestamptz | Yes | When the event occurred |
| `notes` | text | No | Human or system notes on the event |

**Retention:** Perpetual. Audit events are immutable and are never modified or deleted.  
**Indexes:** `(tenant_id, event_type)`, `(tenant_id, object_id)`, `(tenant_id, occurred_at DESC)`, `(tenant_id, actor_id)`

---

## IV. Cross-Object Rules

1. **Tenant isolation is absolute.** No query across this schema should ever return results from more than one `tenant_id` without an explicit cross-tenant authorization object.

2. **Soft deletes only.** No record in any of these tables is ever hard-deleted. Dismissal, archiving, and expiry are state changes, not deletions.

3. **Source anchors must survive.** A `source_event_id` FK must remain resolvable for the life of any downstream object. `conversation_events` records are perpetual for this reason.

4. **Confidence is mutable; provenance is not.** A nugget's `confidence_score` and `confidence_level` may be updated as corroboration accumulates. Its `provenance_source`, `provenance_author`, `source_event_id`, and `created_at` are immutable once written.

5. **Second-order nuggets use the same table as first-order.** They are distinguished by `generation_depth >= 2` and a populated `source_rail_artifact_id`. They participate in the full corpus on equal footing.

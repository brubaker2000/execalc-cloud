-- QCR v1.0: Qualitative Capture Runtime tables
-- Implements the 9-object pipeline from QUALITATIVE_CAPTURE_RUNTIME_SPEC.md
-- All 9 tables are separate concerns — do not merge.

-- ---------------------------------------------------------------------------
-- Tier 0: Raw archive
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_conversation_events (
    event_id                TEXT        NOT NULL,
    tenant_id               TEXT        NOT NULL REFERENCES tenants(tenant_id),
    session_id              TEXT        NOT NULL,
    user_id                 TEXT        NOT NULL,
    role                    TEXT        NOT NULL CHECK (role IN ('operator', 'system', 'agent')),
    message_text            TEXT        NOT NULL,
    token_count             INTEGER,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    capture_queued_at       TIMESTAMPTZ,
    capture_completed_at    TIMESTAMPTZ,
    metadata                JSONB       NOT NULL DEFAULT '{}',
    PRIMARY KEY (event_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_events_tenant_session
    ON qcr_conversation_events (tenant_id, session_id);

CREATE INDEX IF NOT EXISTS idx_qcr_events_tenant_created
    ON qcr_conversation_events (tenant_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- Tier 1–2: Captured signal / Structured claims
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_atomic_nuggets (
    nugget_id               TEXT        NOT NULL,
    tenant_id               TEXT        NOT NULL REFERENCES tenants(tenant_id),
    session_id              TEXT        NOT NULL,
    source_event_id         TEXT        NOT NULL REFERENCES qcr_conversation_events(event_id),
    claim_text              TEXT        NOT NULL,
    claim_type              TEXT        NOT NULL,
    domain                  TEXT        NOT NULL,
    subdomain               TEXT,
    confidence_level        TEXT        NOT NULL CHECK (confidence_level IN ('seed', 'developing', 'corroborated', 'structural')),
    confidence_score        FLOAT       NOT NULL,
    provenance_source       TEXT        NOT NULL,
    provenance_author       TEXT,
    activation_scope        TEXT        NOT NULL,
    activation_triggers     JSONB       NOT NULL DEFAULT '[]',
    polarity                TEXT        NOT NULL CHECK (polarity IN ('positive', 'cautionary', 'negative', 'neutral', 'mixed')),
    durability_class        TEXT        NOT NULL CHECK (durability_class IN ('enduring', 'medium_term', 'ephemeral')),
    evidence_status         TEXT        NOT NULL CHECK (evidence_status IN ('observed', 'argued', 'inferred', 'corroborated', 'unverified')),
    freshness_class         TEXT        NOT NULL CHECK (freshness_class IN ('timeless', 'date_sensitive', 'event_bound', 'expiring')),
    composability_score     INTEGER     CHECK (composability_score BETWEEN 0 AND 100),
    origin                  TEXT,
    counterclaim_links      JSONB       NOT NULL DEFAULT '[]',
    supporting_claim_links  JSONB       NOT NULL DEFAULT '[]',
    scenario_tags           JSONB       NOT NULL DEFAULT '[]',
    rail_candidate          BOOLEAN     NOT NULL DEFAULT FALSE,
    selection_method        TEXT        NOT NULL CHECK (selection_method IN ('machine_extracted', 'keyboard_trigger', 'human_memorialized', 'second_order')),
    generation_depth        INTEGER     NOT NULL DEFAULT 1,
    source_rail_artifact_id TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at              TIMESTAMPTZ,
    PRIMARY KEY (nugget_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_nuggets_tenant_claim_type
    ON qcr_atomic_nuggets (tenant_id, claim_type);

CREATE INDEX IF NOT EXISTS idx_qcr_nuggets_tenant_domain
    ON qcr_atomic_nuggets (tenant_id, domain);

CREATE INDEX IF NOT EXISTS idx_qcr_nuggets_tenant_confidence
    ON qcr_atomic_nuggets (tenant_id, confidence_score DESC);

CREATE INDEX IF NOT EXISTS idx_qcr_nuggets_tenant_session
    ON qcr_atomic_nuggets (tenant_id, session_id);

CREATE INDEX IF NOT EXISTS idx_qcr_nuggets_rail_candidates
    ON qcr_atomic_nuggets (tenant_id, session_id)
    WHERE rail_candidate = TRUE;

-- ---------------------------------------------------------------------------
-- Tier 1–2: Human-preserved items
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_preserved_ideas (
    idea_id                         TEXT        NOT NULL,
    tenant_id                       TEXT        NOT NULL REFERENCES tenants(tenant_id),
    nugget_id                       TEXT        NOT NULL REFERENCES qcr_atomic_nuggets(nugget_id),
    session_id                      TEXT        NOT NULL,
    source_event_id                 TEXT        NOT NULL REFERENCES qcr_conversation_events(event_id),
    selected_text                   TEXT        NOT NULL,
    memorialized_by                 TEXT        NOT NULL,
    memorialized_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    corroborated_by                 JSONB       NOT NULL DEFAULT '[]',
    corroboration_count             INTEGER     NOT NULL DEFAULT 1,
    structural_threshold_crossed_at TIMESTAMPTZ,
    rail_card_id                    TEXT,
    PRIMARY KEY (idea_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_ideas_tenant_by
    ON qcr_preserved_ideas (tenant_id, memorialized_by);

CREATE INDEX IF NOT EXISTS idx_qcr_ideas_tenant_at
    ON qcr_preserved_ideas (tenant_id, memorialized_at DESC);

-- ---------------------------------------------------------------------------
-- Tier 3: Executive conclusions
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_executive_conclusions (
    conclusion_id               TEXT        NOT NULL,
    tenant_id                   TEXT        NOT NULL REFERENCES tenants(tenant_id),
    session_id                  TEXT        NOT NULL,
    conclusion_text             TEXT        NOT NULL,
    source_nugget_ids           JSONB       NOT NULL DEFAULT '[]',
    claim_types_present         JSONB       NOT NULL DEFAULT '[]',
    reconstruction_confidence   FLOAT       NOT NULL,
    domain                      TEXT        NOT NULL,
    polarity                    TEXT        NOT NULL CHECK (polarity IN ('positive', 'cautionary', 'negative', 'neutral', 'mixed')),
    rail_card_type              TEXT        NOT NULL,
    generated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    promoted_to_artifact_id     TEXT,
    PRIMARY KEY (conclusion_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_conclusions_tenant_session
    ON qcr_executive_conclusions (tenant_id, session_id);

CREATE INDEX IF NOT EXISTS idx_qcr_conclusions_tenant_generated
    ON qcr_executive_conclusions (tenant_id, generated_at DESC);

CREATE INDEX IF NOT EXISTS idx_qcr_conclusions_tenant_card_type
    ON qcr_executive_conclusions (tenant_id, rail_card_type);

-- ---------------------------------------------------------------------------
-- Tier 3: Rail display projection
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_right_rail_cards (
    card_id                 TEXT        NOT NULL,
    tenant_id               TEXT        NOT NULL REFERENCES tenants(tenant_id),
    session_id              TEXT        NOT NULL,
    card_type               TEXT        NOT NULL,
    card_text               TEXT        NOT NULL,
    source_conclusion_id    TEXT        REFERENCES qcr_executive_conclusions(conclusion_id),
    source_idea_id          TEXT        REFERENCES qcr_preserved_ideas(idea_id),
    is_memorialized         BOOLEAN     NOT NULL DEFAULT FALSE,
    is_pinned               BOOLEAN     NOT NULL DEFAULT FALSE,
    is_dismissed            BOOLEAN     NOT NULL DEFAULT FALSE,
    pin_order               INTEGER,
    display_rank            INTEGER     NOT NULL DEFAULT 0,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    dismissed_at            TIMESTAMPTZ,
    artifact_id             TEXT,
    PRIMARY KEY (card_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_cards_tenant_session_active
    ON qcr_right_rail_cards (tenant_id, session_id, is_dismissed, display_rank);

CREATE INDEX IF NOT EXISTS idx_qcr_cards_tenant_session_pinned
    ON qcr_right_rail_cards (tenant_id, session_id, is_pinned);

-- ---------------------------------------------------------------------------
-- Tier 3: Rail artifacts (first-class, perpetual)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_rail_artifacts (
    artifact_id                         TEXT        NOT NULL,
    tenant_id                           TEXT        NOT NULL REFERENCES tenants(tenant_id),
    session_id                          TEXT        NOT NULL,
    source_card_id                      TEXT        NOT NULL REFERENCES qcr_right_rail_cards(card_id),
    artifact_text                       TEXT        NOT NULL,
    card_type                           TEXT        NOT NULL,
    is_memorialized                     BOOLEAN     NOT NULL DEFAULT FALSE,
    operator_action                     TEXT        NOT NULL CHECK (operator_action IN ('preserved', 'promoted', 'routed', 'system_auto')),
    actioned_by                         TEXT,
    actioned_at                         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    second_order_deconstruction_status  TEXT        NOT NULL DEFAULT 'pending'
                                                    CHECK (second_order_deconstruction_status IN ('pending', 'in_progress', 'complete', 'skipped')),
    second_order_nugget_ids             JSONB       NOT NULL DEFAULT '[]',
    deconstructed_at                    TIMESTAMPTZ,
    promotion_candidate_id              TEXT,
    PRIMARY KEY (artifact_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_artifacts_tenant_session
    ON qcr_rail_artifacts (tenant_id, session_id);

CREATE INDEX IF NOT EXISTS idx_qcr_artifacts_pending_deconstruction
    ON qcr_rail_artifacts (tenant_id, second_order_deconstruction_status)
    WHERE second_order_deconstruction_status = 'pending';

CREATE INDEX IF NOT EXISTS idx_qcr_artifacts_tenant_actioned
    ON qcr_rail_artifacts (tenant_id, actioned_at DESC);

-- ---------------------------------------------------------------------------
-- Tier 3→4: Promotion candidates
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_promotion_candidates (
    candidate_id            TEXT        NOT NULL,
    tenant_id               TEXT        NOT NULL REFERENCES tenants(tenant_id),
    source_artifact_id      TEXT        REFERENCES qcr_rail_artifacts(artifact_id),
    source_conclusion_id    TEXT        REFERENCES qcr_executive_conclusions(conclusion_id),
    candidate_text          TEXT        NOT NULL,
    proposed_claim_type     TEXT        NOT NULL,
    nominated_by            TEXT        NOT NULL CHECK (nominated_by IN ('system_auto', 'operator')),
    nominated_by_user_id    TEXT,
    nominated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    nomination_rationale    TEXT,
    review_status           TEXT        NOT NULL DEFAULT 'pending'
                                        CHECK (review_status IN ('pending', 'approved', 'rejected', 'deferred')),
    reviewed_by             TEXT,
    reviewed_at             TIMESTAMPTZ,
    rejection_reason        TEXT,
    canon_nugget_id         TEXT,
    PRIMARY KEY (candidate_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_candidates_tenant_status
    ON qcr_promotion_candidates (tenant_id, review_status);

CREATE INDEX IF NOT EXISTS idx_qcr_candidates_tenant_nominated
    ON qcr_promotion_candidates (tenant_id, nominated_at DESC);

-- ---------------------------------------------------------------------------
-- Audit: Runtime activations
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_runtime_activations (
    activation_id           TEXT        NOT NULL,
    tenant_id               TEXT        NOT NULL REFERENCES tenants(tenant_id),
    nugget_id               TEXT        NOT NULL REFERENCES qcr_atomic_nuggets(nugget_id),
    session_id              TEXT        NOT NULL,
    activation_context      TEXT        NOT NULL CHECK (activation_context IN ('reconstruction', 'reflex', 'diagnostic', 'retrieval', 'contradiction_check')),
    triggered_object_type   TEXT        CHECK (triggered_object_type IN ('executive_conclusion', 'rail_card', 'governance_flag', 'contradiction')),
    triggered_object_id     TEXT,
    activation_score        FLOAT,
    activated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (activation_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_activations_tenant_session
    ON qcr_runtime_activations (tenant_id, session_id);

CREATE INDEX IF NOT EXISTS idx_qcr_activations_nugget
    ON qcr_runtime_activations (tenant_id, nugget_id);

-- ---------------------------------------------------------------------------
-- Audit: Full audit trail
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS qcr_audit_events (
    audit_id                TEXT        NOT NULL,
    tenant_id               TEXT        NOT NULL REFERENCES tenants(tenant_id),
    event_kind              TEXT        NOT NULL,
    actor_id                TEXT,
    source_object_type      TEXT,
    source_object_id        TEXT,
    payload                 JSONB       NOT NULL DEFAULT '{}',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (audit_id)
);

CREATE INDEX IF NOT EXISTS idx_qcr_audit_tenant_created
    ON qcr_audit_events (tenant_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_qcr_audit_tenant_kind
    ON qcr_audit_events (tenant_id, event_kind);

-- PEM v1.0: memory_objects table
-- Persistent Executive Memory corpus — tenant-scoped, provenance-carrying,
-- activation-state-aware. Separate from execution_records and gaqp_claims.

CREATE TABLE IF NOT EXISTS memory_objects (
    memory_id        TEXT        NOT NULL,
    tenant_id        TEXT        NOT NULL REFERENCES tenants(tenant_id),
    memory_class     TEXT        NOT NULL CHECK (memory_class IN ('gaqp_claim', 'structural')),
    activation_state TEXT        NOT NULL CHECK (activation_state IN ('active', 'deferred', 'reference_only', 'dormant')),

    content          TEXT        NOT NULL,
    summary          TEXT        NOT NULL,
    source_kind      TEXT        NOT NULL,
    source_ref       TEXT        NOT NULL,
    origin_surface   TEXT        NOT NULL,

    -- Class A (gaqp_claim): claim_type required, memory_family null
    -- Class B (structural): memory_family required, claim_type null
    claim_type       TEXT,
    domain           TEXT,
    memory_family    TEXT,

    actor_id         TEXT,
    admission_reason TEXT,
    confidence       NUMERIC(5,4),

    related_memory_ids JSONB    NOT NULL DEFAULT '[]',
    supersedes       TEXT,

    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    archived_at      TIMESTAMPTZ,

    PRIMARY KEY (memory_id),
    CONSTRAINT memory_objects_class_a_check CHECK (
        memory_class != 'gaqp_claim' OR (claim_type IS NOT NULL AND memory_family IS NULL)
    ),
    CONSTRAINT memory_objects_class_b_check CHECK (
        memory_class != 'structural' OR (memory_family IS NOT NULL AND claim_type IS NULL)
    )
);

CREATE INDEX IF NOT EXISTS idx_memory_objects_tenant_state
    ON memory_objects (tenant_id, activation_state);

CREATE INDEX IF NOT EXISTS idx_memory_objects_tenant_claim_type
    ON memory_objects (tenant_id, claim_type)
    WHERE claim_type IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_memory_objects_tenant_family
    ON memory_objects (tenant_id, memory_family)
    WHERE memory_family IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_memory_objects_tenant_domain
    ON memory_objects (tenant_id, domain)
    WHERE domain IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_memory_objects_tenant_created
    ON memory_objects (tenant_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_memory_objects_source_ref
    ON memory_objects (tenant_id, source_ref);

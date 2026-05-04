-- Execalc Cloud SQL schema (PostgreSQL)
-- Canonical baseline for multi-tenant persistence

CREATE TABLE IF NOT EXISTS tenants (
  tenant_id TEXT PRIMARY KEY,
  tenant_name TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS execution_records (
  record_id BIGSERIAL PRIMARY KEY,
  tenant_id TEXT NOT NULL REFERENCES tenants(tenant_id),
  envelope_id TEXT NOT NULL,
  ok BOOLEAN NOT NULL,
  result JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_execution_records_tenant_created
  ON execution_records (tenant_id, created_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_execution_records_tenant_envelope
  ON execution_records (tenant_id, envelope_id);


-- ---------------------------------------------------------------------------
-- Stage 9C: GAQP corpus
-- Complex fields (provenance, activation_triggers, corroboration_profile,
-- contradiction_refs, support_refs) stored as JSONB for v1 flexibility.
-- Link tables (gaqp_claim_sources, gaqp_claim_links) deferred to v2.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gaqp_claims (
  claim_id             TEXT        NOT NULL,
  tenant_id            TEXT        NOT NULL REFERENCES tenants(tenant_id),
  source_envelope_id   TEXT        NOT NULL,
  claim_type           TEXT        NOT NULL,
  domain               TEXT        NOT NULL,
  content              TEXT        NOT NULL,
  confidence_level     TEXT        NOT NULL,
  confidence_score     FLOAT       NOT NULL,
  admission_status     TEXT        NOT NULL,
  corpus_scope         TEXT        NOT NULL,
  extraction_method    TEXT        NOT NULL,
  provenance           JSONB       NOT NULL DEFAULT '{}',
  activation_scope     TEXT        NOT NULL,
  activation_triggers  JSONB       NOT NULL DEFAULT '[]',
  corroboration_profile JSONB      NOT NULL DEFAULT '{}',
  contradiction_refs   JSONB       NOT NULL DEFAULT '[]',
  support_refs         JSONB       NOT NULL DEFAULT '[]',
  fingerprint          TEXT        NOT NULL,
  schema_version       TEXT        NOT NULL,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (claim_id)
);

-- Idempotent backfill: duplicate fingerprints are silently skipped
CREATE UNIQUE INDEX IF NOT EXISTS uq_gaqp_claims_fingerprint
  ON gaqp_claims (fingerprint);

-- Primary activation query path
CREATE INDEX IF NOT EXISTS idx_gaqp_claims_tenant_type
  ON gaqp_claims (tenant_id, claim_type);

-- Corpus-wide confidence floor filtering
CREATE INDEX IF NOT EXISTS idx_gaqp_claims_scope_confidence
  ON gaqp_claims (corpus_scope, confidence_score DESC);

-- Backfill verification: all claims from a given decision artifact
CREATE INDEX IF NOT EXISTS idx_gaqp_claims_envelope
  ON gaqp_claims (tenant_id, source_envelope_id);

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

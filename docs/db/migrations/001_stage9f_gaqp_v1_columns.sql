-- Migration 001: Stage 9F — GAQP v1.0 spec columns
-- Adds inference_flag, source_location, and standards_package_version to
-- gaqp_claims. Safe to run multiple times (IF NOT EXISTS / SET DEFAULT guards).
--
-- Run against the live database before deploying Stage 9F code or running
-- the Stage 9G backfill.

ALTER TABLE gaqp_claims
  ADD COLUMN IF NOT EXISTS inference_flag           BOOLEAN  NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS source_location          TEXT,
  ADD COLUMN IF NOT EXISTS standards_package_version TEXT    NOT NULL DEFAULT 'gaqp_v1.0';

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.service.db.postgres import get_conn
from src.service.gaqp.models import GAQPClaim

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class InsertSummary:
    inserted: int = 0
    skipped: int = 0   # duplicate fingerprint — idempotent, not an error
    failed: int = 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_psycopg2_json():
    try:
        from psycopg2.extras import Json  # type: ignore
        return Json
    except ImportError as e:
        raise RuntimeError(
            "psycopg2 is not available. Install the Postgres dependency before using corpus persistence."
        ) from e


def _claim_to_row(claim: GAQPClaim, Json: Any) -> tuple:
    return (
        claim.claim_id,
        claim.tenant_id,
        claim.source_envelope_id,
        claim.claim_type,
        claim.domain,
        claim.content,
        claim.confidence_level,
        claim.confidence_score,
        claim.admission_status,
        claim.corpus_scope,
        claim.extraction_method,
        Json(claim.provenance.to_dict()),
        claim.activation_scope,
        Json(claim.activation_triggers),
        Json(claim.corroboration_profile.to_dict()),
        Json(claim.contradiction_refs),
        Json(claim.support_refs),
        claim.fingerprint,
        claim.schema_version,
    )


_INSERT_SQL = """
    INSERT INTO gaqp_claims (
        claim_id, tenant_id, source_envelope_id, claim_type, domain, content,
        confidence_level, confidence_score, admission_status, corpus_scope,
        extraction_method, provenance, activation_scope, activation_triggers,
        corroboration_profile, contradiction_refs, support_refs,
        fingerprint, schema_version
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s
    )
    ON CONFLICT (fingerprint) DO NOTHING
"""

_SELECT_BY_ID_SQL = """
    SELECT claim_id, tenant_id, source_envelope_id, claim_type, domain, content,
           confidence_level, confidence_score, admission_status, corpus_scope,
           extraction_method, provenance, activation_scope, activation_triggers,
           corroboration_profile, contradiction_refs, support_refs,
           fingerprint, schema_version, created_at, updated_at
    FROM gaqp_claims
    WHERE claim_id = %s AND tenant_id = %s
"""

_SELECT_BY_ENVELOPE_SQL = """
    SELECT claim_id, tenant_id, source_envelope_id, claim_type, domain, content,
           confidence_level, confidence_score, admission_status, corpus_scope,
           extraction_method, provenance, activation_scope, activation_triggers,
           corroboration_profile, contradiction_refs, support_refs,
           fingerprint, schema_version, created_at, updated_at
    FROM gaqp_claims
    WHERE tenant_id = %s AND source_envelope_id = %s
    ORDER BY created_at ASC
"""


def _row_to_dict(row: tuple) -> Dict[str, Any]:
    (
        claim_id, tenant_id, source_envelope_id, claim_type, domain, content,
        confidence_level, confidence_score, admission_status, corpus_scope,
        extraction_method, provenance, activation_scope, activation_triggers,
        corroboration_profile, contradiction_refs, support_refs,
        fingerprint, schema_version, created_at, updated_at,
    ) = row
    return {
        "claim_id": claim_id,
        "tenant_id": tenant_id,
        "source_envelope_id": source_envelope_id,
        "claim_type": claim_type,
        "domain": domain,
        "content": content,
        "confidence_level": confidence_level,
        "confidence_score": confidence_score,
        "admission_status": admission_status,
        "corpus_scope": corpus_scope,
        "extraction_method": extraction_method,
        "provenance": provenance,
        "activation_scope": activation_scope,
        "activation_triggers": activation_triggers,
        "corroboration_profile": corroboration_profile,
        "contradiction_refs": contradiction_refs,
        "support_refs": support_refs,
        "fingerprint": fingerprint,
        "schema_version": schema_version,
        "created_at": created_at.isoformat() if created_at else None,
        "updated_at": updated_at.isoformat() if updated_at else None,
    }


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def insert_claim(claim: GAQPClaim) -> bool:
    """
    Persist one admitted claim to the corpus.

    Returns True if inserted, False if skipped (duplicate fingerprint).
    Only admitted claims are written — rejected and needs_review are not persisted.
    """
    if claim.admission_status != "admitted":
        return False

    Json = _load_psycopg2_json()
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_INSERT_SQL, _claim_to_row(claim, Json))
            inserted = cur.rowcount > 0
        return inserted
    finally:
        conn.close()


def insert_claims(claims: List[GAQPClaim]) -> InsertSummary:
    """
    Batch persist admitted claims to the corpus.

    Skips non-admitted claims. Duplicate fingerprints are silently skipped
    (idempotent — safe to run the same extraction twice).
    """
    admitted = [c for c in claims if c.admission_status == "admitted"]
    if not admitted:
        return InsertSummary()

    Json = _load_psycopg2_json()
    summary = InsertSummary()
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            for claim in admitted:
                try:
                    cur.execute(_INSERT_SQL, _claim_to_row(claim, Json))
                    if cur.rowcount > 0:
                        summary.inserted += 1
                    else:
                        summary.skipped += 1
                except Exception:
                    logger.exception("Failed to insert claim %s", claim.claim_id)
                    summary.failed += 1
    finally:
        conn.close()

    return summary


def get_claim(*, claim_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single corpus claim by (claim_id, tenant_id)."""
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_SELECT_BY_ID_SQL, (claim_id, tenant_id))
            row = cur.fetchone()
            return _row_to_dict(row) if row else None
    finally:
        conn.close()


def list_claims(
    *,
    tenant_id: str,
    claim_type: Optional[str] = None,
    corpus_scope: Optional[str] = None,
    admission_status: str = "admitted",
    confidence_floor: float = 0.0,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    List corpus claims for a tenant with optional filters.

    Defaults to admitted claims above the confidence floor, newest first.
    """
    limit = max(1, min(limit, 200))

    conditions = ["tenant_id = %s", "admission_status = %s", "confidence_score >= %s"]
    params: List[Any] = [tenant_id, admission_status, confidence_floor]

    if claim_type:
        conditions.append("claim_type = %s")
        params.append(claim_type)
    if corpus_scope:
        conditions.append("corpus_scope = %s")
        params.append(corpus_scope)

    params.append(limit)
    sql = (
        "SELECT claim_id, tenant_id, source_envelope_id, claim_type, domain, content, "
        "confidence_level, confidence_score, admission_status, corpus_scope, "
        "extraction_method, provenance, activation_scope, activation_triggers, "
        "corroboration_profile, contradiction_refs, support_refs, "
        "fingerprint, schema_version, created_at, updated_at "
        "FROM gaqp_claims "
        "WHERE " + " AND ".join(conditions) +
        " ORDER BY confidence_score DESC, created_at DESC LIMIT %s"
    )

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


_UPDATE_CORROBORATION_SQL = """
    UPDATE gaqp_claims
    SET corroboration_profile = %s,
        confidence_level = %s,
        confidence_score = %s,
        updated_at = NOW()
    WHERE claim_id = %s AND tenant_id = %s
"""


def update_claim_corroboration(
    *,
    claim_id: str,
    tenant_id: str,
    new_profile: "CorroborationProfile",
    new_confidence_level: str,
    new_confidence_score: float,
) -> bool:
    """
    Persist a corroboration profile update and confidence promotion to the corpus.

    Returns True if the claim was found and updated, False if not found.
    Called exclusively by the corroboration engine after computing the new profile.
    """
    from src.service.gaqp.models import CorroborationProfile  # local to avoid circular
    Json = _load_psycopg2_json()
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_UPDATE_CORROBORATION_SQL, (
                Json(new_profile.to_dict()),
                new_confidence_level,
                new_confidence_score,
                claim_id,
                tenant_id,
            ))
            return cur.rowcount > 0
    finally:
        conn.close()


_UPDATE_CONTRADICTIONS_SQL = """
    UPDATE gaqp_claims
    SET contradiction_refs = %s,
        corroboration_profile = %s,
        updated_at = NOW()
    WHERE claim_id = %s AND tenant_id = %s
"""


def update_claim_contradictions(
    *,
    claim_id: str,
    tenant_id: str,
    new_contradiction_refs: List[str],
    new_corroboration_profile: "CorroborationProfile",
) -> bool:
    """
    Persist updated contradiction_refs and corroboration_profile for a claim.

    Returns True if the claim was found and updated, False if not found.
    Called exclusively by the contradiction engine after linking or resolving.
    """
    Json = _load_psycopg2_json()
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_UPDATE_CONTRADICTIONS_SQL, (
                Json(new_contradiction_refs),
                Json(new_corroboration_profile.to_dict()),
                claim_id,
                tenant_id,
            ))
            return cur.rowcount > 0
    finally:
        conn.close()


def list_claims_by_envelope(
    *,
    tenant_id: str,
    source_envelope_id: str,
) -> List[Dict[str, Any]]:
    """
    List all claims extracted from a specific decision artifact.
    Used for backfill verification and per-decision corpus inspection.
    """
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_SELECT_BY_ENVELOPE_SQL, (tenant_id, source_envelope_id))
            rows = cur.fetchall() or []
            return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()

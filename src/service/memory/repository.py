from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from src.service.db.postgres import get_conn
from src.service.memory.models import MemoryObject

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

_INSERT_SQL = """
    INSERT INTO memory_objects (
        memory_id, tenant_id, memory_class, activation_state,
        content, summary, source_kind, source_ref, origin_surface,
        claim_type, domain, memory_family,
        actor_id, admission_reason, confidence,
        related_memory_ids, supersedes
    ) VALUES (
        %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s
    )
    ON CONFLICT (memory_id) DO NOTHING
"""

_SELECT_BY_ID_SQL = """
    SELECT memory_id, tenant_id, memory_class, activation_state,
           content, summary, source_kind, source_ref, origin_surface,
           claim_type, domain, memory_family,
           actor_id, admission_reason, confidence,
           related_memory_ids, supersedes,
           created_at, updated_at, archived_at
    FROM memory_objects
    WHERE memory_id = %s AND tenant_id = %s
"""

_UPDATE_STATE_SQL = """
    UPDATE memory_objects
    SET activation_state = %s,
        updated_at = NOW(),
        archived_at = CASE WHEN %s IN ('dormant') THEN NULL
                          WHEN %s = 'reference_only' THEN NOW()
                          ELSE archived_at END
    WHERE memory_id = %s AND tenant_id = %s
"""

_ARCHIVE_SQL = """
    UPDATE memory_objects
    SET activation_state = 'reference_only',
        archived_at = NOW(),
        updated_at = NOW()
    WHERE memory_id = %s AND tenant_id = %s
"""


def _load_json():
    try:
        from psycopg2.extras import Json  # type: ignore
        return Json
    except ImportError as e:
        raise RuntimeError("psycopg2 not available") from e


def _row_to_dict(row: tuple) -> Dict[str, Any]:
    (
        memory_id, tenant_id, memory_class, activation_state,
        content, summary, source_kind, source_ref, origin_surface,
        claim_type, domain, memory_family,
        actor_id, admission_reason, confidence,
        related_memory_ids, supersedes,
        created_at, updated_at, archived_at,
    ) = row
    return {
        "memory_id": memory_id,
        "tenant_id": tenant_id,
        "memory_class": memory_class,
        "activation_state": activation_state,
        "content": content,
        "summary": summary,
        "source_kind": source_kind,
        "source_ref": source_ref,
        "origin_surface": origin_surface,
        "claim_type": claim_type,
        "domain": domain,
        "memory_family": memory_family,
        "actor_id": actor_id,
        "admission_reason": admission_reason,
        "confidence": float(confidence) if confidence is not None else None,
        "related_memory_ids": list(related_memory_ids or []),
        "supersedes": supersedes,
        "created_at": created_at.isoformat() if created_at else None,
        "updated_at": updated_at.isoformat() if updated_at else None,
        "archived_at": archived_at.isoformat() if archived_at else None,
    }


def _dict_to_object(d: Dict[str, Any]) -> MemoryObject:
    def _dt(v: Optional[str]) -> datetime:
        return datetime.fromisoformat(v) if v else datetime.now(UTC)

    return MemoryObject(
        memory_id=d["memory_id"],
        tenant_id=d["tenant_id"],
        memory_class=d["memory_class"],
        activation_state=d["activation_state"],
        content=d["content"],
        summary=d["summary"],
        source_kind=d["source_kind"],
        source_ref=d["source_ref"],
        origin_surface=d["origin_surface"],
        claim_type=d.get("claim_type"),
        domain=d.get("domain"),
        memory_family=d.get("memory_family"),
        actor_id=d.get("actor_id"),
        admission_reason=d.get("admission_reason"),
        confidence=d.get("confidence"),
        related_memory_ids=list(d.get("related_memory_ids") or []),
        supersedes=d.get("supersedes"),
        created_at=_dt(d.get("created_at")),
        updated_at=_dt(d.get("updated_at")),
        archived_at=datetime.fromisoformat(d["archived_at"]) if d.get("archived_at") else None,
    )


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def db_insert(obj: MemoryObject) -> bool:
    Json = _load_json()
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_INSERT_SQL, (
                obj.memory_id, obj.tenant_id, obj.memory_class, obj.activation_state,
                obj.content, obj.summary, obj.source_kind, obj.source_ref, obj.origin_surface,
                obj.claim_type, obj.domain, obj.memory_family,
                obj.actor_id, obj.admission_reason, obj.confidence,
                Json(list(obj.related_memory_ids)), obj.supersedes,
            ))
            return cur.rowcount > 0
    finally:
        conn.close()


def db_get(*, tenant_id: str, memory_id: str) -> Optional[MemoryObject]:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_SELECT_BY_ID_SQL, (memory_id, tenant_id))
            row = cur.fetchone()
            return _dict_to_object(_row_to_dict(row)) if row else None
    finally:
        conn.close()


def db_list(
    *,
    tenant_id: str,
    activation_state: Optional[str] = None,
    claim_type: Optional[str] = None,
    memory_family: Optional[str] = None,
    domain: Optional[str] = None,
    limit: int = 50,
) -> List[MemoryObject]:
    limit = max(1, min(limit, 200))

    conditions = ["tenant_id = %s"]
    params: List[Any] = [tenant_id]

    if activation_state:
        conditions.append("activation_state = %s")
        params.append(activation_state)
    if claim_type:
        conditions.append("claim_type = %s")
        params.append(claim_type)
    if memory_family:
        conditions.append("memory_family = %s")
        params.append(memory_family)
    if domain:
        conditions.append("domain = %s")
        params.append(domain)

    params.append(limit)
    sql = (
        "SELECT memory_id, tenant_id, memory_class, activation_state, "
        "content, summary, source_kind, source_ref, origin_surface, "
        "claim_type, domain, memory_family, "
        "actor_id, admission_reason, confidence, "
        "related_memory_ids, supersedes, "
        "created_at, updated_at, archived_at "
        "FROM memory_objects "
        "WHERE " + " AND ".join(conditions) +
        " ORDER BY confidence DESC NULLS LAST, created_at DESC LIMIT %s"
    )

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            return [_dict_to_object(_row_to_dict(r)) for r in rows]
    finally:
        conn.close()


def db_update_state(
    *,
    tenant_id: str,
    memory_id: str,
    new_state: str,
) -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_UPDATE_STATE_SQL, (new_state, new_state, new_state, memory_id, tenant_id))
            return cur.rowcount > 0
    finally:
        conn.close()

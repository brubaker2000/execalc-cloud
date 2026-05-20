from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from src.service.memory.admission import AdmissionError, build
from src.service.memory.models import ACTIVATION_STATES, MemoryContext, MemoryObject
from src.service.memory.repository import db_get, db_insert, db_list, db_update_state
from src.service.memory.upstream_context import assemble_context

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public service seam — all callers use these five functions only
# ---------------------------------------------------------------------------

def admit_memory(
    *,
    tenant_id: str,
    memory_class: str,
    content: str,
    summary: str,
    source_kind: str,
    source_ref: str,
    origin_surface: str,
    activation_state: str = "active",
    claim_type: Optional[str] = None,
    domain: Optional[str] = None,
    memory_family: Optional[str] = None,
    actor_id: Optional[str] = None,
    admission_reason: Optional[str] = None,
    confidence: Optional[float] = None,
    related_memory_ids: Optional[List[str]] = None,
    supersedes: Optional[str] = None,
) -> MemoryObject:
    """
    Admit a new memory object through the governed PEM seam.

    Validates, classifies, builds, and persists. All callers use this
    function — no direct repository writes are permitted outside this seam.
    Raises AdmissionError on validation failure.
    """
    obj = build(
        tenant_id=tenant_id,
        memory_class=memory_class,
        content=content,
        summary=summary,
        source_kind=source_kind,
        source_ref=source_ref,
        origin_surface=origin_surface,
        activation_state=activation_state,
        claim_type=claim_type,
        domain=domain,
        memory_family=memory_family,
        actor_id=actor_id,
        admission_reason=admission_reason,
        confidence=confidence,
        related_memory_ids=related_memory_ids or [],
        supersedes=supersedes,
    )

    try:
        db_insert(obj)
    except Exception:
        logger.exception("PEM db_insert failed for tenant %s", tenant_id)
        raise

    logger.debug("PEM admitted memory_id=%s tenant=%s class=%s", obj.memory_id, tenant_id, memory_class)
    return obj


def get_memory(*, tenant_id: str, memory_id: str) -> Optional[MemoryObject]:
    """Retrieve a single memory object by ID within tenant scope."""
    try:
        return db_get(tenant_id=tenant_id, memory_id=memory_id)
    except Exception:
        logger.exception("PEM get_memory failed for %s tenant %s", memory_id, tenant_id)
        return None


def list_memory(
    *,
    tenant_id: str,
    limit: int = 50,
    activation_state: Optional[str] = None,
    claim_type: Optional[str] = None,
    memory_family: Optional[str] = None,
    domain: Optional[str] = None,
) -> List[MemoryObject]:
    """
    List memory objects for a tenant with optional filters.

    Bounded to 200 max. Ordered by confidence DESC, recency DESC.
    """
    try:
        return db_list(
            tenant_id=tenant_id,
            activation_state=activation_state,
            claim_type=claim_type,
            memory_family=memory_family,
            domain=domain,
            limit=limit,
        )
    except Exception:
        logger.exception("PEM list_memory failed for tenant %s", tenant_id)
        return []


def get_upstream_context(
    *,
    tenant_id: str,
    scenario_type: str,
    domain: Optional[str] = None,
) -> MemoryContext:
    """
    Assemble PEM memory context for upstream reasoning.

    Returns an empty MemoryContext if PEM is unavailable — upstream
    reasoning proceeds normally without memory rather than failing.
    """
    try:
        return assemble_context(
            tenant_id=tenant_id,
            scenario_type=scenario_type,
            domain=domain,
        )
    except Exception:
        logger.exception("PEM get_upstream_context failed for tenant %s", tenant_id)
        return MemoryContext(
            tenant_id=tenant_id,
            scenario_type=scenario_type,
            domain=domain,
            items=[],
        )


def update_memory_state(
    *,
    tenant_id: str,
    memory_id: str,
    new_state: str,
    actor_id: Optional[str] = None,
    reason: Optional[str] = None,
) -> Optional[MemoryObject]:
    """
    Update the activation state of a memory object.

    Valid transitions: active ↔ deferred, active → reference_only,
    any → dormant. Returns the updated object or None if not found.
    """
    if new_state not in ACTIVATION_STATES:
        raise ValueError(f"new_state must be one of {ACTIVATION_STATES}")

    try:
        updated = db_update_state(tenant_id=tenant_id, memory_id=memory_id, new_state=new_state)
        if not updated:
            return None
        return db_get(tenant_id=tenant_id, memory_id=memory_id)
    except Exception:
        logger.exception(
            "PEM update_memory_state failed for %s tenant %s", memory_id, tenant_id
        )
        return None

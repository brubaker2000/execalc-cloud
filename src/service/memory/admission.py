from __future__ import annotations

import secrets
from datetime import UTC, datetime
from typing import Optional

from src.service.memory.models import (
    ACTIVATION_STATES,
    MEMORY_CLASSES,
    MEMORY_FAMILIES,
    SOURCE_KINDS,
    MemoryObject,
)
from src.service.gaqp.models import CLAIM_TYPES


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class AdmissionError(ValueError):
    pass


def validate(
    *,
    tenant_id: str,
    memory_class: str,
    content: str,
    summary: str,
    source_kind: str,
    source_ref: str,
    origin_surface: str,
    activation_state: str,
    claim_type: Optional[str],
    memory_family: Optional[str],
) -> None:
    if not tenant_id or not tenant_id.strip():
        raise AdmissionError("tenant_id is required")
    if memory_class not in MEMORY_CLASSES:
        raise AdmissionError(f"memory_class must be one of {MEMORY_CLASSES}")
    if not content or not content.strip():
        raise AdmissionError("content is required")
    if not summary or not summary.strip():
        raise AdmissionError("summary is required")
    if source_kind not in SOURCE_KINDS:
        raise AdmissionError(f"source_kind must be one of {SOURCE_KINDS}")
    if not source_ref or not source_ref.strip():
        raise AdmissionError("source_ref is required")
    if not origin_surface or not origin_surface.strip():
        raise AdmissionError("origin_surface is required")
    if activation_state not in ACTIVATION_STATES:
        raise AdmissionError(f"activation_state must be one of {ACTIVATION_STATES}")

    if memory_class == "gaqp_claim":
        if not claim_type:
            raise AdmissionError("claim_type is required for gaqp_claim memory objects")
        if claim_type not in CLAIM_TYPES:
            raise AdmissionError(f"claim_type '{claim_type}' is not a valid GAQP type")
        if memory_family is not None:
            raise AdmissionError("memory_family must not be set for gaqp_claim objects — use claim_type")

    if memory_class == "structural":
        if not memory_family:
            raise AdmissionError("memory_family is required for structural memory objects")
        if memory_family not in MEMORY_FAMILIES:
            raise AdmissionError(f"memory_family must be one of {MEMORY_FAMILIES}")
        if claim_type is not None:
            raise AdmissionError("claim_type must not be set for structural objects — use memory_family")


def build(
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
    related_memory_ids: Optional[list] = None,
    supersedes: Optional[str] = None,
) -> MemoryObject:
    validate(
        tenant_id=tenant_id,
        memory_class=memory_class,
        content=content,
        summary=summary,
        source_kind=source_kind,
        source_ref=source_ref,
        origin_surface=origin_surface,
        activation_state=activation_state,
        claim_type=claim_type,
        memory_family=memory_family,
    )
    now = datetime.now(UTC)
    return MemoryObject(
        memory_id=secrets.token_hex(16),
        tenant_id=tenant_id,
        memory_class=memory_class,
        activation_state=activation_state,
        content=content,
        summary=summary,
        source_kind=source_kind,
        source_ref=source_ref,
        origin_surface=origin_surface,
        claim_type=claim_type,
        domain=domain,
        memory_family=memory_family,
        actor_id=actor_id,
        admission_reason=admission_reason,
        confidence=confidence,
        related_memory_ids=list(related_memory_ids or []),
        supersedes=supersedes,
        created_at=now,
        updated_at=now,
    )

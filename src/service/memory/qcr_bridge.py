from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_STRUCTURAL_CONFIDENCE = 1.00


def admit_structural_claim(
    *,
    claim_id: str,
    tenant_id: str,
    claim_type: str,
    domain: str,
    content: str,
    confidence_score: float,
    source_envelope_id: str,
    actor_id: Optional[str] = None,
) -> bool:
    """
    Admit a GAQP claim that has reached structural confidence into PEM.

    Called by the corroboration engine after a claim is promoted to structural.
    Returns True if admitted, False if skipped or failed.

    Only structural-confidence claims (score == 1.00) are eligible.
    """
    if confidence_score < _STRUCTURAL_CONFIDENCE:
        return False

    try:
        from src.service.memory.service import admit_memory
        admit_memory(
            tenant_id=tenant_id,
            memory_class="gaqp_claim",
            content=content,
            summary=f"Structural GAQP claim: {claim_type}",
            source_kind="qcr_nugget",
            source_ref=claim_id,
            origin_surface="qcr_corpus",
            activation_state="active",
            claim_type=claim_type,
            domain=domain,
            actor_id=actor_id,
            confidence=confidence_score,
            admission_reason="GAQP structural confidence threshold reached",
        )
        logger.info(
            "PEM admitted structural claim %s (type=%s tenant=%s)",
            claim_id, claim_type, tenant_id,
        )
        return True
    except Exception:
        logger.exception(
            "PEM admission failed for structural claim %s tenant %s",
            claim_id, tenant_id,
        )
        return False


def admit_memorialized_item(
    *,
    idea_id: str,
    tenant_id: str,
    claim_type: str,
    domain: Optional[str],
    content: str,
    actor_id: str,
) -> bool:
    """
    Admit a human-memorialized rail item into PEM immediately.

    Human preservation is the highest-priority admission path.
    Activation state is always 'active'.
    """
    try:
        from src.service.memory.service import admit_memory
        admit_memory(
            tenant_id=tenant_id,
            memory_class="gaqp_claim",
            content=content,
            summary=f"Operator-memorialized: {claim_type}",
            source_kind="qcr_preserved",
            source_ref=idea_id,
            origin_surface="executive_rail",
            activation_state="active",
            claim_type=claim_type,
            domain=domain,
            actor_id=actor_id,
            confidence=0.91,  # Strong — human validation
            admission_reason="Operator Memorialize action",
        )
        logger.info("PEM admitted memorialized item %s tenant %s", idea_id, tenant_id)
        return True
    except Exception:
        logger.exception("PEM admission failed for memorialized item %s tenant %s", idea_id, tenant_id)
        return False

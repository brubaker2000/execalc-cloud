from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Optional

from src.service.qualitative_capture.models import AtomicNugget, PromotionCandidate
from src.service.qualitative_capture.repository import (
    get_promotion_candidate,
    insert_nugget,
    insert_promotion_candidate,
    list_promotion_candidates,
    update_candidate_review,
)

logger = logging.getLogger(__name__)

VALID_REVIEW_STATUSES = {"pending", "approved", "rejected", "deferred"}

_CANON_SESSION_ID = "system:canon_elevation"
_CANON_CONFIDENCE = 1.00
_CANON_CONFIDENCE_LEVEL = "structural"


def nominate_for_promotion(
    *,
    tenant_id: str,
    candidate_text: str,
    proposed_claim_type: str,
    nominated_by: str,
    source_artifact_id: Optional[str] = None,
    source_conclusion_id: Optional[str] = None,
    nominated_by_user_id: Optional[str] = None,
    nomination_rationale: Optional[str] = None,
) -> PromotionCandidate:
    """
    Nominate a rail artifact or conclusion for Canon elevation.

    Nomination is always operator or system — promotion to Canon requires
    explicit human approval via approve_candidate(). This function only
    creates the candidate record.
    """
    valid_nominators = {"system_auto", "operator"}
    if nominated_by not in valid_nominators:
        raise ValueError(f"nominated_by must be one of {valid_nominators}")
    if not source_artifact_id and not source_conclusion_id:
        raise ValueError("Either source_artifact_id or source_conclusion_id is required")

    candidate = PromotionCandidate(
        candidate_id=uuid.uuid4().hex,
        tenant_id=tenant_id,
        candidate_text=candidate_text,
        proposed_claim_type=proposed_claim_type,
        nominated_by=nominated_by,
        nominated_at=datetime.now(UTC),
        review_status="pending",
        source_artifact_id=source_artifact_id,
        source_conclusion_id=source_conclusion_id,
        nominated_by_user_id=nominated_by_user_id,
        nomination_rationale=nomination_rationale,
    )

    try:
        insert_promotion_candidate(candidate)
        logger.info(
            "QCR promotion: candidate=%s tenant=%s claim_type=%s nominated_by=%s",
            candidate.candidate_id, tenant_id, proposed_claim_type, nominated_by,
        )
    except Exception:
        logger.exception("QCR promotion: candidate persistence failed for tenant %s", tenant_id)

    return candidate


def approve_candidate(
    *,
    candidate_id: str,
    tenant_id: str,
    reviewed_by: str,
    domain: Optional[str] = None,
) -> bool:
    """
    Approve a promotion candidate and elevate it to Canon (Tier 4).

    Creates a structural-confidence (1.00) AtomicNugget, links it back to the
    candidate record as canon_nugget_id, and admits it to PEM via qcr_bridge.

    Returns True if the candidate was found and approved, False if not found.
    """
    candidate = get_promotion_candidate(
        candidate_id=candidate_id, tenant_id=tenant_id
    )
    if candidate is None:
        return False

    canon_nugget = _build_canon_nugget(candidate, domain=domain, approved_by=reviewed_by)

    try:
        insert_nugget(canon_nugget)
        logger.info(
            "Canon nugget created: nugget_id=%s candidate=%s tenant=%s",
            canon_nugget.nugget_id, candidate_id, tenant_id,
        )
    except Exception:
        logger.exception(
            "Canon nugget insert failed for candidate %s tenant %s",
            candidate_id, tenant_id,
        )

    _admit_to_pem(canon_nugget, candidate_id=candidate_id)

    updated = update_candidate_review(
        candidate_id=candidate_id,
        tenant_id=tenant_id,
        review_status="approved",
        reviewed_by=reviewed_by,
        canon_nugget_id=canon_nugget.nugget_id,
    )

    logger.info(
        "QCR Canon elevation: candidate=%s nugget=%s tenant=%s by=%s",
        candidate_id, canon_nugget.nugget_id, tenant_id, reviewed_by,
    )
    return updated


def reject_candidate(
    *,
    candidate_id: str,
    tenant_id: str,
    reviewed_by: str,
    rejection_reason: Optional[str] = None,
) -> bool:
    """Reject a promotion candidate."""
    return update_candidate_review(
        candidate_id=candidate_id,
        tenant_id=tenant_id,
        review_status="rejected",
        reviewed_by=reviewed_by,
        rejection_reason=rejection_reason,
    )


def list_pending_candidates(*, tenant_id: str, limit: int = 50) -> list:
    """List promotion candidates awaiting review."""
    try:
        return list_promotion_candidates(
            tenant_id=tenant_id,
            review_status="pending",
            limit=limit,
        )
    except Exception:
        logger.exception("QCR promotion: list_pending_candidates failed for tenant %s", tenant_id)
        return []


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------

def _build_canon_nugget(
    candidate: dict,
    *,
    domain: Optional[str],
    approved_by: str,
) -> AtomicNugget:
    """Construct a Tier 4 canon nugget from an approved promotion candidate."""
    resolved_domain = domain or "strategy"
    return AtomicNugget(
        nugget_id=uuid.uuid4().hex,
        tenant_id=candidate["tenant_id"],
        session_id=_CANON_SESSION_ID,
        source_event_id=candidate["candidate_id"],
        claim_text=candidate["candidate_text"],
        claim_type=candidate["proposed_claim_type"],
        domain=resolved_domain,
        confidence_level=_CANON_CONFIDENCE_LEVEL,
        confidence_score=_CANON_CONFIDENCE,
        provenance_source=f"canon:candidate:{candidate['candidate_id']}",
        provenance_author=approved_by,
        activation_scope="tenant_specific",
        activation_triggers=["canon:approved", f"claim_type:{candidate['proposed_claim_type']}"],
        polarity="neutral",
        durability_class="enduring",
        evidence_status="corroborated",
        freshness_class="timeless",
        selection_method="canon_approved",
        generation_depth=1,
        rail_candidate=True,
        created_at=datetime.now(UTC),
    )


def _admit_to_pem(nugget: AtomicNugget, *, candidate_id: str) -> None:
    try:
        from src.service.memory.qcr_bridge import admit_structural_claim
        admit_structural_claim(
            claim_id=nugget.nugget_id,
            tenant_id=nugget.tenant_id,
            claim_type=nugget.claim_type,
            domain=nugget.domain,
            content=nugget.claim_text,
            confidence_score=nugget.confidence_score,
            source_envelope_id=candidate_id,
            actor_id=nugget.provenance_author,
        )
    except Exception:
        logger.exception(
            "PEM admission failed for canon nugget %s (candidate %s)",
            nugget.nugget_id, candidate_id,
        )

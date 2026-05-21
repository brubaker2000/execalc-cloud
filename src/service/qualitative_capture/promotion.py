from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Optional

from src.service.qualitative_capture.models import PromotionCandidate
from src.service.qualitative_capture.repository import (
    insert_promotion_candidate,
    list_promotion_candidates,
    update_candidate_review,
)

logger = logging.getLogger(__name__)

VALID_REVIEW_STATUSES = {"pending", "approved", "rejected", "deferred"}


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
) -> bool:
    """
    Approve a promotion candidate for Canon elevation.

    Approval triggers PEM admission of the candidate as a structural-confidence
    memory object — the highest tier of durable knowledge.
    """
    updated = update_candidate_review(
        candidate_id=candidate_id,
        tenant_id=tenant_id,
        review_status="approved",
        reviewed_by=reviewed_by,
    )
    if not updated:
        return False

    logger.info(
        "QCR promotion approved: candidate=%s tenant=%s by=%s",
        candidate_id, tenant_id, reviewed_by,
    )
    return True


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

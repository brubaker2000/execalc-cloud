from __future__ import annotations

import logging
import uuid
from typing import Dict, Optional

from src.service.qualitative_capture.repository import (
    insert_audit_event,
    list_expired_ephemeral_nuggets,
    list_stale_date_sensitive_nuggets,
    list_stale_medium_term_nuggets,
    update_nugget_confidence,
)

logger = logging.getLogger(__name__)

# Decay thresholds — sourced from GAQP_TEMPORAL_DECAY_RULES.md
_MEDIUM_TERM_STALE_MONTHS = 12
_DATE_SENSITIVE_STALE_DAYS = 90

# Expired ephemeral nuggets are set to this score (effectively archived)
_EXPIRED_CONFIDENCE_SCORE = 0.0
_EXPIRED_CONFIDENCE_LEVEL = "seed"

# Canon-confidence nuggets are exempt from all automated decay
_CANON_CONFIDENCE = 1.00


def apply_decay_pass(
    *,
    tenant_id: str,
    batch_size: int = 50,
) -> Dict:
    """
    Run one decay pass for a tenant.

    Applies the rules from GAQP_TEMPORAL_DECAY_RULES.md:
      - Ephemeral nuggets past expires_at → confidence zeroed (effectively archived)
      - Medium-term nuggets older than 12 months → decay review audit event emitted
      - Date-sensitive nuggets without corroboration in 90 days → staleness audit event

    Canon-confidence nuggets (score == 1.00) are exempt from all actions.
    No records are deleted. The corpus record is permanent.

    Returns a summary dict: {expired, flagged_medium_term, flagged_date_sensitive, failed}
    """
    summary: Dict[str, int] = {
        "expired": 0,
        "flagged_medium_term": 0,
        "flagged_date_sensitive": 0,
        "failed": 0,
    }

    _expire_ephemeral(tenant_id=tenant_id, batch_size=batch_size, summary=summary)
    _flag_medium_term(tenant_id=tenant_id, batch_size=batch_size, summary=summary)
    _flag_date_sensitive(tenant_id=tenant_id, batch_size=batch_size, summary=summary)

    logger.info(
        "Decay pass complete: tenant=%s expired=%d flagged_mt=%d flagged_ds=%d failed=%d",
        tenant_id,
        summary["expired"],
        summary["flagged_medium_term"],
        summary["flagged_date_sensitive"],
        summary["failed"],
    )
    return summary


def _expire_ephemeral(*, tenant_id: str, batch_size: int, summary: Dict) -> None:
    try:
        expired = list_expired_ephemeral_nuggets(tenant_id=tenant_id, limit=batch_size)
    except Exception:
        logger.exception("decay: failed to list expired ephemeral nuggets for tenant %s", tenant_id)
        return

    for nugget in expired:
        nugget_id = nugget["nugget_id"]
        if nugget.get("confidence_score", 0) >= _CANON_CONFIDENCE:
            continue  # exempt — canon revision path only
        try:
            update_nugget_confidence(
                nugget_id=nugget_id,
                tenant_id=tenant_id,
                new_score=_EXPIRED_CONFIDENCE_SCORE,
                new_level=_EXPIRED_CONFIDENCE_LEVEL,
            )
            _audit(
                tenant_id=tenant_id,
                event_kind="nugget.expired",
                source_object_id=nugget_id,
                payload={"reason": "ephemeral_expires_at_passed"},
            )
            summary["expired"] += 1
        except Exception:
            logger.exception("decay: failed to expire nugget %s", nugget_id)
            summary["failed"] += 1


def _flag_medium_term(*, tenant_id: str, batch_size: int, summary: Dict) -> None:
    try:
        stale = list_stale_medium_term_nuggets(
            tenant_id=tenant_id,
            months_threshold=_MEDIUM_TERM_STALE_MONTHS,
            limit=batch_size,
        )
    except Exception:
        logger.exception("decay: failed to list stale medium_term nuggets for tenant %s", tenant_id)
        return

    for nugget in stale:
        nugget_id = nugget["nugget_id"]
        if nugget.get("confidence_score", 0) >= _CANON_CONFIDENCE:
            continue
        try:
            _audit(
                tenant_id=tenant_id,
                event_kind="nugget.decay_review_requested",
                source_object_id=nugget_id,
                payload={
                    "reason": "medium_term_12mo_threshold",
                    "confidence_score": nugget.get("confidence_score"),
                },
            )
            summary["flagged_medium_term"] += 1
        except Exception:
            logger.exception("decay: failed to emit review event for nugget %s", nugget_id)
            summary["failed"] += 1


def _flag_date_sensitive(*, tenant_id: str, batch_size: int, summary: Dict) -> None:
    try:
        stale = list_stale_date_sensitive_nuggets(
            tenant_id=tenant_id,
            days_threshold=_DATE_SENSITIVE_STALE_DAYS,
            limit=batch_size,
        )
    except Exception:
        logger.exception("decay: failed to list stale date_sensitive nuggets for tenant %s", tenant_id)
        return

    for nugget in stale:
        nugget_id = nugget["nugget_id"]
        if nugget.get("confidence_score", 0) >= _CANON_CONFIDENCE:
            continue
        try:
            _audit(
                tenant_id=tenant_id,
                event_kind="nugget.staleness_flagged",
                source_object_id=nugget_id,
                payload={
                    "reason": "date_sensitive_90d_without_corroboration",
                    "confidence_score": nugget.get("confidence_score"),
                },
            )
            summary["flagged_date_sensitive"] += 1
        except Exception:
            logger.exception("decay: failed to emit staleness event for nugget %s", nugget_id)
            summary["failed"] += 1


def _audit(
    *,
    tenant_id: str,
    event_kind: str,
    source_object_id: Optional[str] = None,
    payload: Optional[Dict] = None,
) -> None:
    try:
        insert_audit_event(
            audit_id=uuid.uuid4().hex,
            tenant_id=tenant_id,
            event_kind=event_kind,
            source_object_type="qcr_nugget",
            source_object_id=source_object_id,
            payload=payload or {},
        )
    except Exception:
        logger.warning("decay: audit write failed for event_kind %s nugget %s", event_kind, source_object_id)

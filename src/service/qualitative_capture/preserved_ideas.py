from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Optional

from src.service.qualitative_capture.models import AtomicNugget, PreservedIdea
from src.service.qualitative_capture.repository import insert_nugget, insert_preserved_idea

logger = logging.getLogger(__name__)

_MEMORIALIZE_CONFIDENCE_SCORE = 0.91   # Strong — human validation
_MEMORIALIZE_CONFIDENCE_LEVEL = "corroborated"


def memorialize(
    *,
    tenant_id: str,
    session_id: str,
    source_event_id: str,
    selected_text: str,
    memorialized_by: str,
    claim_type: str,
    domain: Optional[str] = None,
) -> PreservedIdea:
    """
    Human memorialize path — operator deliberately captures a piece of text.

    This is the highest-priority admission path. Confidence starts at Strong
    (0.91) regardless of the machine extraction outcome for the same content.
    Creates both an AtomicNugget (Tier 2) and a PreservedIdea (Tier 1–2).

    Also admits the item to PEM via qcr_bridge so it persists across sessions.
    """
    now = datetime.now(UTC)
    nugget_id = uuid.uuid4().hex
    idea_id = uuid.uuid4().hex

    nugget = AtomicNugget(
        nugget_id=nugget_id,
        tenant_id=tenant_id,
        session_id=session_id,
        source_event_id=source_event_id,
        claim_text=selected_text,
        claim_type=claim_type,
        domain=domain or "strategy",
        confidence_level=_MEMORIALIZE_CONFIDENCE_LEVEL,
        confidence_score=_MEMORIALIZE_CONFIDENCE_SCORE,
        provenance_source=f"session:{session_id}",
        provenance_author=memorialized_by,
        activation_scope="tenant_specific",
        activation_triggers=[f"session:{session_id}", "human_memorialized"],
        polarity="neutral",
        durability_class="enduring",
        evidence_status="observed",
        freshness_class="timeless",
        selection_method="human_memorialized",
        generation_depth=1,
        rail_candidate=True,
        created_at=now,
    )

    idea = PreservedIdea(
        idea_id=idea_id,
        tenant_id=tenant_id,
        nugget_id=nugget_id,
        session_id=session_id,
        source_event_id=source_event_id,
        selected_text=selected_text,
        memorialized_by=memorialized_by,
        memorialized_at=now,
    )

    try:
        insert_nugget(nugget)
    except Exception:
        logger.exception("QCR memorialize: nugget persistence failed for idea %s", idea_id)

    try:
        insert_preserved_idea(idea)
    except Exception:
        logger.exception("QCR memorialize: idea persistence failed for idea %s", idea_id)

    try:
        from src.service.memory.qcr_bridge import admit_memorialized_item
        admit_memorialized_item(
            idea_id=idea_id,
            tenant_id=tenant_id,
            claim_type=claim_type,
            domain=domain,
            content=selected_text,
            actor_id=memorialized_by,
        )
    except Exception:
        logger.exception("QCR memorialize: PEM admission failed for idea %s", idea_id)

    logger.info(
        "QCR memorialize: idea=%s tenant=%s claim_type=%s by=%s",
        idea_id, tenant_id, claim_type, memorialized_by,
    )
    return idea

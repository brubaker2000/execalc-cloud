from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Optional

from src.service.qualitative_capture.models import ConversationEvent
from src.service.qualitative_capture.repository import insert_event

logger = logging.getLogger(__name__)

VALID_ROLES = {"operator", "system", "agent"}


def ingest_event(
    *,
    tenant_id: str,
    session_id: str,
    user_id: str,
    role: str,
    message_text: str,
    token_count: Optional[int] = None,
) -> ConversationEvent:
    """
    Ingest a raw conversation event into the Tier 0 archive.

    Non-blocking — callers should fire this and proceed. The return value
    carries the event_id needed for downstream deconstruction.
    """
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role {role!r}. Must be one of: {VALID_ROLES}")
    if not message_text or not message_text.strip():
        raise ValueError("message_text must not be empty")

    event = ConversationEvent(
        event_id=uuid.uuid4().hex,
        tenant_id=tenant_id,
        session_id=session_id,
        user_id=user_id,
        role=role,
        message_text=message_text,
        token_count=token_count,
        created_at=datetime.now(UTC),
        capture_queued_at=datetime.now(UTC),
    )

    try:
        insert_event(event)
        logger.debug(
            "QCR event ingested: event=%s tenant=%s session=%s role=%s",
            event.event_id, tenant_id, session_id, role,
        )
    except Exception:
        logger.exception(
            "QCR event persistence failed for tenant=%s session=%s; returning event without DB write",
            tenant_id, session_id,
        )

    return event

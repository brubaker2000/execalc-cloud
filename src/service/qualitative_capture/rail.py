from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import List, Optional

from src.service.qualitative_capture.models import (
    ExecutiveConclusion,
    PreservedIdea,
    RailArtifact,
    RightRailCard,
)
from src.service.qualitative_capture.repository import (
    dismiss_rail_card,
    insert_rail_artifact,
    insert_rail_card,
    list_rail_cards,
    pin_rail_card,
)

logger = logging.getLogger(__name__)


def project_conclusion_to_rail(
    conclusion: ExecutiveConclusion,
    *,
    display_rank: int = 0,
) -> RightRailCard:
    """Project an executive conclusion onto the rail as a display card."""
    return RightRailCard(
        card_id=uuid.uuid4().hex,
        tenant_id=conclusion.tenant_id,
        session_id=conclusion.session_id,
        card_type=conclusion.rail_card_type,
        card_text=conclusion.conclusion_text,
        source_conclusion_id=conclusion.conclusion_id,
        is_memorialized=False,
        is_pinned=False,
        is_dismissed=False,
        display_rank=display_rank,
        created_at=datetime.now(UTC),
    )


def project_idea_to_rail(
    idea: PreservedIdea,
    *,
    display_rank: int = 0,
) -> RightRailCard:
    """Project a preserved idea onto the rail as a memorialized card."""
    return RightRailCard(
        card_id=uuid.uuid4().hex,
        tenant_id=idea.tenant_id,
        session_id=idea.session_id,
        card_type="preserved_idea",
        card_text=idea.selected_text,
        source_idea_id=idea.idea_id,
        is_memorialized=True,
        is_pinned=False,
        is_dismissed=False,
        display_rank=display_rank,
        created_at=datetime.now(UTC),
    )


def persist_card_as_artifact(
    card: RightRailCard,
    *,
    operator_action: str,
    actioned_by: Optional[str] = None,
) -> RailArtifact:
    """
    Persist a rail card as a first-class artifact.

    Called when an operator preserves, promotes, or routes a card, or when
    the system auto-persists a high-significance card. The artifact enters the
    second-order deconstruction queue immediately.
    """
    valid_actions = {"preserved", "promoted", "routed", "system_auto"}
    if operator_action not in valid_actions:
        raise ValueError(f"Invalid operator_action {operator_action!r}")

    artifact = RailArtifact(
        artifact_id=uuid.uuid4().hex,
        tenant_id=card.tenant_id,
        session_id=card.session_id,
        source_card_id=card.card_id,
        artifact_text=card.card_text,
        card_type=card.card_type,
        is_memorialized=card.is_memorialized,
        operator_action=operator_action,
        actioned_by=actioned_by,
        actioned_at=datetime.now(UTC),
        second_order_deconstruction_status="pending",
    )

    try:
        insert_rail_artifact(artifact)
    except Exception:
        logger.exception("QCR rail artifact persistence failed for card %s", card.card_id)

    return artifact


def publish_conclusions_to_rail(
    conclusions: List[ExecutiveConclusion],
) -> List[RightRailCard]:
    """
    Project a batch of conclusions to the rail and persist all cards.

    Returns the list of created cards. Persistence errors are logged and
    swallowed — the rail is a display surface, not a data source.
    """
    cards: List[RightRailCard] = []
    for rank, conclusion in enumerate(conclusions):
        card = project_conclusion_to_rail(conclusion, display_rank=rank)
        try:
            insert_rail_card(card)
        except Exception:
            logger.exception(
                "QCR rail card persistence failed for conclusion %s", conclusion.conclusion_id
            )
        cards.append(card)
    return cards


def get_session_rail(
    *,
    tenant_id: str,
    session_id: str,
    include_dismissed: bool = False,
) -> List[dict]:
    """Return the current rail state for a session."""
    try:
        return list_rail_cards(
            tenant_id=tenant_id,
            session_id=session_id,
            include_dismissed=include_dismissed,
        )
    except Exception:
        logger.exception("QCR get_session_rail failed for tenant=%s session=%s", tenant_id, session_id)
        return []

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Dict, List, Optional

from src.service.qualitative_capture.repository import (
    list_conclusions,
    list_nuggets,
    list_preserved_ideas_for_session,
    list_promotion_candidates,
)

logger = logging.getLogger(__name__)

# Minimum confidence for a nugget to appear in the packet
_PACKET_CONFIDENCE_FLOOR = 0.50

# Claim types considered doctrine candidates
_DOCTRINE_TYPES = {"doctrine", "principle", "declaration_of_value", "axiom"}

# Claim types considered decisions
_DECISION_TYPES = {"objective", "tactic", "best_practice"}

# Maximum items per section in the packet
_SECTION_LIMIT = 10


@dataclass(frozen=True)
class SessionIntelligencePacket:
    session_id: str
    tenant_id: str
    generated_at: datetime
    session_title: str
    core_breakthrough: Optional[str]          # single most important output
    nugget_count: int                          # total captured
    claim_type_breakdown: Dict[str, int]       # counts by claim_type
    top_nuggets: List[Dict]                    # ranked by importance
    doctrine_candidates: List[Dict]            # doctrine/principle class
    decisions_made: List[Dict]                 # objective class
    open_questions: List[Dict]                 # seed-confidence + threshold_condition
    preserved_ideas: List[Dict]                # human-memorialized
    pending_promotions: List[Dict]             # awaiting canon review
    executive_conclusions: List[Dict]          # reconstructed Tier 3 objects
    domain: Optional[str]

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "tenant_id": self.tenant_id,
            "generated_at": self.generated_at.isoformat(),
            "session_title": self.session_title,
            "core_breakthrough": self.core_breakthrough,
            "nugget_count": self.nugget_count,
            "claim_type_breakdown": self.claim_type_breakdown,
            "top_nuggets": self.top_nuggets,
            "doctrine_candidates": self.doctrine_candidates,
            "decisions_made": self.decisions_made,
            "open_questions": self.open_questions,
            "preserved_ideas": self.preserved_ideas,
            "pending_promotions": self.pending_promotions,
            "executive_conclusions": self.executive_conclusions,
            "domain": self.domain,
        }

    @property
    def is_empty(self) -> bool:
        return self.nugget_count == 0 and not self.preserved_ideas


def _infer_session_title(nuggets: List[Dict], domain: Optional[str]) -> str:
    """
    Infer a session title from the dominant claim types and domain.

    Reads the top-3 claim types by frequency and combines them with the domain.
    Falls back to a generic label if no nuggets exist.
    """
    if not nuggets:
        return "Empty session — no claims captured"

    counts = Counter(n.get("claim_type", "unknown") for n in nuggets)
    top_types = [ct for ct, _ in counts.most_common(3)]
    type_label = " · ".join(t.replace("_", " ") for t in top_types)
    domain_label = f" [{domain}]" if domain else ""
    return f"{type_label}{domain_label}"


def _find_core_breakthrough(nuggets: List[Dict]) -> Optional[str]:
    """
    Identify the single most important output of the session.

    Priority: rail_candidate=True → highest confidence → doctrine/principle first.
    Returns the claim_text of the top candidate, or None if no nuggets.
    """
    candidates = [n for n in nuggets if n.get("rail_candidate")]
    if not candidates:
        candidates = list(nuggets)
    if not candidates:
        return None

    def _score(n: Dict) -> tuple:
        is_doctrine = n.get("claim_type") in _DOCTRINE_TYPES
        return (is_doctrine, n.get("confidence_score", 0))

    best = max(candidates, key=_score)
    return best.get("claim_text")


def generate_session_packet(
    *,
    tenant_id: str,
    session_id: str,
    domain: Optional[str] = None,
) -> SessionIntelligencePacket:
    """
    Generate a Session Intelligence Packet for a completed session.

    This is the anti-overload mechanism: long conversation in, operational packet out.
    The packet is assembled from the live corpus state — it is not cached.

    Returns a packet with is_empty=True if no intelligence has been captured yet.
    This is a valid outcome for short or low-signal sessions.
    """
    now = datetime.now(UTC)

    try:
        all_nuggets = list_nuggets(
            tenant_id=tenant_id,
            session_id=session_id,
            min_confidence=_PACKET_CONFIDENCE_FLOOR,
            limit=500,
        )
    except Exception:
        logger.exception("session_packet: failed to load nuggets for session %s", session_id)
        all_nuggets = []

    # Claim type breakdown
    breakdown = dict(Counter(n.get("claim_type", "unknown") for n in all_nuggets))

    # Top nuggets — rail candidates first, then by confidence
    top_nuggets = sorted(
        all_nuggets,
        key=lambda n: (n.get("rail_candidate", False), n.get("confidence_score", 0)),
        reverse=True,
    )[:_SECTION_LIMIT]

    # Doctrine candidates
    doctrine_candidates = [
        n for n in all_nuggets if n.get("claim_type") in _DOCTRINE_TYPES
    ][:_SECTION_LIMIT]

    # Decisions made
    decisions_made = [
        n for n in all_nuggets if n.get("claim_type") in _DECISION_TYPES
    ][:_SECTION_LIMIT]

    # Open questions: seed-confidence items + threshold conditions
    open_questions = [
        n for n in all_nuggets
        if n.get("confidence_score", 1) <= 0.50 or n.get("claim_type") == "threshold_condition"
    ][:_SECTION_LIMIT]

    # Preserved ideas
    try:
        preserved = list_preserved_ideas_for_session(
            tenant_id=tenant_id, session_id=session_id, limit=_SECTION_LIMIT,
        )
    except Exception:
        logger.exception("session_packet: failed to load preserved ideas for session %s", session_id)
        preserved = []

    # Pending promotions (session-scoped would need artifact linkage — use tenant-wide for V1)
    try:
        pending = list_promotion_candidates(
            tenant_id=tenant_id, review_status="pending", limit=_SECTION_LIMIT,
        )
    except Exception:
        logger.exception("session_packet: failed to load promotions for tenant %s", tenant_id)
        pending = []

    # Executive conclusions
    try:
        conclusions = list_conclusions(
            tenant_id=tenant_id, session_id=session_id, limit=_SECTION_LIMIT,
        )
    except Exception:
        logger.exception("session_packet: failed to load conclusions for session %s", session_id)
        conclusions = []

    title = _infer_session_title(all_nuggets, domain)
    breakthrough = _find_core_breakthrough(all_nuggets)

    packet = SessionIntelligencePacket(
        session_id=session_id,
        tenant_id=tenant_id,
        generated_at=now,
        session_title=title,
        core_breakthrough=breakthrough,
        nugget_count=len(all_nuggets),
        claim_type_breakdown=breakdown,
        top_nuggets=[_slim(n) for n in top_nuggets],
        doctrine_candidates=[_slim(n) for n in doctrine_candidates],
        decisions_made=[_slim(n) for n in decisions_made],
        open_questions=[_slim(n) for n in open_questions],
        preserved_ideas=preserved,
        pending_promotions=pending,
        executive_conclusions=conclusions,
        domain=domain,
    )

    logger.info(
        "Session packet generated: session=%s tenant=%s nuggets=%d is_empty=%s",
        session_id, tenant_id, len(all_nuggets), packet.is_empty,
    )
    return packet


def _slim(nugget: Dict) -> Dict:
    """Return a display-ready subset of a nugget for packet sections."""
    return {
        "nugget_id": nugget.get("nugget_id"),
        "claim_text": nugget.get("claim_text"),
        "claim_type": nugget.get("claim_type"),
        "domain": nugget.get("domain"),
        "confidence_score": nugget.get("confidence_score"),
        "confidence_level": nugget.get("confidence_level"),
        "polarity": nugget.get("polarity"),
        "rail_candidate": nugget.get("rail_candidate"),
        "selection_method": nugget.get("selection_method"),
    }

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from src.service.qualitative_capture.repository import (
    list_conclusions,
    list_nuggets,
    list_preserved_ideas_for_session,
    list_promotion_candidates,
    search_nuggets,
)

logger = logging.getLogger(__name__)

# Claim types that map to each retrieval shortcut
_DOCTRINE_TYPES = ["doctrine", "principle", "declaration_of_value", "axiom"]
_RISK_TYPES = ["risk", "threat", "diagnostic_signal"]
_OPPORTUNITY_TYPES = ["opportunity"]
_DECISION_TYPES = ["objective", "tactic", "best_practice"]
_CAUSAL_TYPES = ["causal_claim", "tradeoff", "threshold_condition"]
_STRUCTURAL_TYPES = ["constraint", "heuristic"]


def retrieve_doctrine(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """Return all doctrine-class claims (doctrine, principle, declaration_of_value, axiom)."""
    try:
        return list_nuggets(
            tenant_id=tenant_id,
            session_id=session_id,
            claim_type=None,
            limit=limit * len(_DOCTRINE_TYPES),
        )
    except Exception:
        logger.exception("retrieval: retrieve_doctrine failed for tenant %s", tenant_id)
        return []


def retrieve_risks(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """Return risk-class claims (risk, threat, diagnostic_signal)."""
    results = []
    for ct in _RISK_TYPES:
        try:
            results.extend(list_nuggets(
                tenant_id=tenant_id, session_id=session_id,
                claim_type=ct, limit=limit,
            ))
        except Exception:
            logger.exception("retrieval: retrieve_risks failed for claim_type %s", ct)
    results.sort(key=lambda r: r.get("confidence_score", 0), reverse=True)
    return results[:limit]


def retrieve_opportunities(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """Return opportunity claims."""
    try:
        return list_nuggets(
            tenant_id=tenant_id, session_id=session_id,
            claim_type="opportunity", limit=limit,
        )
    except Exception:
        logger.exception("retrieval: retrieve_opportunities failed for tenant %s", tenant_id)
        return []


def retrieve_decisions(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """Return decision-class claims (objective, tactic, best_practice)."""
    results = []
    for ct in _DECISION_TYPES:
        try:
            results.extend(list_nuggets(
                tenant_id=tenant_id, session_id=session_id,
                claim_type=ct, limit=limit,
            ))
        except Exception:
            logger.exception("retrieval: retrieve_decisions failed for claim_type %s", ct)
    results.sort(key=lambda r: r.get("confidence_score", 0), reverse=True)
    return results[:limit]


def retrieve_open_questions(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """
    Return low-confidence claims and threshold conditions — the corpus's open loops.

    These are signals that have been captured but not yet corroborated or resolved.
    Seed-confidence items are the most likely candidates for follow-up.
    """
    try:
        results = list_nuggets(
            tenant_id=tenant_id, session_id=session_id,
            claim_type="threshold_condition", limit=limit,
        )
        seed_items = list_nuggets(
            tenant_id=tenant_id, session_id=session_id,
            min_confidence=0.0, limit=limit * 2,
        )
        seed_only = [r for r in seed_items if r.get("confidence_score", 1) <= 0.50]
        combined = {r["nugget_id"]: r for r in results + seed_only}
        out = list(combined.values())
        out.sort(key=lambda r: r.get("created_at", ""), reverse=True)
        return out[:limit]
    except Exception:
        logger.exception("retrieval: retrieve_open_questions failed for tenant %s", tenant_id)
        return []


def retrieve_rail_candidates(
    *,
    tenant_id: str,
    session_id: str,
    limit: int = 20,
) -> List[Dict]:
    """Return all rail-candidate nuggets for a session, ranked by confidence."""
    try:
        return list_nuggets(
            tenant_id=tenant_id,
            session_id=session_id,
            rail_candidate_only=True,
            limit=limit,
        )
    except Exception:
        logger.exception("retrieval: retrieve_rail_candidates failed for session %s", session_id)
        return []


def retrieve_by_domain(
    *,
    tenant_id: str,
    domain: str,
    session_id: Optional[str] = None,
    min_confidence: float = 0.50,
    limit: int = 30,
) -> List[Dict]:
    """Return all claims for a given domain, ordered by confidence."""
    try:
        conn = __import__("src.service.db.postgres", fromlist=["get_conn"]).get_conn()
        conditions = ["tenant_id = %s", "domain = %s", "confidence_score >= %s"]
        params = [tenant_id, domain, min_confidence]
        if session_id:
            conditions.append("session_id = %s")
            params.append(session_id)
        params.append(limit)
        sql = (
            "SELECT nugget_id, tenant_id, session_id, source_event_id, claim_text, claim_type, "
            "domain, confidence_level, confidence_score, polarity, durability_class, "
            "selection_method, rail_candidate, created_at "
            "FROM qcr_atomic_nuggets WHERE " + " AND ".join(conditions) +
            " ORDER BY confidence_score DESC, created_at DESC LIMIT %s"
        )
        try:
            with conn, conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall() or []
                cols = [
                    "nugget_id", "tenant_id", "session_id", "source_event_id", "claim_text",
                    "claim_type", "domain", "confidence_level", "confidence_score", "polarity",
                    "durability_class", "selection_method", "rail_candidate", "created_at",
                ]
                return [dict(zip(cols, r)) for r in rows]
        finally:
            conn.close()
    except Exception:
        logger.exception("retrieval: retrieve_by_domain failed for domain %s", domain)
        return []


def search_claims(
    *,
    tenant_id: str,
    query: str,
    claim_types: Optional[List[str]] = None,
    domain: Optional[str] = None,
    session_id: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """
    Keyword search across the claim corpus.

    Matches all words in the query against claim_text (case-insensitive).
    Optional filters by claim_type list, domain, and session.
    """
    if not query or not query.strip():
        return []
    try:
        return search_nuggets(
            tenant_id=tenant_id,
            query=query,
            claim_types=claim_types,
            domain=domain,
            session_id=session_id,
            limit=limit,
        )
    except Exception:
        logger.exception("retrieval: search_claims failed for tenant %s query %r", tenant_id, query)
        return []


def retrieve_preserved_ideas(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 30,
) -> List[Dict]:
    """Return all preserved (human-memorialized) ideas, newest first."""
    try:
        return list_preserved_ideas_for_session(
            tenant_id=tenant_id, session_id=session_id, limit=limit,
        )
    except Exception:
        logger.exception("retrieval: retrieve_preserved_ideas failed for tenant %s", tenant_id)
        return []


def retrieve_pending_promotions(
    *,
    tenant_id: str,
    limit: int = 20,
) -> List[Dict]:
    """Return promotion candidates awaiting review."""
    try:
        return list_promotion_candidates(
            tenant_id=tenant_id, review_status="pending", limit=limit,
        )
    except Exception:
        logger.exception("retrieval: retrieve_pending_promotions failed for tenant %s", tenant_id)
        return []


def retrieve_session_conclusions(
    *,
    tenant_id: str,
    session_id: str,
    rail_card_type: Optional[str] = None,
    limit: int = 20,
) -> List[Dict]:
    """Return executive conclusions for a session, optionally filtered by card type."""
    try:
        all_conclusions = list_conclusions(
            tenant_id=tenant_id, session_id=session_id, limit=limit,
        )
        if rail_card_type:
            return [c for c in all_conclusions if c.get("rail_card_type") == rail_card_type]
        return all_conclusions
    except Exception:
        logger.exception("retrieval: retrieve_session_conclusions failed for session %s", session_id)
        return []

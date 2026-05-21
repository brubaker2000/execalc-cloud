from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from src.service.db.postgres import get_conn

logger = logging.getLogger(__name__)


def _json(v: Any) -> str:
    return json.dumps(v)


# ---------------------------------------------------------------------------
# conversation_events
# ---------------------------------------------------------------------------

def insert_event(event: "ConversationEvent") -> bool:
    from src.service.qualitative_capture.models import ConversationEvent
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_conversation_events
                    (event_id, tenant_id, session_id, user_id, role,
                     message_text, token_count, created_at, capture_queued_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                (
                    event.event_id, event.tenant_id, event.session_id,
                    event.user_id, event.role, event.message_text,
                    event.token_count, event.created_at, event.capture_queued_at,
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def mark_event_captured(event_id: str) -> None:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE qcr_conversation_events SET capture_completed_at = NOW() WHERE event_id = %s",
                (event_id,),
            )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# atomic_nuggets
# ---------------------------------------------------------------------------

def insert_nugget(nugget: "AtomicNugget") -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_atomic_nuggets
                    (nugget_id, tenant_id, session_id, source_event_id,
                     claim_text, claim_type, domain, subdomain,
                     confidence_level, confidence_score,
                     provenance_source, provenance_author,
                     activation_scope, activation_triggers,
                     polarity, durability_class, evidence_status, freshness_class,
                     composability_score, origin,
                     counterclaim_links, supporting_claim_links, scenario_tags,
                     rail_candidate, selection_method, generation_depth,
                     source_rail_artifact_id, created_at, expires_at)
                VALUES
                    (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s, %s,%s, %s,%s,
                     %s,%s,%s,%s, %s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)
                ON CONFLICT (nugget_id) DO NOTHING
                """,
                (
                    nugget.nugget_id, nugget.tenant_id, nugget.session_id, nugget.source_event_id,
                    nugget.claim_text, nugget.claim_type, nugget.domain, nugget.subdomain,
                    nugget.confidence_level, nugget.confidence_score,
                    nugget.provenance_source, nugget.provenance_author,
                    nugget.activation_scope, _json(nugget.activation_triggers),
                    nugget.polarity, nugget.durability_class, nugget.evidence_status, nugget.freshness_class,
                    nugget.composability_score, nugget.origin,
                    _json(nugget.counterclaim_links), _json(nugget.supporting_claim_links), _json(nugget.scenario_tags),
                    nugget.rail_candidate, nugget.selection_method, nugget.generation_depth,
                    nugget.source_rail_artifact_id, nugget.created_at, nugget.expires_at,
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def list_nuggets(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    claim_type: Optional[str] = None,
    min_confidence: float = 0.0,
    rail_candidate_only: bool = False,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    conditions = ["tenant_id = %s", "confidence_score >= %s"]
    params: List[Any] = [tenant_id, min_confidence]
    if session_id:
        conditions.append("session_id = %s")
        params.append(session_id)
    if claim_type:
        conditions.append("claim_type = %s")
        params.append(claim_type)
    if rail_candidate_only:
        conditions.append("rail_candidate = TRUE")
    params.append(limit)

    sql = (
        "SELECT nugget_id, tenant_id, session_id, source_event_id, claim_text, claim_type, "
        "domain, subdomain, confidence_level, confidence_score, provenance_source, provenance_author, "
        "activation_scope, activation_triggers, polarity, durability_class, evidence_status, "
        "freshness_class, composability_score, origin, counterclaim_links, supporting_claim_links, "
        "scenario_tags, rail_candidate, selection_method, generation_depth, "
        "source_rail_artifact_id, created_at, expires_at "
        "FROM qcr_atomic_nuggets WHERE " + " AND ".join(conditions) +
        " ORDER BY confidence_score DESC, created_at DESC LIMIT %s"
    )

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            cols = [
                "nugget_id", "tenant_id", "session_id", "source_event_id", "claim_text", "claim_type",
                "domain", "subdomain", "confidence_level", "confidence_score", "provenance_source",
                "provenance_author", "activation_scope", "activation_triggers", "polarity",
                "durability_class", "evidence_status", "freshness_class", "composability_score",
                "origin", "counterclaim_links", "supporting_claim_links", "scenario_tags",
                "rail_candidate", "selection_method", "generation_depth",
                "source_rail_artifact_id", "created_at", "expires_at",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def search_nuggets(
    *,
    tenant_id: str,
    query: str,
    claim_types: Optional[List[str]] = None,
    domain: Optional[str] = None,
    session_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    Keyword search across claim_text using ILIKE.

    Returns nuggets whose claim_text contains all words in the query (case-insensitive).
    Ordered by confidence_score DESC so the most authoritative matches surface first.
    """
    query = (query or "").strip()
    if not query:
        return []

    conditions = ["tenant_id = %s"]
    params: List[Any] = [tenant_id]

    for word in query.split():
        conditions.append("claim_text ILIKE %s")
        params.append(f"%{word}%")

    if session_id:
        conditions.append("session_id = %s")
        params.append(session_id)
    if domain:
        conditions.append("domain = %s")
        params.append(domain)
    if claim_types:
        placeholders = ",".join(["%s"] * len(claim_types))
        conditions.append(f"claim_type IN ({placeholders})")
        params.extend(claim_types)

    params.append(limit)

    sql = (
        "SELECT nugget_id, tenant_id, session_id, source_event_id, claim_text, claim_type, "
        "domain, subdomain, confidence_level, confidence_score, provenance_source, "
        "provenance_author, activation_scope, activation_triggers, polarity, "
        "durability_class, evidence_status, freshness_class, composability_score, "
        "origin, counterclaim_links, supporting_claim_links, scenario_tags, "
        "rail_candidate, selection_method, generation_depth, "
        "source_rail_artifact_id, created_at, expires_at "
        "FROM qcr_atomic_nuggets "
        "WHERE " + " AND ".join(conditions) +
        " ORDER BY confidence_score DESC, created_at DESC LIMIT %s"
    )

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            cols = [
                "nugget_id", "tenant_id", "session_id", "source_event_id", "claim_text", "claim_type",
                "domain", "subdomain", "confidence_level", "confidence_score", "provenance_source",
                "provenance_author", "activation_scope", "activation_triggers", "polarity",
                "durability_class", "evidence_status", "freshness_class", "composability_score",
                "origin", "counterclaim_links", "supporting_claim_links", "scenario_tags",
                "rail_candidate", "selection_method", "generation_depth",
                "source_rail_artifact_id", "created_at", "expires_at",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def list_preserved_ideas_for_session(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    conditions = ["tenant_id = %s"]
    params: List[Any] = [tenant_id]
    if session_id:
        conditions.append("session_id = %s")
        params.append(session_id)
    params.append(limit)

    sql = (
        "SELECT idea_id, tenant_id, nugget_id, session_id, source_event_id, "
        "selected_text, memorialized_by, memorialized_at, corroboration_count, "
        "corroborated_by, structural_threshold_crossed_at, rail_card_id "
        "FROM qcr_preserved_ideas "
        "WHERE " + " AND ".join(conditions) +
        " ORDER BY memorialized_at DESC LIMIT %s"
    )

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            cols = [
                "idea_id", "tenant_id", "nugget_id", "session_id", "source_event_id",
                "selected_text", "memorialized_by", "memorialized_at", "corroboration_count",
                "corroborated_by", "structural_threshold_crossed_at", "rail_card_id",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# preserved_ideas
# ---------------------------------------------------------------------------

def insert_preserved_idea(idea: "PreservedIdea") -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_preserved_ideas
                    (idea_id, tenant_id, nugget_id, session_id, source_event_id,
                     selected_text, memorialized_by, memorialized_at,
                     corroboration_count, corroborated_by)
                VALUES (%s,%s,%s,%s,%s, %s,%s,%s, %s,%s)
                ON CONFLICT (idea_id) DO NOTHING
                """,
                (
                    idea.idea_id, idea.tenant_id, idea.nugget_id, idea.session_id, idea.source_event_id,
                    idea.selected_text, idea.memorialized_by, idea.memorialized_at,
                    idea.corroboration_count, _json(idea.corroborated_by),
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def get_preserved_idea(*, idea_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT idea_id, tenant_id, nugget_id, session_id, source_event_id, "
                "selected_text, memorialized_by, memorialized_at, corroboration_count, "
                "corroborated_by, structural_threshold_crossed_at, rail_card_id "
                "FROM qcr_preserved_ideas WHERE idea_id = %s AND tenant_id = %s",
                (idea_id, tenant_id),
            )
            row = cur.fetchone()
            if not row:
                return None
            cols = [
                "idea_id", "tenant_id", "nugget_id", "session_id", "source_event_id",
                "selected_text", "memorialized_by", "memorialized_at", "corroboration_count",
                "corroborated_by", "structural_threshold_crossed_at", "rail_card_id",
            ]
            return dict(zip(cols, row))
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# executive_conclusions
# ---------------------------------------------------------------------------

def insert_conclusion(conclusion: "ExecutiveConclusion") -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_executive_conclusions
                    (conclusion_id, tenant_id, session_id, conclusion_text,
                     source_nugget_ids, claim_types_present,
                     reconstruction_confidence, domain, polarity, rail_card_type, generated_at)
                VALUES (%s,%s,%s,%s, %s,%s, %s,%s,%s,%s,%s)
                ON CONFLICT (conclusion_id) DO NOTHING
                """,
                (
                    conclusion.conclusion_id, conclusion.tenant_id, conclusion.session_id,
                    conclusion.conclusion_text,
                    _json(conclusion.source_nugget_ids), _json(conclusion.claim_types_present),
                    conclusion.reconstruction_confidence, conclusion.domain,
                    conclusion.polarity, conclusion.rail_card_type, conclusion.generated_at,
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def list_conclusions(
    *,
    tenant_id: str,
    session_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    conditions = ["tenant_id = %s"]
    params: List[Any] = [tenant_id]
    if session_id:
        conditions.append("session_id = %s")
        params.append(session_id)
    params.append(limit)

    sql = (
        "SELECT conclusion_id, tenant_id, session_id, conclusion_text, source_nugget_ids, "
        "claim_types_present, reconstruction_confidence, domain, polarity, rail_card_type, "
        "generated_at, promoted_to_artifact_id "
        "FROM qcr_executive_conclusions WHERE " + " AND ".join(conditions) +
        " ORDER BY generated_at DESC LIMIT %s"
    )

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            cols = [
                "conclusion_id", "tenant_id", "session_id", "conclusion_text", "source_nugget_ids",
                "claim_types_present", "reconstruction_confidence", "domain", "polarity",
                "rail_card_type", "generated_at", "promoted_to_artifact_id",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# right_rail_cards
# ---------------------------------------------------------------------------

def insert_rail_card(card: "RightRailCard") -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_right_rail_cards
                    (card_id, tenant_id, session_id, card_type, card_text,
                     source_conclusion_id, source_idea_id,
                     is_memorialized, is_pinned, is_dismissed,
                     pin_order, display_rank, created_at)
                VALUES (%s,%s,%s,%s,%s, %s,%s, %s,%s,%s, %s,%s,%s)
                ON CONFLICT (card_id) DO NOTHING
                """,
                (
                    card.card_id, card.tenant_id, card.session_id, card.card_type, card.card_text,
                    card.source_conclusion_id, card.source_idea_id,
                    card.is_memorialized, card.is_pinned, card.is_dismissed,
                    card.pin_order, card.display_rank, card.created_at,
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def dismiss_rail_card(*, card_id: str, tenant_id: str) -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE qcr_right_rail_cards SET is_dismissed = TRUE, dismissed_at = NOW() "
                "WHERE card_id = %s AND tenant_id = %s",
                (card_id, tenant_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def pin_rail_card(*, card_id: str, tenant_id: str, pin_order: int) -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE qcr_right_rail_cards SET is_pinned = TRUE, pin_order = %s "
                "WHERE card_id = %s AND tenant_id = %s",
                (pin_order, card_id, tenant_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def list_rail_cards(
    *,
    tenant_id: str,
    session_id: str,
    include_dismissed: bool = False,
) -> List[Dict[str, Any]]:
    sql = (
        "SELECT card_id, tenant_id, session_id, card_type, card_text, "
        "source_conclusion_id, source_idea_id, is_memorialized, is_pinned, "
        "is_dismissed, pin_order, display_rank, created_at, dismissed_at, artifact_id "
        "FROM qcr_right_rail_cards "
        "WHERE tenant_id = %s AND session_id = %s"
    )
    params: List[Any] = [tenant_id, session_id]
    if not include_dismissed:
        sql += " AND is_dismissed = FALSE"
    sql += " ORDER BY is_pinned DESC, pin_order ASC NULLS LAST, display_rank ASC"

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() or []
            cols = [
                "card_id", "tenant_id", "session_id", "card_type", "card_text",
                "source_conclusion_id", "source_idea_id", "is_memorialized", "is_pinned",
                "is_dismissed", "pin_order", "display_rank", "created_at", "dismissed_at", "artifact_id",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# rail_artifacts
# ---------------------------------------------------------------------------

def insert_rail_artifact(artifact: "RailArtifact") -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_rail_artifacts
                    (artifact_id, tenant_id, session_id, source_card_id,
                     artifact_text, card_type, is_memorialized,
                     operator_action, actioned_by, actioned_at,
                     second_order_deconstruction_status)
                VALUES (%s,%s,%s,%s, %s,%s,%s, %s,%s,%s, %s)
                ON CONFLICT (artifact_id) DO NOTHING
                """,
                (
                    artifact.artifact_id, artifact.tenant_id, artifact.session_id,
                    artifact.source_card_id,
                    artifact.artifact_text, artifact.card_type, artifact.is_memorialized,
                    artifact.operator_action, artifact.actioned_by, artifact.actioned_at,
                    artifact.second_order_deconstruction_status,
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def list_rail_artifacts_pending_deconstruction(
    *,
    tenant_id: str,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT artifact_id, tenant_id, session_id, source_card_id, artifact_text, "
                "card_type, is_memorialized, operator_action, actioned_by, actioned_at, "
                "second_order_deconstruction_status, second_order_nugget_ids, deconstructed_at "
                "FROM qcr_rail_artifacts "
                "WHERE tenant_id = %s AND second_order_deconstruction_status = 'pending' "
                "ORDER BY actioned_at ASC LIMIT %s",
                (tenant_id, limit),
            )
            rows = cur.fetchall() or []
            cols = [
                "artifact_id", "tenant_id", "session_id", "source_card_id", "artifact_text",
                "card_type", "is_memorialized", "operator_action", "actioned_by", "actioned_at",
                "second_order_deconstruction_status", "second_order_nugget_ids", "deconstructed_at",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def mark_artifact_deconstructed(
    *,
    artifact_id: str,
    tenant_id: str,
    nugget_ids: List[str],
) -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE qcr_rail_artifacts "
                "SET second_order_deconstruction_status = 'complete', "
                "    second_order_nugget_ids = %s, deconstructed_at = NOW() "
                "WHERE artifact_id = %s AND tenant_id = %s",
                (_json(nugget_ids), artifact_id, tenant_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def update_artifact_deconstruction_status(
    *,
    artifact_id: str,
    tenant_id: str,
    new_status: str,
) -> bool:
    """Transition artifact deconstruction status (pending → in_progress → complete/skipped)."""
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE qcr_rail_artifacts SET second_order_deconstruction_status = %s "
                "WHERE artifact_id = %s AND tenant_id = %s",
                (new_status, artifact_id, tenant_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def insert_audit_event(
    *,
    audit_id: str,
    tenant_id: str,
    event_kind: str,
    actor_id: Optional[str] = None,
    source_object_type: Optional[str] = None,
    source_object_id: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO qcr_audit_events "
                "(audit_id, tenant_id, event_kind, actor_id, source_object_type, source_object_id, payload) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (audit_id) DO NOTHING",
                (
                    audit_id, tenant_id, event_kind, actor_id,
                    source_object_type, source_object_id,
                    _json(payload or {}),
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# promotion_candidates
# ---------------------------------------------------------------------------

def insert_promotion_candidate(candidate: "PromotionCandidate") -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qcr_promotion_candidates
                    (candidate_id, tenant_id, source_artifact_id, source_conclusion_id,
                     candidate_text, proposed_claim_type,
                     nominated_by, nominated_by_user_id, nominated_at, nomination_rationale,
                     review_status)
                VALUES (%s,%s,%s,%s, %s,%s, %s,%s,%s,%s, %s)
                ON CONFLICT (candidate_id) DO NOTHING
                """,
                (
                    candidate.candidate_id, candidate.tenant_id,
                    candidate.source_artifact_id, candidate.source_conclusion_id,
                    candidate.candidate_text, candidate.proposed_claim_type,
                    candidate.nominated_by, candidate.nominated_by_user_id,
                    candidate.nominated_at, candidate.nomination_rationale,
                    candidate.review_status,
                ),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def get_promotion_candidate(
    *,
    candidate_id: str,
    tenant_id: str,
) -> Optional[Dict[str, Any]]:
    """Fetch a single promotion candidate by (candidate_id, tenant_id)."""
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT candidate_id, tenant_id, source_artifact_id, source_conclusion_id, "
                "candidate_text, proposed_claim_type, nominated_by, nominated_by_user_id, "
                "nominated_at, nomination_rationale, review_status, "
                "reviewed_by, reviewed_at, rejection_reason, canon_nugget_id "
                "FROM qcr_promotion_candidates "
                "WHERE candidate_id = %s AND tenant_id = %s",
                (candidate_id, tenant_id),
            )
            row = cur.fetchone()
            if row is None:
                return None
            cols = [
                "candidate_id", "tenant_id", "source_artifact_id", "source_conclusion_id",
                "candidate_text", "proposed_claim_type", "nominated_by", "nominated_by_user_id",
                "nominated_at", "nomination_rationale", "review_status",
                "reviewed_by", "reviewed_at", "rejection_reason", "canon_nugget_id",
            ]
            return dict(zip(cols, row))
    finally:
        conn.close()


def list_promotion_candidates(
    *,
    tenant_id: str,
    review_status: str = "pending",
    limit: int = 50,
) -> List[Dict[str, Any]]:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT candidate_id, tenant_id, source_artifact_id, source_conclusion_id, "
                "candidate_text, proposed_claim_type, nominated_by, nominated_by_user_id, "
                "nominated_at, nomination_rationale, review_status, "
                "reviewed_by, reviewed_at, rejection_reason, canon_nugget_id "
                "FROM qcr_promotion_candidates "
                "WHERE tenant_id = %s AND review_status = %s "
                "ORDER BY nominated_at DESC LIMIT %s",
                (tenant_id, review_status, limit),
            )
            rows = cur.fetchall() or []
            cols = [
                "candidate_id", "tenant_id", "source_artifact_id", "source_conclusion_id",
                "candidate_text", "proposed_claim_type", "nominated_by", "nominated_by_user_id",
                "nominated_at", "nomination_rationale", "review_status",
                "reviewed_by", "reviewed_at", "rejection_reason", "canon_nugget_id",
            ]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def update_candidate_review(
    *,
    candidate_id: str,
    tenant_id: str,
    review_status: str,
    reviewed_by: Optional[str] = None,
    rejection_reason: Optional[str] = None,
    canon_nugget_id: Optional[str] = None,
) -> bool:
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE qcr_promotion_candidates "
                "SET review_status = %s, reviewed_by = %s, reviewed_at = NOW(), "
                "    rejection_reason = %s, canon_nugget_id = %s "
                "WHERE candidate_id = %s AND tenant_id = %s",
                (review_status, reviewed_by, rejection_reason, canon_nugget_id,
                 candidate_id, tenant_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


# ---------------------------------------------------------------------------
# Tier 0 — Raw archive
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ConversationEvent:
    event_id: str
    tenant_id: str
    session_id: str
    user_id: str
    role: str                          # operator / system / agent
    message_text: str
    created_at: datetime
    token_count: Optional[int] = None
    capture_queued_at: Optional[datetime] = None
    capture_completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "tenant_id": self.tenant_id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "role": self.role,
            "message_text": self.message_text,
            "token_count": self.token_count,
            "created_at": self.created_at.isoformat(),
            "capture_queued_at": self.capture_queued_at.isoformat() if self.capture_queued_at else None,
            "capture_completed_at": self.capture_completed_at.isoformat() if self.capture_completed_at else None,
        }


# ---------------------------------------------------------------------------
# Tier 1–2 — Captured signal / Structured claims
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AtomicNugget:
    nugget_id: str
    tenant_id: str
    session_id: str
    source_event_id: str
    claim_text: str
    claim_type: str
    domain: str
    confidence_level: str              # seed / developing / strong / structural
    confidence_score: float
    provenance_source: str
    activation_scope: str
    polarity: str                      # positive / cautionary / negative / neutral / mixed
    durability_class: str              # enduring / medium_term / ephemeral
    evidence_status: str               # observed / argued / inferred / corroborated / unverified
    freshness_class: str               # timeless / date_sensitive / event_bound / expiring
    selection_method: str              # machine_extracted / keyboard_trigger / human_memorialized / second_order
    generation_depth: int              # 1 = first-order; 2+ = second-order
    created_at: datetime
    subdomain: Optional[str] = None
    provenance_author: Optional[str] = None
    activation_triggers: List[str] = field(default_factory=list)
    composability_score: Optional[int] = None
    origin: Optional[str] = None
    counterclaim_links: List[str] = field(default_factory=list)
    supporting_claim_links: List[str] = field(default_factory=list)
    scenario_tags: List[str] = field(default_factory=list)
    rail_candidate: bool = False
    source_rail_artifact_id: Optional[str] = None
    expires_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "nugget_id": self.nugget_id,
            "tenant_id": self.tenant_id,
            "session_id": self.session_id,
            "source_event_id": self.source_event_id,
            "claim_text": self.claim_text,
            "claim_type": self.claim_type,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "provenance_source": self.provenance_source,
            "provenance_author": self.provenance_author,
            "activation_scope": self.activation_scope,
            "activation_triggers": self.activation_triggers,
            "polarity": self.polarity,
            "durability_class": self.durability_class,
            "evidence_status": self.evidence_status,
            "freshness_class": self.freshness_class,
            "composability_score": self.composability_score,
            "origin": self.origin,
            "counterclaim_links": self.counterclaim_links,
            "supporting_claim_links": self.supporting_claim_links,
            "scenario_tags": self.scenario_tags,
            "rail_candidate": self.rail_candidate,
            "selection_method": self.selection_method,
            "generation_depth": self.generation_depth,
            "source_rail_artifact_id": self.source_rail_artifact_id,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


@dataclass(frozen=True)
class PreservedIdea:
    idea_id: str
    tenant_id: str
    nugget_id: str
    session_id: str
    source_event_id: str
    selected_text: str
    memorialized_by: str
    memorialized_at: datetime
    corroboration_count: int = 1
    corroborated_by: List[str] = field(default_factory=list)
    structural_threshold_crossed_at: Optional[datetime] = None
    rail_card_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "idea_id": self.idea_id,
            "tenant_id": self.tenant_id,
            "nugget_id": self.nugget_id,
            "session_id": self.session_id,
            "source_event_id": self.source_event_id,
            "selected_text": self.selected_text,
            "memorialized_by": self.memorialized_by,
            "memorialized_at": self.memorialized_at.isoformat(),
            "corroboration_count": self.corroboration_count,
            "corroborated_by": self.corroborated_by,
            "structural_threshold_crossed_at": (
                self.structural_threshold_crossed_at.isoformat()
                if self.structural_threshold_crossed_at else None
            ),
            "rail_card_id": self.rail_card_id,
        }


# ---------------------------------------------------------------------------
# Tier 3 — Executive conclusions / Rail
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutiveConclusion:
    conclusion_id: str
    tenant_id: str
    session_id: str
    conclusion_text: str
    source_nugget_ids: List[str]
    claim_types_present: List[str]
    reconstruction_confidence: float
    domain: str
    polarity: str
    rail_card_type: str
    generated_at: datetime
    promoted_to_artifact_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "conclusion_id": self.conclusion_id,
            "tenant_id": self.tenant_id,
            "session_id": self.session_id,
            "conclusion_text": self.conclusion_text,
            "source_nugget_ids": self.source_nugget_ids,
            "claim_types_present": self.claim_types_present,
            "reconstruction_confidence": self.reconstruction_confidence,
            "domain": self.domain,
            "polarity": self.polarity,
            "rail_card_type": self.rail_card_type,
            "generated_at": self.generated_at.isoformat(),
            "promoted_to_artifact_id": self.promoted_to_artifact_id,
        }


@dataclass(frozen=True)
class RightRailCard:
    card_id: str
    tenant_id: str
    session_id: str
    card_type: str
    card_text: str
    is_memorialized: bool
    is_pinned: bool
    is_dismissed: bool
    display_rank: int
    created_at: datetime
    source_conclusion_id: Optional[str] = None
    source_idea_id: Optional[str] = None
    pin_order: Optional[int] = None
    dismissed_at: Optional[datetime] = None
    artifact_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "card_id": self.card_id,
            "tenant_id": self.tenant_id,
            "session_id": self.session_id,
            "card_type": self.card_type,
            "card_text": self.card_text,
            "source_conclusion_id": self.source_conclusion_id,
            "source_idea_id": self.source_idea_id,
            "is_memorialized": self.is_memorialized,
            "is_pinned": self.is_pinned,
            "is_dismissed": self.is_dismissed,
            "pin_order": self.pin_order,
            "display_rank": self.display_rank,
            "created_at": self.created_at.isoformat(),
            "dismissed_at": self.dismissed_at.isoformat() if self.dismissed_at else None,
            "artifact_id": self.artifact_id,
        }


@dataclass(frozen=True)
class RailArtifact:
    artifact_id: str
    tenant_id: str
    session_id: str
    source_card_id: str
    artifact_text: str
    card_type: str
    is_memorialized: bool
    operator_action: str               # preserved / promoted / routed / system_auto
    actioned_at: datetime
    second_order_deconstruction_status: str  # pending / in_progress / complete / skipped
    actioned_by: Optional[str] = None
    second_order_nugget_ids: List[str] = field(default_factory=list)
    deconstructed_at: Optional[datetime] = None
    promotion_candidate_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "artifact_id": self.artifact_id,
            "tenant_id": self.tenant_id,
            "session_id": self.session_id,
            "source_card_id": self.source_card_id,
            "artifact_text": self.artifact_text,
            "card_type": self.card_type,
            "is_memorialized": self.is_memorialized,
            "operator_action": self.operator_action,
            "actioned_by": self.actioned_by,
            "actioned_at": self.actioned_at.isoformat(),
            "second_order_deconstruction_status": self.second_order_deconstruction_status,
            "second_order_nugget_ids": self.second_order_nugget_ids,
            "deconstructed_at": self.deconstructed_at.isoformat() if self.deconstructed_at else None,
            "promotion_candidate_id": self.promotion_candidate_id,
        }


# ---------------------------------------------------------------------------
# Tier 3→4 — Promotion candidates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PromotionCandidate:
    candidate_id: str
    tenant_id: str
    candidate_text: str
    proposed_claim_type: str
    nominated_by: str                  # system_auto / operator
    nominated_at: datetime
    review_status: str                 # pending / approved / rejected / deferred
    source_artifact_id: Optional[str] = None
    source_conclusion_id: Optional[str] = None
    nominated_by_user_id: Optional[str] = None
    nomination_rationale: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    canon_nugget_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "tenant_id": self.tenant_id,
            "source_artifact_id": self.source_artifact_id,
            "source_conclusion_id": self.source_conclusion_id,
            "candidate_text": self.candidate_text,
            "proposed_claim_type": self.proposed_claim_type,
            "nominated_by": self.nominated_by,
            "nominated_by_user_id": self.nominated_by_user_id,
            "nominated_at": self.nominated_at.isoformat(),
            "nomination_rationale": self.nomination_rationale,
            "review_status": self.review_status,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "rejection_reason": self.rejection_reason,
            "canon_nugget_id": self.canon_nugget_id,
        }

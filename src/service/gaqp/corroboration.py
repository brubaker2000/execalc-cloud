from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import List, Tuple

from src.service.gaqp.corpus import get_claim, update_claim_corroboration
from src.service.gaqp.exceptions import ClaimNotFoundError
from src.service.gaqp.models import (
    CONFIDENCE_SCORE,
    ConfidenceLevel,
    CorroborationProfile,
)

logger = logging.getLogger(__name__)

# Re-export: callers that import ClaimNotFoundError from this module still work.
__all__ = [
    "CorroborationResult", "ClaimNotFoundError",
    "corroborate", "_compute_confidence", "_actor_key",
]


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class CorroborationResult:
    claim_id: str
    was_independent: bool       # True → new actor key, independent source
    promoted: bool              # True → confidence level advanced
    previous_level: str
    new_level: str
    previous_score: float
    new_score: float
    independent_sources: int    # total after this corroboration


# ---------------------------------------------------------------------------
# Promotion logic — pure, no I/O
# ---------------------------------------------------------------------------

def _actor_key(tenant_id: str, actor_id: str) -> str:
    return f"{tenant_id}:{actor_id}"


def _compute_confidence(independent_sources: int) -> Tuple[str, float]:
    """
    Map independent_sources count to (confidence_level, confidence_score).

    independent_sources is the count of post-creation independent corroborations.
    Structural is operator-only — this function never returns it.

    Ladder:
      0 → seed (0.50)       no corroboration yet
      1 → developing (0.72) second independent source
     ≥2 → strong (0.91)    three or more converging
    """
    if independent_sources >= 2:
        return ("strong", CONFIDENCE_SCORE["strong"])
    if independent_sources >= 1:
        return ("developing", CONFIDENCE_SCORE["developing"])
    return ("seed", CONFIDENCE_SCORE["seed"])


# ---------------------------------------------------------------------------
# Engine entry point
# ---------------------------------------------------------------------------

def corroborate(
    *,
    claim_id: str,
    tenant_id: str,
    corroborating_tenant_id: str,
    corroborating_actor_id: str,
) -> CorroborationResult:
    """
    Record a corroboration event against an existing corpus claim and
    promote its confidence level if the source is independent.

    Independence criterion: (corroborating_tenant_id, corroborating_actor_id)
    must not have been seen in a prior corroboration for this claim.
    Same actor submitting the same claim twice is repetition, not corroboration.

    Structural claims are never auto-promoted further — structural is
    an operator-only elevation. Confidence is never lowered.

    Raises ClaimNotFoundError if the claim does not exist for the tenant.
    """
    row = get_claim(claim_id=claim_id, tenant_id=tenant_id)
    if row is None:
        raise ClaimNotFoundError(
            f"Claim {claim_id!r} not found for tenant {tenant_id!r}"
        )

    corr_raw = row.get("corroboration_profile") or {}
    existing_actors: List[str] = list(corr_raw.get("corroborating_actors") or [])

    key = _actor_key(corroborating_tenant_id, corroborating_actor_id)
    was_independent = key not in existing_actors

    # Counts always update
    new_count = corr_raw.get("corroboration_count", 0) + 1
    is_cross_tenant = corroborating_tenant_id != tenant_id
    new_same_tenant = corr_raw.get("same_tenant_count", 0) + (0 if is_cross_tenant else 1)
    new_cross_tenant = corr_raw.get("cross_tenant_count", 0) + (1 if is_cross_tenant else 0)

    # Independent sources and actor list update only on new actors
    new_independent = corr_raw.get("independent_sources", 0)
    updated_actors = list(existing_actors)
    if was_independent:
        new_independent += 1
        updated_actors.append(key)

    new_profile = CorroborationProfile(
        corroboration_count=new_count,
        independent_sources=new_independent,
        same_tenant_count=new_same_tenant,
        cross_tenant_count=new_cross_tenant,
        contradictions=corr_raw.get("contradictions", 0),
        last_corroborated_at=datetime.now(UTC),
        corroborating_actors=updated_actors,
    )

    previous_level: str = row["confidence_level"]
    previous_score: float = row["confidence_score"]

    # Structural is an operator ceiling — never auto-promote into it,
    # never demote from it.
    if previous_level == "structural":
        new_level, new_score = "structural", CONFIDENCE_SCORE["structural"]
    else:
        computed_level, computed_score = _compute_confidence(new_independent)
        if computed_score >= previous_score:
            new_level, new_score = computed_level, computed_score
        else:
            new_level, new_score = previous_level, previous_score

    promoted = new_level != previous_level

    update_claim_corroboration(
        claim_id=claim_id,
        tenant_id=tenant_id,
        new_profile=new_profile,
        new_confidence_level=new_level,
        new_confidence_score=new_score,
    )

    logger.info(
        "Corroboration recorded: claim=%s tenant=%s actor=%s:%s "
        "independent=%s promoted=%s %s→%s",
        claim_id, tenant_id, corroborating_tenant_id, corroborating_actor_id,
        was_independent, promoted, previous_level, new_level,
    )

    return CorroborationResult(
        claim_id=claim_id,
        was_independent=was_independent,
        promoted=promoted,
        previous_level=previous_level,
        new_level=new_level,
        previous_score=previous_score,
        new_score=new_score,
        independent_sources=new_independent,
    )

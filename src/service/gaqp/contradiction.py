from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from src.service.gaqp.corpus import get_claim, update_claim_contradictions
from src.service.gaqp.exceptions import ClaimNotFoundError, SelfContradictionError
from src.service.gaqp.models import CorroborationProfile

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class ContradictionResult:
    claim_id: str
    contradicting_claim_id: str
    was_new_link: bool   # False → link already existed (contradict) or didn't exist (resolve)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _profile_from_row(row: Dict[str, Any]) -> CorroborationProfile:
    corr = row.get("corroboration_profile") or {}
    lca_raw = corr.get("last_corroborated_at")
    return CorroborationProfile(
        corroboration_count=corr.get("corroboration_count", 0),
        independent_sources=corr.get("independent_sources", 0),
        same_tenant_count=corr.get("same_tenant_count", 0),
        cross_tenant_count=corr.get("cross_tenant_count", 0),
        contradictions=corr.get("contradictions", 0),
        last_corroborated_at=datetime.fromisoformat(lca_raw) if lca_raw else None,
        corroborating_actors=list(corr.get("corroborating_actors") or []),
    )


def _with_contradictions_delta(profile: CorroborationProfile, delta: int) -> CorroborationProfile:
    """Return a new profile with contradictions count adjusted by delta (clamped to 0)."""
    new_count = max(0, profile.contradictions + delta)
    return CorroborationProfile(
        corroboration_count=profile.corroboration_count,
        independent_sources=profile.independent_sources,
        same_tenant_count=profile.same_tenant_count,
        cross_tenant_count=profile.cross_tenant_count,
        contradictions=new_count,
        last_corroborated_at=profile.last_corroborated_at,
        corroborating_actors=list(profile.corroborating_actors),
    )


# ---------------------------------------------------------------------------
# Engine entry points
# ---------------------------------------------------------------------------

def contradict(
    *,
    claim_id: str,
    contradicting_claim_id: str,
    tenant_id: str,
) -> ContradictionResult:
    """
    Register a bidirectional contradiction between two corpus claims.

    Both claims must belong to the same tenant. The link is idempotent:
    calling contradict() twice for the same pair is safe and returns
    was_new_link=False on the second call.

    Raises SelfContradictionError if claim_id == contradicting_claim_id.
    Raises ClaimNotFoundError if either claim is absent from the corpus.
    """
    if claim_id == contradicting_claim_id:
        raise SelfContradictionError(
            f"Claim {claim_id!r} cannot contradict itself."
        )

    row_a = get_claim(claim_id=claim_id, tenant_id=tenant_id)
    if row_a is None:
        raise ClaimNotFoundError(f"Claim {claim_id!r} not found for tenant {tenant_id!r}")

    row_b = get_claim(claim_id=contradicting_claim_id, tenant_id=tenant_id)
    if row_b is None:
        raise ClaimNotFoundError(
            f"Claim {contradicting_claim_id!r} not found for tenant {tenant_id!r}"
        )

    refs_a: List[str] = list(row_a.get("contradiction_refs") or [])
    refs_b: List[str] = list(row_b.get("contradiction_refs") or [])

    if contradicting_claim_id in refs_a:
        # Already linked — idempotent, no update needed.
        return ContradictionResult(
            claim_id=claim_id,
            contradicting_claim_id=contradicting_claim_id,
            was_new_link=False,
        )

    profile_a = _with_contradictions_delta(_profile_from_row(row_a), +1)
    profile_b = _with_contradictions_delta(_profile_from_row(row_b), +1)

    update_claim_contradictions(
        claim_id=claim_id,
        tenant_id=tenant_id,
        new_contradiction_refs=refs_a + [contradicting_claim_id],
        new_corroboration_profile=profile_a,
    )
    update_claim_contradictions(
        claim_id=contradicting_claim_id,
        tenant_id=tenant_id,
        new_contradiction_refs=refs_b + [claim_id],
        new_corroboration_profile=profile_b,
    )

    logger.info(
        "Contradiction linked: tenant=%s claim_a=%s claim_b=%s",
        tenant_id, claim_id, contradicting_claim_id,
    )

    return ContradictionResult(
        claim_id=claim_id,
        contradicting_claim_id=contradicting_claim_id,
        was_new_link=True,
    )


def resolve_contradiction(
    *,
    claim_id: str,
    contradicting_claim_id: str,
    tenant_id: str,
) -> ContradictionResult:
    """
    Remove a previously established contradiction link between two claims.

    Idempotent: resolving a link that doesn't exist returns was_new_link=False
    without error. Both claims must still exist in the corpus.

    Raises ClaimNotFoundError if either claim is absent from the corpus.
    """
    row_a = get_claim(claim_id=claim_id, tenant_id=tenant_id)
    if row_a is None:
        raise ClaimNotFoundError(f"Claim {claim_id!r} not found for tenant {tenant_id!r}")

    row_b = get_claim(claim_id=contradicting_claim_id, tenant_id=tenant_id)
    if row_b is None:
        raise ClaimNotFoundError(
            f"Claim {contradicting_claim_id!r} not found for tenant {tenant_id!r}"
        )

    refs_a: List[str] = list(row_a.get("contradiction_refs") or [])
    refs_b: List[str] = list(row_b.get("contradiction_refs") or [])

    if contradicting_claim_id not in refs_a:
        # Link doesn't exist — idempotent, nothing to remove.
        return ContradictionResult(
            claim_id=claim_id,
            contradicting_claim_id=contradicting_claim_id,
            was_new_link=False,
        )

    profile_a = _with_contradictions_delta(_profile_from_row(row_a), -1)
    profile_b = _with_contradictions_delta(_profile_from_row(row_b), -1)

    update_claim_contradictions(
        claim_id=claim_id,
        tenant_id=tenant_id,
        new_contradiction_refs=[r for r in refs_a if r != contradicting_claim_id],
        new_corroboration_profile=profile_a,
    )
    update_claim_contradictions(
        claim_id=contradicting_claim_id,
        tenant_id=tenant_id,
        new_contradiction_refs=[r for r in refs_b if r != claim_id],
        new_corroboration_profile=profile_b,
    )

    logger.info(
        "Contradiction resolved: tenant=%s claim_a=%s claim_b=%s",
        tenant_id, claim_id, contradicting_claim_id,
    )

    return ContradictionResult(
        claim_id=claim_id,
        contradicting_claim_id=contradicting_claim_id,
        was_new_link=True,
    )

from __future__ import annotations

import logging
import uuid
from collections import defaultdict
from datetime import UTC, datetime
from typing import Dict, List, Optional

from src.service.qualitative_capture.models import AtomicNugget, ExecutiveConclusion

logger = logging.getLogger(__name__)

# Minimum nuggets of the same type required to trigger reconstruction
_CLUSTER_THRESHOLD = 2

# Minimum confidence score for a nugget to be included in reconstruction
_CONFIDENCE_FLOOR = 0.50

# Rail card type mapping by claim type
_RAIL_CARD_TYPE: Dict[str, str] = {
    "risk": "risk",
    "threat": "risk",
    "opportunity": "opportunity",
    "doctrine": "executive_conclusion",
    "principle": "executive_conclusion",
    "objective": "executive_conclusion",
    "causal_claim": "executive_conclusion",
    "tradeoff": "executive_conclusion",
    "declaration_of_value": "executive_conclusion",
    "constraint": "executive_conclusion",
    "heuristic": "executive_conclusion",
    "threshold_condition": "executive_conclusion",
    "observation": "executive_conclusion",
}


def _polarity_for_cluster(nuggets: List[AtomicNugget]) -> str:
    counts: Dict[str, int] = defaultdict(int)
    for n in nuggets:
        counts[n.polarity] += 1
    return max(counts, key=counts.__getitem__)


def _conclusion_text(claim_type: str, nuggets: List[AtomicNugget]) -> str:
    top = sorted(nuggets, key=lambda n: n.confidence_score, reverse=True)[:3]
    excerpts = "; ".join(n.claim_text[:80] for n in top)
    label = claim_type.replace("_", " ").title()
    count = len(nuggets)
    return f"[{label}] {count} signal{'s' if count != 1 else ''} captured: {excerpts}"


def reconstruct_from_nuggets(
    nuggets: List[AtomicNugget],
    *,
    tenant_id: str,
    session_id: str,
    domain: str = "strategy",
) -> List[ExecutiveConclusion]:
    """
    Cluster high-signal nuggets into executive conclusions.

    Groups nuggets by claim_type. Each group that meets the cluster threshold
    and contains at least one rail-candidate nugget produces one conclusion.

    Returns an empty list when no cluster meets the threshold — normal outcome.
    """
    eligible = [n for n in nuggets if n.confidence_score >= _CONFIDENCE_FLOOR]
    if not eligible:
        return []

    clusters: Dict[str, List[AtomicNugget]] = defaultdict(list)
    for nugget in eligible:
        clusters[nugget.claim_type].append(nugget)

    conclusions: List[ExecutiveConclusion] = []
    now = datetime.now(UTC)

    for claim_type, cluster in clusters.items():
        if len(cluster) < _CLUSTER_THRESHOLD:
            continue
        if not any(n.rail_candidate for n in cluster):
            continue

        avg_confidence = sum(n.confidence_score for n in cluster) / len(cluster)
        rail_card_type = _RAIL_CARD_TYPE.get(claim_type, "executive_conclusion")
        polarity = _polarity_for_cluster(cluster)

        conclusion = ExecutiveConclusion(
            conclusion_id=uuid.uuid4().hex,
            tenant_id=tenant_id,
            session_id=session_id,
            conclusion_text=_conclusion_text(claim_type, cluster),
            source_nugget_ids=[n.nugget_id for n in cluster],
            claim_types_present=list({n.claim_type for n in cluster}),
            reconstruction_confidence=round(avg_confidence, 4),
            domain=domain,
            polarity=polarity,
            rail_card_type=rail_card_type,
            generated_at=now,
        )
        conclusions.append(conclusion)
        logger.debug(
            "QCR reconstruction: tenant=%s session=%s claim_type=%s nuggets=%d → conclusion=%s",
            tenant_id, session_id, claim_type, len(cluster), conclusion.conclusion_id,
        )

    return conclusions

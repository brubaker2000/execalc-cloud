from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Tuple

from src.service.gaqp.corpus import get_claim, list_claims
from src.service.gaqp.models import (
    ActivationBundle,
    ClaimProvenance,
    ContradictionAlert,
    CorroborationProfile,
    GAQPClaim,
)
from src.service.orchestration.models import ScenarioEnvelope

logger = logging.getLogger(__name__)

_DEFAULT_CONFIDENCE_FLOOR = 0.50  # Seed — include all admitted claims by default
_DEFAULT_MAX_CLAIMS = 20
_CORPUS_FETCH_LIMIT = 200  # fetch wide, filter in Python


def activate(
    *,
    scenario: ScenarioEnvelope,
    tenant_id: str,
    confidence_floor: float = _DEFAULT_CONFIDENCE_FLOOR,
    max_claims: int = _DEFAULT_MAX_CLAIMS,
) -> ActivationBundle:
    """
    Stage 9D activation engine: scenario in → ActivationBundle out.

    Queries the corpus for claims relevant to the incoming scenario and returns
    a bundle for surfacing alongside the DecisionReport. Never injected into
    DecisionReport — operator-visible, not silent.

    Matching strategy (v1 — deterministic, no embeddings):
    - Universal-scope claims always fire.
    - Other scopes fire when any activation_trigger keyword matches scenario text.
    - Sorted by confidence_score DESC, capped at max_claims.
    """
    try:
        candidates = _fetch_candidates(tenant_id, confidence_floor)
    except Exception:
        logger.exception("Corpus fetch failed during activation for tenant %s", tenant_id)
        return ActivationBundle(
            activated_claims=[],
            activation_rationale=[],
            corpus_scope="structural",
            confidence_floor=confidence_floor,
        )

    search_text = _build_search_text(scenario)
    matched: List[Tuple[Dict[str, Any], str]] = []

    for row in candidates:
        rationale = _match_rationale(row, search_text)
        if rationale:
            matched.append((row, rationale))

    matched.sort(key=lambda pair: pair[0].get("confidence_score", 0.0), reverse=True)
    matched = matched[:max_claims]

    contradiction_alerts = _build_contradiction_alerts(matched, tenant_id)

    return ActivationBundle(
        activated_claims=[_dict_to_claim(row) for row, _ in matched],
        activation_rationale=[r for _, r in matched],
        contradiction_alerts=contradiction_alerts,
        corpus_scope="structural",
        confidence_floor=confidence_floor,
    )


def _fetch_candidates(tenant_id: str, confidence_floor: float) -> List[Dict[str, Any]]:
    """
    Fetch admitted claims from all applicable scopes, deduplicated by claim_id.

    private + tenant: scoped to this tenant.
    structural: cross-tenant de-identified claims.
    """
    seen: set = set()
    candidates: List[Dict[str, Any]] = []

    for scope in ("private", "tenant", "structural"):
        rows = list_claims(
            tenant_id=tenant_id,
            corpus_scope=scope,
            confidence_floor=confidence_floor,
            limit=_CORPUS_FETCH_LIMIT,
        )
        for row in rows:
            cid = row["claim_id"]
            if cid not in seen:
                seen.add(cid)
                candidates.append(row)

    return candidates


def _build_search_text(scenario: ScenarioEnvelope) -> str:
    """Combine scenario fields into a single lowercase search surface."""
    parts = [scenario.scenario_type, scenario.governing_objective, scenario.prompt]
    return " ".join(p for p in parts if p).lower()


def _match_rationale(row: Dict[str, Any], search_text: str) -> Optional[str]:
    """
    Return a rationale string if the claim activates for this scenario, None otherwise.

    Universal scope always fires. Other scopes require a trigger keyword match.
    """
    activation_scope: str = row.get("activation_scope", "")
    triggers: List[str] = row.get("activation_triggers") or []

    if activation_scope == "universal":
        return "Universal activation: claim fires on all scenarios."

    for trigger in triggers:
        if trigger.lower() in search_text:
            return f'Trigger match: "{trigger}" found in scenario context.'

    return None


def _build_contradiction_alerts(
    matched: List[Tuple[Dict[str, Any], str]],
    tenant_id: str,
) -> List[ContradictionAlert]:
    """
    For each activated claim that carries contradiction_refs, fetch the
    contradicting claims and build ContradictionAlert objects.

    Errors fetching individual refs are logged and skipped — a missing ref
    does not abort the activation.
    """
    alerts: List[ContradictionAlert] = []
    for row, _ in matched:
        refs: List[str] = row.get("contradiction_refs") or []
        for ref_id in refs:
            try:
                contra_row = get_claim(claim_id=ref_id, tenant_id=tenant_id)
                if contra_row:
                    alerts.append(ContradictionAlert(
                        activated_claim_id=row["claim_id"],
                        contradicting_claim=_dict_to_claim(contra_row),
                    ))
                else:
                    logger.warning(
                        "Contradiction ref %r not found in corpus for tenant %s (claim %s)",
                        ref_id, tenant_id, row["claim_id"],
                    )
            except Exception:
                logger.exception(
                    "Failed to fetch contradiction ref %r for claim %s tenant %s",
                    ref_id, row["claim_id"], tenant_id,
                )
    return alerts


def _parse_dt(value: Optional[str]) -> datetime:
    if value:
        return datetime.fromisoformat(value)
    return datetime.now(UTC)


def _dict_to_claim(row: Dict[str, Any]) -> GAQPClaim:
    """Reconstruct a GAQPClaim from a corpus row dict."""
    prov_raw: Dict[str, Any] = row.get("provenance") or {}
    provenance = ClaimProvenance(
        source_kind=prov_raw.get("source_kind", "unknown"),
        source_ref=prov_raw.get("source_ref", ""),
        actor_id=prov_raw.get("actor_id", ""),
        envelope_id=prov_raw.get("envelope_id"),
        origin_surface=prov_raw.get("origin_surface"),
    )

    corr_raw: Dict[str, Any] = row.get("corroboration_profile") or {}
    lca_raw = corr_raw.get("last_corroborated_at")
    corroboration_profile = CorroborationProfile(
        corroboration_count=corr_raw.get("corroboration_count", 0),
        independent_sources=corr_raw.get("independent_sources", 0),
        same_tenant_count=corr_raw.get("same_tenant_count", 0),
        cross_tenant_count=corr_raw.get("cross_tenant_count", 0),
        contradictions=corr_raw.get("contradictions", 0),
        last_corroborated_at=datetime.fromisoformat(lca_raw) if lca_raw else None,
        corroborating_actors=list(corr_raw.get("corroborating_actors") or []),
    )

    return GAQPClaim(
        claim_id=row["claim_id"],
        tenant_id=row["tenant_id"],
        source_envelope_id=row["source_envelope_id"],
        claim_type=row["claim_type"],
        domain=row["domain"],
        content=row["content"],
        confidence_level=row["confidence_level"],
        confidence_score=row["confidence_score"],
        admission_status=row["admission_status"],
        corpus_scope=row["corpus_scope"],
        extraction_method=row["extraction_method"],
        provenance=provenance,
        activation_scope=row["activation_scope"],
        activation_triggers=list(row.get("activation_triggers") or []),
        corroboration_profile=corroboration_profile,
        contradiction_refs=list(row.get("contradiction_refs") or []),
        support_refs=list(row.get("support_refs") or []),
        fingerprint=row.get("fingerprint", ""),
        schema_version=row.get("schema_version", "stage9_v1"),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )

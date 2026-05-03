from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.service.decision_loop.models import DecisionReport
from src.service.gaqp.models import (
    CONFIDENCE_SCORE,
    SCHEMA_VERSION,
    ActivationScope,
    AdmissionStatus,
    ClaimProvenance,
    ClaimType,
    CorroborationProfile,
    Domain,
    GAQPClaim,
    compute_fingerprint,
)

# ---------------------------------------------------------------------------
# Admission test engine
# ---------------------------------------------------------------------------

_MIN_CONTENT_LENGTH = 20

_EPHEMERAL_MARKERS = (
    "today", "yesterday", "this week", "this month",
    "right now", "currently pending", "as of now",
)

_BOILERPLATE_PREFIXES = (
    "n/a", "not applicable", "none identified", "no major",
    "no significant", "standard analysis", "see above",
)


@dataclass
class AdmissionResult:
    admission_status: AdmissionStatus
    failed_tests: List[str]

    @property
    def admitted(self) -> bool:
        return self.admission_status == "admitted"


def _run_admission_tests(content: str) -> AdmissionResult:
    """
    Sequential application of the seven GAQP admission tests.

    Tests 1-4 failure → rejected (hard gate).
    Tests 5-7 failure → needs_review (held for operator evaluation).
    Per GAQP_ADMISSION_TESTS.md: failure at Test 1 terminates evaluation.
    """
    stripped = (content or "").strip()
    lower = stripped.lower()
    failed: List[str] = []

    # Test 1 — Stand-Alone: must have sufficient standalone meaning
    if len(stripped) < _MIN_CONTENT_LENGTH:
        return AdmissionResult("rejected", ["stand_alone"])
    if any(lower.startswith(p) for p in _BOILERPLATE_PREFIXES):
        return AdmissionResult("rejected", ["stand_alone"])

    # Test 2 — Disputability: pure questions are not assertions
    if stripped.endswith("?"):
        failed.append("disputability")

    # Test 3 — Governance: always passes for direct-field extraction
    # (claim_type and provenance are assigned by the extractor)

    # Test 4 — Activation: always passes for direct-field extraction
    # (activation_triggers are assigned from the field map)

    # Test 5 — Durability: reject obviously ephemeral content
    if any(m in lower for m in _EPHEMERAL_MARKERS):
        failed.append("durability")

    # Test 6 — Composability: always passes in v1

    # Test 7 — Non-Triviality: content must carry interpretive weight
    # Proxy: below a secondary length floor signals low information density
    if len(stripped) < 40:
        failed.append("non_triviality")

    if not failed:
        return AdmissionResult("admitted", [])

    # Tests 2-4 failures are blocking (rejected); 5-7 are non-blocking (needs_review)
    blocking = {"disputability"}
    if any(t in blocking for t in failed):
        return AdmissionResult("rejected", failed)

    return AdmissionResult("needs_review", failed)


# ---------------------------------------------------------------------------
# Extraction surface map
# Per STAGE_9A0_ARCHITECTURE_LOCK.md — direct field extraction only in v1.
# ---------------------------------------------------------------------------

# Each entry: (content_accessor, claim_type, domain, base_activation_triggers, activation_scope)
_SCALAR_FIELDS: List[Tuple[
    Callable[[DecisionReport], Optional[str]],
    str,   # claim_type
    str,   # domain
    List[str],  # base activation triggers
    str,   # activation_scope
]] = [
    (
        lambda r: r.value_assessment,
        "tradeoff", "strategy",
        ["value_assessment", "governing_objective"],
        "situational",
    ),
    (
        lambda r: r.risk_reward_assessment,
        "tradeoff", "strategy",
        ["risk_reward_assessment", "risk_decision"],
        "situational",
    ),
    (
        lambda r: r.supply_demand_assessment,
        "causal_claim", "strategy",
        ["supply_demand_assessment", "market_analysis"],
        "situational",
    ),
    (
        lambda r: r.asset_assessment,
        "strength", "strategy",
        ["asset_assessment", "capability_review"],
        "situational",
    ),
    (
        lambda r: r.liability_assessment,
        "weakness", "strategy",
        ["liability_assessment", "constraint_review"],
        "situational",
    ),
]

# Each entry: (list_accessor, claim_type, domain, base_activation_triggers, activation_scope)
_LIST_FIELDS: List[Tuple[
    Callable[[DecisionReport], List[str]],
    str,
    str,
    List[str],
    str,
]] = [
    (
        lambda r: r.incentives,
        "objective", "strategy",
        ["incentive_analysis", "stakeholder_alignment"],
        "situational",
    ),
    (
        lambda r: r.asymmetries,
        "causal_claim", "strategy",
        ["asymmetry_analysis", "leverage_assessment"],
        "situational",
    ),
    (
        lambda r: (r.tradeoffs or {}).get("key_tradeoffs") or [],
        "tradeoff", "strategy",
        ["tradeoff_analysis", "key_tradeoffs"],
        "situational",
    ),
    (
        lambda r: r.confidence_rationale,
        "observation", "strategy",
        ["confidence_review", "rationale_audit"],
        "situational",
    ),
]


# ---------------------------------------------------------------------------
# Claim builder
# ---------------------------------------------------------------------------

def _build_claim(
    *,
    content: str,
    claim_type: str,
    domain: str,
    base_triggers: List[str],
    activation_scope: str,
    admission: AdmissionResult,
    tenant_id: str,
    source_envelope_id: str,
    actor_id: str,
    governing_objective: Optional[str],
    scenario_type: Optional[str],
) -> GAQPClaim:
    # Enrich activation triggers with scenario context
    triggers = list(base_triggers)
    if governing_objective and governing_objective not in ("unspecified_objective", "unspecified", ""):
        triggers.append(f"objective:{governing_objective}")
    if scenario_type and scenario_type not in ("general", ""):
        triggers.append(f"scenario:{scenario_type}")

    fp = compute_fingerprint(
        tenant_id=tenant_id,
        source_envelope_id=source_envelope_id,
        claim_type=claim_type,
        content=content,
        activation_scope=activation_scope,
    )

    return GAQPClaim(
        claim_id=uuid.uuid4().hex,
        tenant_id=tenant_id,
        source_envelope_id=source_envelope_id,
        claim_type=claim_type,  # type: ignore[arg-type]
        domain=domain,  # type: ignore[arg-type]
        content=content,
        confidence_level="seed",
        confidence_score=CONFIDENCE_SCORE["seed"],
        admission_status=admission.admission_status,
        corpus_scope="tenant",
        extraction_method="direct_field",
        provenance=ClaimProvenance(
            source_kind="decision_artifact",
            source_ref=source_envelope_id,
            actor_id=actor_id,
            envelope_id=source_envelope_id,
            origin_surface="extraction_pipeline",
        ),
        activation_scope=activation_scope,  # type: ignore[arg-type]
        activation_triggers=triggers,
        corroboration_profile=CorroborationProfile(),
        fingerprint=fp,
    )


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def extract_claims(
    *,
    report: DecisionReport,
    tenant_id: str,
    source_envelope_id: str,
    actor_id: str,
) -> List[GAQPClaim]:
    """
    Stage 9B extraction pipeline.

    Extracts GAQP claim candidates from a DecisionReport and runs each
    through the admission test suite. Returns all claims regardless of
    admission_status — callers filter by status as needed.

    The corpus persistence layer (9C) writes only admitted claims.
    needs_review claims are held for operator evaluation.
    rejected claims are discarded after logging.
    """
    audit = report.audit or {}
    governing_objective = str(audit.get("governing_objective") or report.governing_objective or "")
    scenario_type = str(audit.get("scenario_type") or "")

    claims: List[GAQPClaim] = []

    # Scalar fields — one candidate per field
    for accessor, claim_type, domain, triggers, scope in _SCALAR_FIELDS:
        content = accessor(report)
        if not content:
            continue
        admission = _run_admission_tests(content)
        claims.append(_build_claim(
            content=content,
            claim_type=claim_type,
            domain=domain,
            base_triggers=triggers,
            activation_scope=scope,
            admission=admission,
            tenant_id=tenant_id,
            source_envelope_id=source_envelope_id,
            actor_id=actor_id,
            governing_objective=governing_objective,
            scenario_type=scenario_type,
        ))

    # List fields — one candidate per list item
    for accessor, claim_type, domain, triggers, scope in _LIST_FIELDS:
        items = accessor(report)
        if not items:
            continue
        for item in items:
            content = str(item).strip() if item else ""
            if not content:
                continue
            admission = _run_admission_tests(content)
            claims.append(_build_claim(
                content=content,
                claim_type=claim_type,
                domain=domain,
                base_triggers=triggers,
                activation_scope=scope,
                admission=admission,
                tenant_id=tenant_id,
                source_envelope_id=source_envelope_id,
                actor_id=actor_id,
                governing_objective=governing_objective,
                scenario_type=scenario_type,
            ))

    return claims


def admitted_claims(claims: List[GAQPClaim]) -> List[GAQPClaim]:
    """Filter to admitted claims only — these are corpus-ready."""
    return [c for c in claims if c.admission_status == "admitted"]


def needs_review_claims(claims: List[GAQPClaim]) -> List[GAQPClaim]:
    """Filter to needs_review claims — held for operator evaluation."""
    return [c for c in claims if c.admission_status == "needs_review"]

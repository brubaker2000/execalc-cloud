from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict, List, Literal, Optional

# ---------------------------------------------------------------------------
# Canonical enumerations
# ---------------------------------------------------------------------------

ClaimType = Literal[
    "axiom",
    "definition",
    "ontological_assertion",
    "principle",
    "doctrine",
    "heuristic",
    "best_practice",
    "tendency",
    "observation",
    "event",
    "institutional_precedent",
    "constraint",
    "threshold_condition",
    "objective",
    "tradeoff",
    "causal_claim",
    "declaration_of_value",
    "diagnostic_signal",
    "stakeholder_complaint",
    "tactic",
    "strength",
    "weakness",
    "threat",
    "opportunity",
]

CLAIM_TYPES: List[str] = [
    "axiom", "definition", "ontological_assertion", "principle", "doctrine",
    "heuristic", "best_practice", "tendency", "observation", "event",
    "institutional_precedent", "constraint", "threshold_condition", "objective",
    "tradeoff", "causal_claim", "declaration_of_value", "diagnostic_signal",
    "stakeholder_complaint", "tactic", "strength", "weakness", "threat",
    "opportunity",
]

ConfidenceLevel = Literal["seed", "developing", "strong", "structural", "disputed"]
AdmissionStatus = Literal["admitted", "rejected", "needs_review", "candidate"]
CorpusScope = Literal["private", "tenant", "structural"]
ActivationScope = Literal["universal", "domain_specific", "situational", "tenant_specific"]
ExtractionMethod = Literal["direct_field", "llm_decomposed", "operator_memoralized"]
Domain = Literal["strategy", "capital", "operations", "human_behavior", "governance"]

# GAQP confidence ladder — Triangulation operationalized.
# Seed=first occurrence, Developing=second independent, Strong=three-point,
# Structural=institutional doctrine. Aligns exactly with the Polymorphia
# triangulation framework.
CONFIDENCE_SCORE: Dict[str, float] = {
    "seed": 0.50,
    "developing": 0.72,
    "strong": 0.91,
    "structural": 1.00,
}

SCHEMA_VERSION = "stage9_v1"


# ---------------------------------------------------------------------------
# Supporting objects
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ClaimProvenance:
    source_kind: str              # decision_artifact / operator_input / operator_memoralized
    source_ref: str               # envelope_id or named reference
    actor_id: str                 # user_id or system actor
    envelope_id: Optional[str] = None
    origin_surface: Optional[str] = None  # api / orchestration / memoralize

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "actor_id": self.actor_id,
            "envelope_id": self.envelope_id,
            "origin_surface": self.origin_surface,
        }


@dataclass(frozen=True)
class CorroborationProfile:
    """
    Tracks independent evidence, not raw repetition.
    confidence_score advances only when independent_sources increases.
    corroborating_actors stores "tenant_id:actor_id" keys seen so far —
    used by the promotion engine to determine independence without a
    separate events table.
    """
    corroboration_count: int = 0
    independent_sources: int = 0      # distinct tenant+user combinations
    same_tenant_count: int = 0        # within-tenant corroborations
    cross_tenant_count: int = 0       # structural-tier cross-tenant matches
    contradictions: int = 0           # active contradicting claims
    last_corroborated_at: Optional[datetime] = None
    corroborating_actors: List[str] = field(default_factory=list)  # "tid:uid" keys

    def to_dict(self) -> Dict[str, Any]:
        return {
            "corroboration_count": self.corroboration_count,
            "independent_sources": self.independent_sources,
            "same_tenant_count": self.same_tenant_count,
            "cross_tenant_count": self.cross_tenant_count,
            "contradictions": self.contradictions,
            "last_corroborated_at": (
                self.last_corroborated_at.isoformat()
                if self.last_corroborated_at else None
            ),
            "corroborating_actors": list(self.corroborating_actors),
        }


# ---------------------------------------------------------------------------
# Fingerprint computation
# ---------------------------------------------------------------------------

def compute_fingerprint(
    *,
    tenant_id: str,
    source_envelope_id: str,
    claim_type: str,
    content: str,
    activation_scope: str,
    schema_version: str = SCHEMA_VERSION,
) -> str:
    """
    Deterministic fingerprint for idempotent corpus admission.
    Running the extraction pipeline twice against the same source
    produces the same fingerprint — duplicate insertion is skipped.
    """
    normalized_content = " ".join(content.strip().lower().split())
    key = json.dumps([
        tenant_id,
        source_envelope_id,
        claim_type,
        normalized_content,
        activation_scope,
        schema_version,
    ], separators=(",", ":"))
    return hashlib.sha256(key.encode()).hexdigest()


# ---------------------------------------------------------------------------
# GAQPClaim — the canonical atomic unit of qualitative intelligence
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GAQPClaim:
    """
    The atomic unit of GAQP corpus intelligence.

    Every claim in the corpus has:
    - passed the seven GAQP admission tests
    - a deterministic fingerprint (idempotent backfill)
    - a corroboration profile (truth, not repetition)
    - tenant-scoped visibility
    - contradiction and support references (Polymorphia: holds tension)
    """

    # Identity
    claim_id: str
    tenant_id: str
    source_envelope_id: str

    # Classification
    claim_type: ClaimType
    domain: Domain
    content: str                          # self-contained claim text

    # Confidence — GAQP ladder governs
    confidence_level: ConfidenceLevel
    confidence_score: float               # 0.50 / 0.72 / 0.91 / 1.00

    # Governance
    admission_status: AdmissionStatus
    corpus_scope: CorpusScope            # private / tenant / structural
    extraction_method: ExtractionMethod

    # Provenance
    provenance: ClaimProvenance

    # Activation
    activation_scope: ActivationScope
    activation_triggers: List[str] = field(default_factory=list)

    # Corroboration and contradiction
    corroboration_profile: CorroborationProfile = field(
        default_factory=CorroborationProfile
    )
    contradiction_refs: List[str] = field(default_factory=list)  # claim_ids
    support_refs: List[str] = field(default_factory=list)         # claim_ids

    # Idempotency
    fingerprint: str = ""

    # Versioning
    schema_version: str = SCHEMA_VERSION

    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "tenant_id": self.tenant_id,
            "source_envelope_id": self.source_envelope_id,
            "claim_type": self.claim_type,
            "domain": self.domain,
            "content": self.content,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "admission_status": self.admission_status,
            "corpus_scope": self.corpus_scope,
            "extraction_method": self.extraction_method,
            "provenance": self.provenance.to_dict(),
            "activation_scope": self.activation_scope,
            "activation_triggers": self.activation_triggers,
            "corroboration_profile": self.corroboration_profile.to_dict(),
            "contradiction_refs": self.contradiction_refs,
            "support_refs": self.support_refs,
            "fingerprint": self.fingerprint,
            "schema_version": self.schema_version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# ContradictionAlert — a conflict surfaced alongside activated claims
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ContradictionAlert:
    """
    Surfaces a contradiction between an activated claim and a corpus claim
    that disputes it. Included in ActivationBundle for operator visibility.
    """
    activated_claim_id: str
    contradicting_claim: "GAQPClaim"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "activated_claim_id": self.activated_claim_id,
            "contradicting_claim": self.contradicting_claim.to_dict(),
        }


# ---------------------------------------------------------------------------
# ActivationBundle — activated corpus intelligence surfaced beside a decision
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ActivationBundle:
    """
    The output of the Stage 9D activation engine.

    Surfaced alongside DecisionReport in the orchestration rail.
    Never injected into DecisionReport itself — operator-visible, not silent.
    """
    activated_claims: List[GAQPClaim]
    activation_rationale: List[str]   # one entry per claim, why it matched
    corpus_scope: CorpusScope
    confidence_floor: float           # minimum score threshold used for retrieval
    contradiction_alerts: List[ContradictionAlert] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "activated_claims": [c.to_dict() for c in self.activated_claims],
            "activation_rationale": self.activation_rationale,
            "corpus_scope": self.corpus_scope,
            "confidence_floor": self.confidence_floor,
            "contradiction_alerts": [a.to_dict() for a in self.contradiction_alerts],
        }

    @property
    def is_empty(self) -> bool:
        return len(self.activated_claims) == 0

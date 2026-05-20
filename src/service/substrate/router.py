from __future__ import annotations

from src.service.substrate.interface import (
    CoverageLevel,
    ModelTier,
    SubstrateCallClass,
)

# Selection policy matrix: (call_class, coverage) -> tier
# Rows: call class. Columns: FULL, PARTIAL, MINIMAL.
_POLICY: dict[tuple[SubstrateCallClass, CoverageLevel], ModelTier] = {
    (SubstrateCallClass.CONVERSATIONAL,      CoverageLevel.FULL):    ModelTier.ECONOMY,
    (SubstrateCallClass.CONVERSATIONAL,      CoverageLevel.PARTIAL): ModelTier.ECONOMY,
    (SubstrateCallClass.CONVERSATIONAL,      CoverageLevel.MINIMAL): ModelTier.ECONOMY,

    (SubstrateCallClass.CLASSIFICATION,      CoverageLevel.FULL):    ModelTier.ECONOMY,
    (SubstrateCallClass.CLASSIFICATION,      CoverageLevel.PARTIAL): ModelTier.STANDARD,
    (SubstrateCallClass.CLASSIFICATION,      CoverageLevel.MINIMAL): ModelTier.STANDARD,

    (SubstrateCallClass.CORPUS_RETRIEVAL,    CoverageLevel.FULL):    ModelTier.ECONOMY,
    (SubstrateCallClass.CORPUS_RETRIEVAL,    CoverageLevel.PARTIAL): ModelTier.STANDARD,
    (SubstrateCallClass.CORPUS_RETRIEVAL,    CoverageLevel.MINIMAL): ModelTier.STANDARD,

    (SubstrateCallClass.STRUCTURED_SYNTHESIS, CoverageLevel.FULL):   ModelTier.STANDARD,
    (SubstrateCallClass.STRUCTURED_SYNTHESIS, CoverageLevel.PARTIAL):ModelTier.CAPABLE,
    (SubstrateCallClass.STRUCTURED_SYNTHESIS, CoverageLevel.MINIMAL):ModelTier.CAPABLE,

    (SubstrateCallClass.ACTION_FRAMING,      CoverageLevel.FULL):    ModelTier.STANDARD,
    (SubstrateCallClass.ACTION_FRAMING,      CoverageLevel.PARTIAL): ModelTier.CAPABLE,
    (SubstrateCallClass.ACTION_FRAMING,      CoverageLevel.MINIMAL): ModelTier.CAPABLE,

    (SubstrateCallClass.EXECUTION_GATE,      CoverageLevel.FULL):    ModelTier.CAPABLE,
    (SubstrateCallClass.EXECUTION_GATE,      CoverageLevel.PARTIAL): ModelTier.CAPABLE,
    (SubstrateCallClass.EXECUTION_GATE,      CoverageLevel.MINIMAL): ModelTier.CAPABLE,

    (SubstrateCallClass.AUDIT_NARRATION,     CoverageLevel.FULL):    ModelTier.ECONOMY,
    (SubstrateCallClass.AUDIT_NARRATION,     CoverageLevel.PARTIAL): ModelTier.ECONOMY,
    (SubstrateCallClass.AUDIT_NARRATION,     CoverageLevel.MINIMAL): ModelTier.STANDARD,
}

# Hard overrides: these call classes always route to CAPABLE regardless of coverage.
_CAPABLE_ALWAYS = {SubstrateCallClass.EXECUTION_GATE}


def select_tier(
    call_class: SubstrateCallClass,
    coverage: CoverageLevel,
    override_tier: ModelTier | None = None,
    risk_level: str | None = None,
    tenant_governance_posture: str | None = None,
) -> ModelTier:
    if call_class in _CAPABLE_ALWAYS:
        return ModelTier.CAPABLE

    if risk_level in ("HIGH", "CRITICAL"):
        return ModelTier.CAPABLE

    if tenant_governance_posture in ("ELEVATED", "MAXIMUM"):
        return ModelTier.CAPABLE

    policy_tier = _POLICY.get((call_class, coverage), ModelTier.STANDARD)

    if override_tier is not None:
        # Override may only escalate, never de-escalate below policy minimum.
        tier_rank = {ModelTier.ECONOMY: 0, ModelTier.STANDARD: 1, ModelTier.CAPABLE: 2}
        return override_tier if tier_rank[override_tier] >= tier_rank[policy_tier] else policy_tier

    return policy_tier

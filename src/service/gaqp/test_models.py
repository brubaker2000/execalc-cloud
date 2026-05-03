from __future__ import annotations

import uuid
from datetime import UTC, datetime

from src.service.gaqp.models import (
    ActivationBundle,
    ClaimProvenance,
    CorroborationProfile,
    GAQPClaim,
    CLAIM_TYPES,
    CONFIDENCE_SCORE,
    SCHEMA_VERSION,
    compute_fingerprint,
)


def _make_provenance() -> ClaimProvenance:
    return ClaimProvenance(
        source_kind="decision_artifact",
        source_ref="envelope_abc123",
        actor_id="user_001",
        envelope_id="envelope_abc123",
        origin_surface="orchestration",
    )


def _make_claim(**overrides) -> GAQPClaim:
    defaults = dict(
        claim_id=uuid.uuid4().hex,
        tenant_id="tenant_001",
        source_envelope_id="envelope_abc123",
        claim_type="tradeoff",
        domain="strategy",
        content="Speed and certainty cannot be fully optimized simultaneously.",
        confidence_level="seed",
        confidence_score=0.50,
        admission_status="admitted",
        corpus_scope="tenant",
        extraction_method="direct_field",
        provenance=_make_provenance(),
        activation_scope="situational",
        activation_triggers=["time_constrained_decision"],
        fingerprint=compute_fingerprint(
            tenant_id="tenant_001",
            source_envelope_id="envelope_abc123",
            claim_type="tradeoff",
            content="Speed and certainty cannot be fully optimized simultaneously.",
            activation_scope="situational",
        ),
    )
    defaults.update(overrides)
    return GAQPClaim(**defaults)


class TestConfidenceLadder:
    def test_scores_match_gaqp_ladder(self):
        assert CONFIDENCE_SCORE["seed"] == 0.50
        assert CONFIDENCE_SCORE["developing"] == 0.72
        assert CONFIDENCE_SCORE["strong"] == 0.91
        assert CONFIDENCE_SCORE["structural"] == 1.00

    def test_scores_are_ordered(self):
        scores = list(CONFIDENCE_SCORE.values())
        assert scores == sorted(scores)


class TestClaimTypes:
    def test_24_canonical_types(self):
        assert len(CLAIM_TYPES) == 24

    def test_swot_types_present(self):
        for t in ("strength", "weakness", "threat", "opportunity"):
            assert t in CLAIM_TYPES

    def test_no_duplicates(self):
        assert len(CLAIM_TYPES) == len(set(CLAIM_TYPES))


class TestComputeFingerprint:
    def test_deterministic(self):
        fp1 = compute_fingerprint(
            tenant_id="t1",
            source_envelope_id="env1",
            claim_type="tradeoff",
            content="Speed vs certainty.",
            activation_scope="situational",
        )
        fp2 = compute_fingerprint(
            tenant_id="t1",
            source_envelope_id="env1",
            claim_type="tradeoff",
            content="Speed vs certainty.",
            activation_scope="situational",
        )
        assert fp1 == fp2

    def test_whitespace_normalized(self):
        fp1 = compute_fingerprint(
            tenant_id="t1", source_envelope_id="e1",
            claim_type="axiom", content="Speed vs certainty.",
            activation_scope="universal",
        )
        fp2 = compute_fingerprint(
            tenant_id="t1", source_envelope_id="e1",
            claim_type="axiom", content="  Speed  vs  certainty.  ",
            activation_scope="universal",
        )
        assert fp1 == fp2

    def test_different_tenants_differ(self):
        fp1 = compute_fingerprint(
            tenant_id="t1", source_envelope_id="e1",
            claim_type="axiom", content="Same claim.",
            activation_scope="universal",
        )
        fp2 = compute_fingerprint(
            tenant_id="t2", source_envelope_id="e1",
            claim_type="axiom", content="Same claim.",
            activation_scope="universal",
        )
        assert fp1 != fp2

    def test_different_content_differs(self):
        fp1 = compute_fingerprint(
            tenant_id="t1", source_envelope_id="e1",
            claim_type="axiom", content="Claim A.",
            activation_scope="universal",
        )
        fp2 = compute_fingerprint(
            tenant_id="t1", source_envelope_id="e1",
            claim_type="axiom", content="Claim B.",
            activation_scope="universal",
        )
        assert fp1 != fp2


class TestGAQPClaim:
    def test_construction(self):
        claim = _make_claim()
        assert claim.claim_type == "tradeoff"
        assert claim.confidence_score == 0.50
        assert claim.admission_status == "admitted"
        assert claim.corpus_scope == "tenant"

    def test_immutable(self):
        claim = _make_claim()
        try:
            claim.content = "mutated"  # type: ignore
            assert False, "Should have raised"
        except (AttributeError, TypeError):
            pass

    def test_to_dict_complete(self):
        claim = _make_claim()
        d = claim.to_dict()
        required_keys = [
            "claim_id", "tenant_id", "source_envelope_id", "claim_type",
            "domain", "content", "confidence_level", "confidence_score",
            "admission_status", "corpus_scope", "extraction_method",
            "provenance", "activation_scope", "activation_triggers",
            "corroboration_profile", "contradiction_refs", "support_refs",
            "fingerprint", "schema_version", "created_at", "updated_at",
        ]
        for key in required_keys:
            assert key in d, f"Missing key: {key}"

    def test_schema_version(self):
        claim = _make_claim()
        assert claim.schema_version == SCHEMA_VERSION

    def test_default_corroboration_profile(self):
        claim = _make_claim()
        assert claim.corroboration_profile.corroboration_count == 0
        assert claim.corroboration_profile.independent_sources == 0
        assert claim.corroboration_profile.contradictions == 0

    def test_default_refs_empty(self):
        claim = _make_claim()
        assert claim.contradiction_refs == []
        assert claim.support_refs == []


class TestCorroborationProfile:
    def test_independence_tracked_separately(self):
        profile = CorroborationProfile(
            corroboration_count=5,
            independent_sources=2,
            same_tenant_count=3,
            cross_tenant_count=0,
            contradictions=0,
        )
        assert profile.corroboration_count == 5
        assert profile.independent_sources == 2

    def test_to_dict(self):
        profile = CorroborationProfile(corroboration_count=1, independent_sources=1)
        d = profile.to_dict()
        assert d["corroboration_count"] == 1
        assert d["independent_sources"] == 1
        assert d["last_corroborated_at"] is None


class TestActivationBundle:
    def test_empty_bundle(self):
        bundle = ActivationBundle(
            activated_claims=[],
            activation_rationale=[],
            corpus_scope="tenant",
            confidence_floor=0.50,
        )
        assert bundle.is_empty

    def test_nonempty_bundle(self):
        claim = _make_claim()
        bundle = ActivationBundle(
            activated_claims=[claim],
            activation_rationale=["Matched claim_type=tradeoff + activation_scope=situational"],
            corpus_scope="tenant",
            confidence_floor=0.50,
        )
        assert not bundle.is_empty
        assert len(bundle.activated_claims) == 1

    def test_to_dict(self):
        bundle = ActivationBundle(
            activated_claims=[],
            activation_rationale=[],
            corpus_scope="structural",
            confidence_floor=0.72,
        )
        d = bundle.to_dict()
        assert d["corpus_scope"] == "structural"
        assert d["confidence_floor"] == 0.72
        assert d["activated_claims"] == []

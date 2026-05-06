from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import MagicMock, call, patch

import pytest

from src.service.gaqp.corroboration import (
    ClaimNotFoundError,
    CorroborationResult,
    _actor_key,
    _compute_confidence,
    corroborate,
)
from src.service.gaqp.models import (
    CONFIDENCE_SCORE,
    ClaimProvenance,
    CorroborationProfile,
    GAQPClaim,
    compute_fingerprint,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_corpus_row(
    *,
    claim_id: str = "claim_abc",
    tenant_id: str = "tenant_001",
    confidence_level: str = "seed",
    confidence_score: float = CONFIDENCE_SCORE["seed"],
    corroboration_profile: dict | None = None,
) -> dict:
    """Minimal corpus row dict as returned by get_claim()."""
    return {
        "claim_id": claim_id,
        "tenant_id": tenant_id,
        "source_envelope_id": "env_001",
        "claim_type": "tradeoff",
        "domain": "strategy",
        "content": "Speed and certainty cannot be fully optimized simultaneously.",
        "confidence_level": confidence_level,
        "confidence_score": confidence_score,
        "admission_status": "admitted",
        "corpus_scope": "tenant",
        "extraction_method": "direct_field",
        "provenance": {
            "source_kind": "decision_artifact",
            "source_ref": "env_001",
            "actor_id": "user_001",
            "envelope_id": "env_001",
            "origin_surface": "extraction_pipeline",
        },
        "activation_scope": "situational",
        "activation_triggers": ["tradeoff_analysis"],
        "corroboration_profile": corroboration_profile or {
            "corroboration_count": 0,
            "independent_sources": 0,
            "same_tenant_count": 0,
            "cross_tenant_count": 0,
            "contradictions": 0,
            "last_corroborated_at": None,
            "corroborating_actors": [],
        },
        "contradiction_refs": [],
        "support_refs": [],
        "fingerprint": "fp_abc123",
        "schema_version": "stage9_v1",
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat(),
    }


# ---------------------------------------------------------------------------
# _compute_confidence — pure, no I/O
# ---------------------------------------------------------------------------

class TestComputeConfidence:
    def test_zero_independent_sources_is_seed(self):
        level, score = _compute_confidence(0)
        assert level == "seed"
        assert score == CONFIDENCE_SCORE["seed"]

    def test_one_independent_source_is_developing(self):
        level, score = _compute_confidence(1)
        assert level == "developing"
        assert score == CONFIDENCE_SCORE["developing"]

    def test_two_independent_sources_is_strong(self):
        level, score = _compute_confidence(2)
        assert level == "strong"
        assert score == CONFIDENCE_SCORE["strong"]

    def test_three_or_more_still_strong(self):
        for n in (3, 5, 10):
            level, score = _compute_confidence(n)
            assert level == "strong", f"Expected strong for {n} sources"
            assert score == CONFIDENCE_SCORE["strong"]

    def test_never_returns_structural(self):
        for n in range(10):
            level, _ = _compute_confidence(n)
            assert level != "structural"

    def test_scores_increase_with_sources(self):
        _, s0 = _compute_confidence(0)
        _, s1 = _compute_confidence(1)
        _, s2 = _compute_confidence(2)
        assert s0 < s1 < s2


# ---------------------------------------------------------------------------
# _actor_key
# ---------------------------------------------------------------------------

class TestActorKey:
    def test_format(self):
        assert _actor_key("tenant_a", "user_1") == "tenant_a:user_1"

    def test_different_tenant_same_user_differs(self):
        assert _actor_key("t1", "u1") != _actor_key("t2", "u1")

    def test_same_tenant_different_user_differs(self):
        assert _actor_key("t1", "u1") != _actor_key("t1", "u2")


# ---------------------------------------------------------------------------
# corroborate() — full engine
# ---------------------------------------------------------------------------

class TestCorroborate:
    def _patch(self, row, update_returns=True):
        """Return context managers patching get_claim and update_claim_corroboration."""
        return (
            patch("src.service.gaqp.corroboration.get_claim", return_value=row),
            patch(
                "src.service.gaqp.corroboration.update_claim_corroboration",
                return_value=update_returns,
            ),
        )

    def test_first_corroboration_promotes_seed_to_developing(self):
        row = _make_corpus_row()
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            result = corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_002",
            )

        assert result.was_independent is True
        assert result.promoted is True
        assert result.previous_level == "seed"
        assert result.new_level == "developing"
        assert result.new_score == CONFIDENCE_SCORE["developing"]
        assert result.independent_sources == 1
        mock_update.assert_called_once()

    def test_second_independent_corroboration_promotes_to_strong(self):
        row = _make_corpus_row(
            confidence_level="developing",
            confidence_score=CONFIDENCE_SCORE["developing"],
            corroboration_profile={
                "corroboration_count": 1,
                "independent_sources": 1,
                "same_tenant_count": 1,
                "cross_tenant_count": 0,
                "contradictions": 0,
                "last_corroborated_at": None,
                "corroborating_actors": ["tenant_001:user_002"],
            },
        )
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration"):
            result = corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_003",
            )

        assert result.was_independent is True
        assert result.promoted is True
        assert result.new_level == "strong"
        assert result.independent_sources == 2

    def test_same_actor_repetition_does_not_promote(self):
        row = _make_corpus_row()
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            # First corroboration — records the actor
            result1 = corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_002",
            )

        # Build state after first corroboration
        row2 = _make_corpus_row(
            confidence_level=result1.new_level,
            confidence_score=result1.new_score,
            corroboration_profile={
                "corroboration_count": 1,
                "independent_sources": 1,
                "same_tenant_count": 1,
                "cross_tenant_count": 0,
                "contradictions": 0,
                "last_corroborated_at": None,
                "corroborating_actors": ["tenant_001:user_002"],
            },
        )

        with patch("src.service.gaqp.corroboration.get_claim", return_value=row2), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration"):
            # Same actor again — repetition
            result2 = corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_002",
            )

        assert result2.was_independent is False
        assert result2.promoted is False
        assert result2.new_level == "developing"
        assert result2.independent_sources == 1  # unchanged

    def test_cross_tenant_corroboration_is_independent(self):
        row = _make_corpus_row()
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            result = corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_999",
                corroborating_actor_id="user_x",
            )

        assert result.was_independent is True
        assert result.promoted is True
        assert result.new_level == "developing"

        # Verify cross_tenant_count was incremented in the profile passed to update
        _, kwargs = mock_update.call_args
        profile = kwargs["new_profile"]
        assert profile.cross_tenant_count == 1
        assert profile.same_tenant_count == 0

    def test_structural_claim_not_auto_promoted(self):
        row = _make_corpus_row(
            confidence_level="structural",
            confidence_score=CONFIDENCE_SCORE["structural"],
        )
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration"):
            result = corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_002",
                corroborating_actor_id="user_y",
            )

        assert result.promoted is False
        assert result.new_level == "structural"
        assert result.new_score == CONFIDENCE_SCORE["structural"]

    def test_claim_not_found_raises(self):
        with patch("src.service.gaqp.corroboration.get_claim", return_value=None):
            with pytest.raises(ClaimNotFoundError):
                corroborate(
                    claim_id="nonexistent",
                    tenant_id="tenant_001",
                    corroborating_tenant_id="tenant_001",
                    corroborating_actor_id="user_002",
                )

    def test_update_called_with_correct_claim_and_tenant(self):
        row = _make_corpus_row(claim_id="claim_xyz", tenant_id="tenant_abc")
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            corroborate(
                claim_id="claim_xyz",
                tenant_id="tenant_abc",
                corroborating_tenant_id="tenant_abc",
                corroborating_actor_id="user_002",
            )

        _, kwargs = mock_update.call_args
        assert kwargs["claim_id"] == "claim_xyz"
        assert kwargs["tenant_id"] == "tenant_abc"

    def test_corroboration_count_increments_on_repetition(self):
        """Total corroboration_count increments even when not independent."""
        row = _make_corpus_row(
            corroboration_profile={
                "corroboration_count": 3,
                "independent_sources": 1,
                "same_tenant_count": 2,
                "cross_tenant_count": 1,
                "contradictions": 0,
                "last_corroborated_at": None,
                "corroborating_actors": ["tenant_001:user_002"],
            },
        )
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_002",  # already seen
            )

        _, kwargs = mock_update.call_args
        assert kwargs["new_profile"].corroboration_count == 4

    def test_actor_key_appended_on_independent_source(self):
        row = _make_corpus_row()
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_007",
            )

        _, kwargs = mock_update.call_args
        profile = kwargs["new_profile"]
        assert "tenant_001:user_007" in profile.corroborating_actors

    def test_actor_key_not_duplicated_on_repetition(self):
        row = _make_corpus_row(
            corroboration_profile={
                "corroboration_count": 1,
                "independent_sources": 1,
                "same_tenant_count": 1,
                "cross_tenant_count": 0,
                "contradictions": 0,
                "last_corroborated_at": None,
                "corroborating_actors": ["tenant_001:user_002"],
            },
        )
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_002",
            )

        _, kwargs = mock_update.call_args
        profile = kwargs["new_profile"]
        assert profile.corroborating_actors.count("tenant_001:user_002") == 1

    def test_last_corroborated_at_updated(self):
        row = _make_corpus_row()
        with patch("src.service.gaqp.corroboration.get_claim", return_value=row), \
             patch("src.service.gaqp.corroboration.update_claim_corroboration") as mock_update:
            corroborate(
                claim_id="claim_abc",
                tenant_id="tenant_001",
                corroborating_tenant_id="tenant_001",
                corroborating_actor_id="user_002",
            )

        _, kwargs = mock_update.call_args
        profile = kwargs["new_profile"]
        assert profile.last_corroborated_at is not None
        assert isinstance(profile.last_corroborated_at, __import__("datetime").datetime)

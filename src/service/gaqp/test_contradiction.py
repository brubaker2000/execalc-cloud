from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict
from unittest.mock import patch

import pytest

from src.service.gaqp.contradiction import (
    ContradictionResult,
    _profile_from_row,
    _with_contradictions_delta,
    contradict,
    resolve_contradiction,
)
from src.service.gaqp.exceptions import ClaimNotFoundError, SelfContradictionError
from src.service.gaqp.models import CorroborationProfile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row(
    claim_id: str = "claim_a",
    tenant_id: str = "tenant_001",
    contradiction_refs: list | None = None,
    contradictions: int = 0,
) -> Dict[str, Any]:
    return {
        "claim_id": claim_id,
        "tenant_id": tenant_id,
        "source_envelope_id": "env_001",
        "claim_type": "tradeoff",
        "domain": "strategy",
        "content": "Speed and certainty cannot both be maximized simultaneously.",
        "confidence_level": "seed",
        "confidence_score": 0.50,
        "admission_status": "admitted",
        "corpus_scope": "tenant",
        "extraction_method": "direct_field",
        "provenance": {
            "source_kind": "decision_artifact",
            "source_ref": "env_001",
            "actor_id": "user_001",
        },
        "activation_scope": "situational",
        "activation_triggers": ["tradeoff_analysis"],
        "corroboration_profile": {
            "corroboration_count": 0,
            "independent_sources": 0,
            "same_tenant_count": 0,
            "cross_tenant_count": 0,
            "contradictions": contradictions,
            "last_corroborated_at": None,
            "corroborating_actors": [],
        },
        "contradiction_refs": contradiction_refs if contradiction_refs is not None else [],
        "support_refs": [],
        "fingerprint": f"fp_{claim_id}",
        "schema_version": "stage9_v1",
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat(),
    }


# ---------------------------------------------------------------------------
# _profile_from_row
# ---------------------------------------------------------------------------

class TestProfileFromRow:
    def test_reconstructs_contradictions_count(self):
        row = _row(contradictions=3)
        profile = _profile_from_row(row)
        assert profile.contradictions == 3

    def test_defaults_when_profile_missing(self):
        row = _row()
        row["corroboration_profile"] = None
        profile = _profile_from_row(row)
        assert profile.contradictions == 0
        assert profile.corroboration_count == 0


# ---------------------------------------------------------------------------
# _with_contradictions_delta
# ---------------------------------------------------------------------------

class TestWithContradictionsDelta:
    def test_increment(self):
        profile = CorroborationProfile(contradictions=2)
        updated = _with_contradictions_delta(profile, +1)
        assert updated.contradictions == 3

    def test_decrement(self):
        profile = CorroborationProfile(contradictions=2)
        updated = _with_contradictions_delta(profile, -1)
        assert updated.contradictions == 1

    def test_clamps_to_zero(self):
        profile = CorroborationProfile(contradictions=0)
        updated = _with_contradictions_delta(profile, -1)
        assert updated.contradictions == 0

    def test_other_fields_preserved(self):
        profile = CorroborationProfile(
            corroboration_count=5,
            independent_sources=2,
            contradictions=1,
        )
        updated = _with_contradictions_delta(profile, +1)
        assert updated.corroboration_count == 5
        assert updated.independent_sources == 2


# ---------------------------------------------------------------------------
# contradict()
# ---------------------------------------------------------------------------

class TestContradict:
    def test_creates_bidirectional_link(self):
        row_a = _row(claim_id="claim_a")
        row_b = _row(claim_id="claim_b")

        def fake_get_claim(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get_claim), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions") as mock_update:
            result = contradict(
                claim_id="claim_a",
                contradicting_claim_id="claim_b",
                tenant_id="tenant_001",
            )

        assert result.was_new_link is True
        assert mock_update.call_count == 2

        # First update call is for claim_a
        _, kwargs_a = mock_update.call_args_list[0]
        assert kwargs_a["claim_id"] == "claim_a"
        assert "claim_b" in kwargs_a["new_contradiction_refs"]

        # Second update call is for claim_b
        _, kwargs_b = mock_update.call_args_list[1]
        assert kwargs_b["claim_id"] == "claim_b"
        assert "claim_a" in kwargs_b["new_contradiction_refs"]

    def test_increments_contradictions_on_both_profiles(self):
        row_a = _row(claim_id="claim_a", contradictions=0)
        row_b = _row(claim_id="claim_b", contradictions=1)

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions") as mock_update:
            contradict(claim_id="claim_a", contradicting_claim_id="claim_b", tenant_id="tenant_001")

        _, kwargs_a = mock_update.call_args_list[0]
        _, kwargs_b = mock_update.call_args_list[1]
        assert kwargs_a["new_corroboration_profile"].contradictions == 1
        assert kwargs_b["new_corroboration_profile"].contradictions == 2

    def test_idempotent_when_already_linked(self):
        row_a = _row(claim_id="claim_a", contradiction_refs=["claim_b"])
        row_b = _row(claim_id="claim_b")

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions") as mock_update:
            result = contradict(claim_id="claim_a", contradicting_claim_id="claim_b", tenant_id="tenant_001")

        assert result.was_new_link is False
        mock_update.assert_not_called()

    def test_self_contradiction_raises(self):
        with pytest.raises(SelfContradictionError):
            contradict(claim_id="claim_a", contradicting_claim_id="claim_a", tenant_id="tenant_001")

    def test_missing_claim_a_raises(self):
        with patch("src.service.gaqp.contradiction.get_claim", return_value=None):
            with pytest.raises(ClaimNotFoundError):
                contradict(claim_id="missing", contradicting_claim_id="claim_b", tenant_id="t1")

    def test_missing_claim_b_raises(self):
        row_a = _row(claim_id="claim_a")

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else None

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get):
            with pytest.raises(ClaimNotFoundError):
                contradict(claim_id="claim_a", contradicting_claim_id="missing", tenant_id="t1")

    def test_returns_correct_claim_ids(self):
        row_a = _row(claim_id="aaa")
        row_b = _row(claim_id="bbb")

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "aaa" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions"):
            result = contradict(claim_id="aaa", contradicting_claim_id="bbb", tenant_id="t1")

        assert result.claim_id == "aaa"
        assert result.contradicting_claim_id == "bbb"


# ---------------------------------------------------------------------------
# resolve_contradiction()
# ---------------------------------------------------------------------------

class TestResolveContradiction:
    def test_removes_bidirectional_link(self):
        row_a = _row(claim_id="claim_a", contradiction_refs=["claim_b"], contradictions=1)
        row_b = _row(claim_id="claim_b", contradiction_refs=["claim_a"], contradictions=1)

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions") as mock_update:
            result = resolve_contradiction(
                claim_id="claim_a",
                contradicting_claim_id="claim_b",
                tenant_id="tenant_001",
            )

        assert result.was_new_link is True
        assert mock_update.call_count == 2

        _, kwargs_a = mock_update.call_args_list[0]
        assert "claim_b" not in kwargs_a["new_contradiction_refs"]

        _, kwargs_b = mock_update.call_args_list[1]
        assert "claim_a" not in kwargs_b["new_contradiction_refs"]

    def test_decrements_contradictions_on_both(self):
        row_a = _row(claim_id="claim_a", contradiction_refs=["claim_b"], contradictions=2)
        row_b = _row(claim_id="claim_b", contradiction_refs=["claim_a"], contradictions=3)

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions") as mock_update:
            resolve_contradiction(claim_id="claim_a", contradicting_claim_id="claim_b", tenant_id="t1")

        _, kwargs_a = mock_update.call_args_list[0]
        _, kwargs_b = mock_update.call_args_list[1]
        assert kwargs_a["new_corroboration_profile"].contradictions == 1
        assert kwargs_b["new_corroboration_profile"].contradictions == 2

    def test_idempotent_when_link_absent(self):
        row_a = _row(claim_id="claim_a", contradiction_refs=[])
        row_b = _row(claim_id="claim_b")

        def fake_get(*, claim_id, tenant_id):
            return row_a if claim_id == "claim_a" else row_b

        with patch("src.service.gaqp.contradiction.get_claim", side_effect=fake_get), \
             patch("src.service.gaqp.contradiction.update_claim_contradictions") as mock_update:
            result = resolve_contradiction(claim_id="claim_a", contradicting_claim_id="claim_b", tenant_id="t1")

        assert result.was_new_link is False
        mock_update.assert_not_called()

    def test_missing_claim_raises(self):
        with patch("src.service.gaqp.contradiction.get_claim", return_value=None):
            with pytest.raises(ClaimNotFoundError):
                resolve_contradiction(claim_id="missing", contradicting_claim_id="b", tenant_id="t1")


# ---------------------------------------------------------------------------
# Activation surfacing (integration with activation engine)
# ---------------------------------------------------------------------------

class TestActivationSurfacesContradictions:
    """Verify the activation engine surfaces contradiction alerts in the bundle."""

    def _activated_row(self, claim_id: str, contradiction_refs: list) -> Dict[str, Any]:
        return {
            "claim_id": claim_id,
            "tenant_id": "t-001",
            "source_envelope_id": "env-001",
            "claim_type": "tradeoff",
            "domain": "strategy",
            "content": "Speed over certainty in high-stakes decisions carries tail risk.",
            "confidence_level": "developing",
            "confidence_score": 0.72,
            "admission_status": "admitted",
            "corpus_scope": "tenant",
            "extraction_method": "direct_field",
            "provenance": {"source_kind": "decision_artifact", "source_ref": "env-001", "actor_id": "u1"},
            "activation_scope": "universal",
            "activation_triggers": [],
            "corroboration_profile": {
                "corroboration_count": 1, "independent_sources": 1,
                "same_tenant_count": 1, "cross_tenant_count": 0,
                "contradictions": len(contradiction_refs),
                "last_corroborated_at": None, "corroborating_actors": [],
            },
            "contradiction_refs": contradiction_refs,
            "support_refs": [],
            "fingerprint": f"fp_{claim_id}",
            "schema_version": "stage9_v1",
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }

    def test_no_contradictions_empty_alerts(self):
        from src.service.gaqp.activation import activate
        from src.service.orchestration.models import ScenarioEnvelope

        row = self._activated_row("claim_a", contradiction_refs=[])
        scenario = ScenarioEnvelope(
            scenario_id="sc-1", scenario_type="acquisition",
            governing_objective="evaluate", user_intent="decision_seeking",
            prompt="acquire?",
        )

        with patch("src.service.gaqp.activation.list_claims", return_value=[row]):
            bundle = activate(scenario=scenario, tenant_id="t-001")

        assert bundle.contradiction_alerts == []

    def test_activated_claim_with_contradiction_ref_surfaces_alert(self):
        from src.service.gaqp.activation import activate
        from src.service.orchestration.models import ScenarioEnvelope

        contra_row = self._activated_row("claim_b", contradiction_refs=[])
        active_row = self._activated_row("claim_a", contradiction_refs=["claim_b"])
        scenario = ScenarioEnvelope(
            scenario_id="sc-1", scenario_type="acquisition",
            governing_objective="evaluate", user_intent="decision_seeking",
            prompt="acquire?",
        )

        with patch("src.service.gaqp.activation.list_claims", return_value=[active_row]), \
             patch("src.service.gaqp.activation.get_claim", return_value=contra_row):
            bundle = activate(scenario=scenario, tenant_id="t-001")

        assert len(bundle.contradiction_alerts) == 1
        alert = bundle.contradiction_alerts[0]
        assert alert.activated_claim_id == "claim_a"
        assert alert.contradicting_claim.claim_id == "claim_b"

    def test_missing_contradiction_ref_skipped_gracefully(self):
        from src.service.gaqp.activation import activate
        from src.service.orchestration.models import ScenarioEnvelope

        active_row = self._activated_row("claim_a", contradiction_refs=["ghost_claim"])
        scenario = ScenarioEnvelope(
            scenario_id="sc-1", scenario_type="acquisition",
            governing_objective="evaluate", user_intent="decision_seeking",
            prompt="acquire?",
        )

        with patch("src.service.gaqp.activation.list_claims", return_value=[active_row]), \
             patch("src.service.gaqp.activation.get_claim", return_value=None):
            bundle = activate(scenario=scenario, tenant_id="t-001")

        # Ghost ref produces no alert — no crash
        assert bundle.contradiction_alerts == []
        assert len(bundle.activated_claims) == 1

    def test_bundle_to_dict_includes_contradiction_alerts(self):
        from src.service.gaqp.models import ActivationBundle, ContradictionAlert, GAQPClaim
        from src.service.gaqp.models import ClaimProvenance, CorroborationProfile
        from src.service.gaqp.models import compute_fingerprint
        import uuid

        contra_claim = GAQPClaim(
            claim_id=uuid.uuid4().hex,
            tenant_id="t1",
            source_envelope_id="env1",
            claim_type="tradeoff",
            domain="strategy",
            content="Certainty over speed preserves optionality under ambiguity.",
            confidence_level="seed",
            confidence_score=0.50,
            admission_status="admitted",
            corpus_scope="tenant",
            extraction_method="direct_field",
            provenance=ClaimProvenance(
                source_kind="decision_artifact", source_ref="env1",
                actor_id="u1",
            ),
            activation_scope="situational",
            fingerprint=compute_fingerprint(
                tenant_id="t1", source_envelope_id="env1",
                claim_type="tradeoff",
                content="Certainty over speed preserves optionality under ambiguity.",
                activation_scope="situational",
            ),
        )
        alert = ContradictionAlert(
            activated_claim_id="claim_a",
            contradicting_claim=contra_claim,
        )
        bundle = ActivationBundle(
            activated_claims=[],
            activation_rationale=[],
            corpus_scope="tenant",
            confidence_floor=0.50,
            contradiction_alerts=[alert],
        )
        d = bundle.to_dict()
        assert "contradiction_alerts" in d
        assert len(d["contradiction_alerts"]) == 1
        assert d["contradiction_alerts"][0]["activated_claim_id"] == "claim_a"

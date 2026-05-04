from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from src.service.gaqp.activation import (
    _build_search_text,
    _dict_to_claim,
    _match_rationale,
    activate,
)
from src.service.orchestration.models import ScenarioEnvelope


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _scenario(
    scenario_type: str = "acquisition",
    governing_objective: str = "evaluate target",
    prompt: str = "Should we acquire this company?",
) -> ScenarioEnvelope:
    return ScenarioEnvelope(
        scenario_id="sc-001",
        scenario_type=scenario_type,
        governing_objective=governing_objective,
        user_intent="decision_seeking",
        prompt=prompt,
    )


def _row(
    claim_id: str = "cid-001",
    claim_type: str = "tradeoff",
    confidence_score: float = 0.72,
    activation_scope: str = "domain_specific",
    activation_triggers: List[str] = None,
    corpus_scope: str = "tenant",
    tenant_id: str = "t-001",
) -> Dict[str, Any]:
    return {
        "claim_id": claim_id,
        "tenant_id": tenant_id,
        "source_envelope_id": "env-001",
        "claim_type": claim_type,
        "domain": "strategy",
        "content": "Acquiring a distressed asset compresses timeline but expands risk.",
        "confidence_level": "developing",
        "confidence_score": confidence_score,
        "admission_status": "admitted",
        "corpus_scope": corpus_scope,
        "extraction_method": "direct_field",
        "provenance": {
            "source_kind": "decision_artifact",
            "source_ref": "env-001",
            "actor_id": "user-1",
        },
        "activation_scope": activation_scope,
        "activation_triggers": activation_triggers or ["acquisition", "acquire"],
        "corroboration_profile": {
            "corroboration_count": 1,
            "independent_sources": 1,
            "same_tenant_count": 0,
            "cross_tenant_count": 0,
            "contradictions": 0,
            "last_corroborated_at": None,
        },
        "contradiction_refs": [],
        "support_refs": [],
        "fingerprint": "abc123",
        "schema_version": "stage9_v1",
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat(),
    }


# ---------------------------------------------------------------------------
# _build_search_text
# ---------------------------------------------------------------------------

def test_build_search_text_combines_fields():
    sc = _scenario(
        scenario_type="acquisition",
        governing_objective="evaluate target",
        prompt="Should we acquire?",
    )
    text = _build_search_text(sc)
    assert "acquisition" in text
    assert "evaluate target" in text
    assert "should we acquire?" in text
    assert text == text.lower()


def test_build_search_text_skips_empty_fields():
    sc = _scenario(scenario_type="general", governing_objective="", prompt="")
    text = _build_search_text(sc)
    assert text == "general"


# ---------------------------------------------------------------------------
# _match_rationale
# ---------------------------------------------------------------------------

def test_match_rationale_universal_always_fires():
    row = _row(activation_scope="universal", activation_triggers=[])
    assert _match_rationale(row, "anything at all") is not None


def test_match_rationale_trigger_match_fires():
    row = _row(activation_scope="domain_specific", activation_triggers=["acquisition"])
    rationale = _match_rationale(row, "considering an acquisition target")
    assert rationale is not None
    assert "acquisition" in rationale


def test_match_rationale_no_match_returns_none():
    row = _row(activation_scope="domain_specific", activation_triggers=["salary cap"])
    assert _match_rationale(row, "quarterly revenue review") is None


def test_match_rationale_case_insensitive():
    row = _row(activation_scope="situational", activation_triggers=["Acquisition"])
    assert _match_rationale(row, "acquisition target") is not None


def test_match_rationale_empty_triggers_no_match():
    row = _row(activation_scope="tenant_specific", activation_triggers=[])
    assert _match_rationale(row, "anything") is None


# ---------------------------------------------------------------------------
# _dict_to_claim
# ---------------------------------------------------------------------------

def test_dict_to_claim_roundtrip():
    row = _row()
    claim = _dict_to_claim(row)
    assert claim.claim_id == "cid-001"
    assert claim.claim_type == "tradeoff"
    assert claim.confidence_score == 0.72
    assert claim.activation_triggers == ["acquisition", "acquire"]
    assert claim.contradiction_refs == []
    assert isinstance(claim.created_at, datetime)


def test_dict_to_claim_missing_provenance_fields():
    row = _row()
    row["provenance"] = {}
    claim = _dict_to_claim(row)
    assert claim.provenance.source_kind == "unknown"
    assert claim.provenance.source_ref == ""


def test_dict_to_claim_null_timestamps_use_defaults():
    row = _row()
    row["created_at"] = None
    row["updated_at"] = None
    claim = _dict_to_claim(row)
    assert isinstance(claim.created_at, datetime)
    assert isinstance(claim.updated_at, datetime)


# ---------------------------------------------------------------------------
# activate — integration via mocked list_claims
# ---------------------------------------------------------------------------

def test_activate_empty_corpus_returns_empty_bundle():
    with patch("src.service.gaqp.activation.list_claims", return_value=[]):
        bundle = activate(scenario=_scenario(), tenant_id="t-001")
    assert bundle.is_empty
    assert bundle.activation_rationale == []


def test_activate_universal_claim_always_fires():
    row = _row(activation_scope="universal", activation_triggers=[])
    with patch("src.service.gaqp.activation.list_claims", return_value=[row]):
        bundle = activate(scenario=_scenario(prompt="completely unrelated topic"), tenant_id="t-001")
    assert len(bundle.activated_claims) == 1
    assert "Universal" in bundle.activation_rationale[0]


def test_activate_trigger_match_fires():
    row = _row(activation_scope="domain_specific", activation_triggers=["acquire"])
    with patch("src.service.gaqp.activation.list_claims", return_value=[row]):
        bundle = activate(scenario=_scenario(prompt="Should we acquire this company?"), tenant_id="t-001")
    assert len(bundle.activated_claims) == 1


def test_activate_no_trigger_match_excluded():
    row = _row(activation_scope="situational", activation_triggers=["salary cap"])
    with patch("src.service.gaqp.activation.list_claims", return_value=[row]):
        bundle = activate(scenario=_scenario(prompt="revenue forecast review"), tenant_id="t-001")
    assert bundle.is_empty


def test_activate_sorted_by_confidence_desc():
    rows = [
        _row(claim_id="low", confidence_score=0.50, activation_scope="universal"),
        _row(claim_id="high", confidence_score=0.91, activation_scope="universal"),
        _row(claim_id="mid", confidence_score=0.72, activation_scope="universal"),
    ]
    with patch("src.service.gaqp.activation.list_claims", return_value=rows):
        bundle = activate(scenario=_scenario(), tenant_id="t-001")
    scores = [c.confidence_score for c in bundle.activated_claims]
    assert scores == sorted(scores, reverse=True)


def test_activate_max_claims_cap():
    rows = [_row(claim_id=f"cid-{i}", activation_scope="universal") for i in range(30)]
    with patch("src.service.gaqp.activation.list_claims", return_value=rows):
        bundle = activate(scenario=_scenario(), tenant_id="t-001", max_claims=5)
    assert len(bundle.activated_claims) == 5
    assert len(bundle.activation_rationale) == 5


def test_activate_deduplicates_across_scopes():
    row = _row(claim_id="cid-dup", activation_scope="universal")
    # list_claims is called 3 times (private, tenant, structural); each returns the same row
    with patch("src.service.gaqp.activation.list_claims", return_value=[row]):
        bundle = activate(scenario=_scenario(), tenant_id="t-001")
    assert len(bundle.activated_claims) == 1


def test_activate_corpus_error_returns_empty_bundle():
    with patch("src.service.gaqp.activation.list_claims", side_effect=RuntimeError("db down")):
        bundle = activate(scenario=_scenario(), tenant_id="t-001")
    assert bundle.is_empty
    assert bundle.confidence_floor == 0.50


def test_activate_bundle_metadata():
    with patch("src.service.gaqp.activation.list_claims", return_value=[]):
        bundle = activate(scenario=_scenario(), tenant_id="t-001", confidence_floor=0.72)
    assert bundle.corpus_scope == "structural"
    assert bundle.confidence_floor == 0.72

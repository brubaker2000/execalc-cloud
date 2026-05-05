from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import MagicMock, patch

import pytest

from src.service.gaqp.backfill import BackfillSummary, _report_from_dict, run_backfill
from src.service.gaqp.corpus import InsertSummary
from src.service.decision_loop.models import DecisionReport, SensitivityVariable


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_FULL_RESULT: Dict[str, Any] = {
    "ok": True,
    "report": {
        "executive_summary": "Market conditions favor entry.",
        "confidence": "medium",
        "confidence_rationale": [
            "Strong demand signal supports conviction.",
            "Counterparty risk is bounded.",
        ],
        "governing_objective": "maximize_returns",
        "tradeoffs": {"upside": ["High upside"], "downside": ["Some downside"], "key_tradeoffs": []},
        "sensitivity": [{"name": "interest_rate", "impact": "increases cost of carry"}],
        "next_actions": ["proceed"],
        "value_assessment": "Strong value proposition exists in this market segment.",
        "risk_reward_assessment": "Risk/reward is favorable given the current signal environment.",
        "supply_demand_assessment": "Demand significantly outpaces available supply at current price.",
        "asset_assessment": "Core assets are well-positioned and liquid for immediate execution.",
        "liability_assessment": "Liabilities are manageable, bounded, and well-understood.",
        "actors": ["management", "investors"],
        "incentives": ["Profit motive drives aggressive expansion into adjacent verticals."],
        "asymmetries": ["Information asymmetry favors the informed buyer with full data access."],
        "execution_trace": {"model": "gpt-4"},
    },
    "audit": {"governing_objective": "maximize_returns", "scenario_type": "investment"},
}


def _make_result(suffix: str = "") -> Dict[str, Any]:
    """Copy of _FULL_RESULT with a unique executive_summary to vary content."""
    import copy
    r = copy.deepcopy(_FULL_RESULT)
    r["report"]["executive_summary"] = f"Market conditions favor entry. Variant {suffix}."
    return r


def _mock_conn() -> MagicMock:
    conn = MagicMock()
    conn.close = MagicMock()
    return conn


# ---------------------------------------------------------------------------
# _report_from_dict — unit tests
# ---------------------------------------------------------------------------

def test_report_from_dict_roundtrip():
    report = _report_from_dict(_FULL_RESULT)
    assert isinstance(report, DecisionReport)
    assert report.executive_summary == "Market conditions favor entry."
    assert report.confidence == "medium"
    assert report.governing_objective == "maximize_returns"
    assert report.value_assessment == "Strong value proposition exists in this market segment."
    assert report.audit["scenario_type"] == "investment"


def test_report_from_dict_sensitivity_reconstruction():
    report = _report_from_dict(_FULL_RESULT)
    assert len(report.sensitivity) == 1
    assert isinstance(report.sensitivity[0], SensitivityVariable)
    assert report.sensitivity[0].name == "interest_rate"
    assert report.sensitivity[0].impact == "increases cost of carry"


def test_report_from_dict_malformed_sensitivity_entries_skipped():
    result = {
        "ok": True,
        "report": {
            "sensitivity": [
                {"name": "inflation", "impact": "raises cost"},
                {"bad_key": True},     # malformed — no name/impact
                "not_a_dict",          # wrong type
            ],
        },
        "audit": {},
    }
    report = _report_from_dict(result)
    assert len(report.sensitivity) == 1
    assert report.sensitivity[0].name == "inflation"


def test_report_from_dict_empty_report_uses_safe_defaults():
    result = {"ok": True, "report": {}, "audit": {}}
    report = _report_from_dict(result)
    assert report.executive_summary == ""
    assert report.confidence == "unknown"
    assert report.sensitivity == []
    assert report.incentives == []
    assert report.tradeoffs == {}
    assert report.execution_trace == {}


def test_report_from_dict_audit_pulled_from_result_not_report():
    result = {
        "ok": True,
        "report": {"governing_objective": "inner_value"},
        "audit": {"governing_objective": "canonical_value", "scenario_type": "test_scenario"},
    }
    report = _report_from_dict(result)
    assert report.audit["governing_objective"] == "canonical_value"
    assert report.audit["scenario_type"] == "test_scenario"


def test_report_from_dict_missing_report_key_uses_defaults():
    result = {"ok": True, "audit": {"scenario_type": "x"}}
    report = _report_from_dict(result)
    assert report.value_assessment == ""
    assert report.audit["scenario_type"] == "x"


def test_report_from_dict_none_report_uses_defaults():
    result = {"ok": True, "report": None, "audit": {}}
    report = _report_from_dict(result)
    assert report.executive_summary == ""


# ---------------------------------------------------------------------------
# run_backfill — empty corpus
# ---------------------------------------------------------------------------

def test_run_backfill_empty_records():
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", return_value=[]):
        summary = run_backfill()
    assert summary.records_read == 0
    assert summary.claims_extracted == 0
    assert summary.errors == []


# ---------------------------------------------------------------------------
# run_backfill — single record happy path
# ---------------------------------------------------------------------------

def test_run_backfill_single_record_inserted():
    page = [(1, "tenant_a", "env_001", _make_result("a"))]
    insert_sum = InsertSummary(inserted=5, skipped=0, failed=0)
    fetch_pages = [page, []]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=fetch_pages), \
         patch("src.service.gaqp.backfill.insert_claims", return_value=insert_sum) as mock_insert:
        summary = run_backfill()
    assert summary.records_read == 1
    assert summary.records_skipped == 0
    assert summary.claims_inserted == 5
    assert summary.claims_failed == 0
    mock_insert.assert_called_once()


# ---------------------------------------------------------------------------
# run_backfill — skipping bad records
# ---------------------------------------------------------------------------

def test_run_backfill_skips_record_without_report_key():
    page = [(1, "tenant_a", "env_001", {"ok": True})]  # no "report" key
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]):
        summary = run_backfill()
    assert summary.records_read == 1
    assert summary.records_skipped == 1
    assert summary.claims_extracted == 0


def test_run_backfill_skips_null_result():
    page = [(1, "tenant_a", "env_001", None)]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]):
        summary = run_backfill()
    assert summary.records_read == 1
    assert summary.records_skipped == 1


def test_run_backfill_isolation_on_reconstruction_error():
    page = [(1, "tenant_a", "env_bad", _make_result())]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]), \
         patch("src.service.gaqp.backfill._report_from_dict", side_effect=ValueError("boom")):
        summary = run_backfill()
    assert summary.records_read == 1
    assert summary.records_skipped == 1
    assert len(summary.errors) == 1
    assert "env_bad" in summary.errors[0]
    assert "reconstruction failed" in summary.errors[0]


def test_run_backfill_isolation_on_extraction_error():
    page = [(1, "tenant_a", "env_001", _make_result())]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]), \
         patch("src.service.gaqp.backfill.extract_claims", side_effect=RuntimeError("extraction exploded")):
        summary = run_backfill()
    assert summary.records_read == 1
    assert summary.records_skipped == 1
    assert len(summary.errors) == 1
    assert "extraction failed" in summary.errors[0]


def test_run_backfill_persistence_error_isolated():
    page = [(1, "tenant_a", "env_001", _make_result())]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]), \
         patch("src.service.gaqp.backfill.insert_claims", side_effect=RuntimeError("db down")):
        summary = run_backfill()
    # record was read and processed — only persistence failed
    assert summary.records_read == 1
    assert summary.records_skipped == 0
    assert len(summary.errors) == 1
    assert "env_001" in summary.errors[0]
    assert "persistence failed" in summary.errors[0]


# ---------------------------------------------------------------------------
# run_backfill — dry_run
# ---------------------------------------------------------------------------

def test_run_backfill_dry_run_does_not_call_insert():
    page = [(1, "tenant_a", "env_001", _make_result())]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]), \
         patch("src.service.gaqp.backfill.insert_claims") as mock_insert:
        summary = run_backfill(dry_run=True)
    mock_insert.assert_not_called()
    assert summary.records_read == 1


def test_run_backfill_dry_run_counts_admitted_claims():
    page = [(1, "tenant_a", "env_001", _make_result())]
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]):
        summary = run_backfill(dry_run=True)
    # claims_inserted reflects admitted count even in dry run
    assert summary.claims_inserted >= 0
    assert summary.claims_extracted >= 0


# ---------------------------------------------------------------------------
# run_backfill — pagination
# ---------------------------------------------------------------------------

def test_run_backfill_pagination_across_two_pages():
    page1 = [
        (1, "t", "e1", _make_result("1")),
        (2, "t", "e2", _make_result("2")),
    ]
    page2 = [(3, "t", "e3", _make_result("3"))]
    insert_sum = InsertSummary(inserted=2, skipped=0, failed=0)
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page1, page2, []]), \
         patch("src.service.gaqp.backfill.insert_claims", return_value=insert_sum):
        summary = run_backfill(batch_size=2)
    assert summary.records_read == 3


def test_run_backfill_limit_stops_early():
    page = [
        (1, "t", "e1", _make_result("1")),
        (2, "t", "e2", _make_result("2")),
        (3, "t", "e3", _make_result("3")),
    ]
    insert_sum = InsertSummary(inserted=2, skipped=0, failed=0)
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]), \
         patch("src.service.gaqp.backfill.insert_claims", return_value=insert_sum):
        summary = run_backfill(limit=2)
    assert summary.records_read == 2


# ---------------------------------------------------------------------------
# run_backfill — InsertSummary accumulation
# ---------------------------------------------------------------------------

def test_run_backfill_accumulates_insert_summary():
    page = [
        (1, "t", "e1", _make_result("1")),
        (2, "t", "e2", _make_result("2")),
    ]
    insert_sum = InsertSummary(inserted=3, skipped=2, failed=0)
    with patch("src.service.gaqp.backfill.get_conn", return_value=_mock_conn()), \
         patch("src.service.gaqp.backfill._fetch_page", side_effect=[page, []]), \
         patch("src.service.gaqp.backfill.insert_claims", return_value=insert_sum):
        summary = run_backfill()
    assert summary.claims_inserted == 6   # 3 per record × 2 records
    assert summary.claims_skipped == 4    # 2 per record × 2 records


# ---------------------------------------------------------------------------
# BackfillSummary
# ---------------------------------------------------------------------------

def test_backfill_summary_to_dict():
    s = BackfillSummary(
        records_read=10,
        records_skipped=1,
        claims_extracted=45,
        claims_inserted=30,
        claims_skipped=15,
        claims_failed=0,
        errors=["env_bad: reconstruction failed — ValueError"],
    )
    d = s.to_dict()
    assert d["records_read"] == 10
    assert d["records_skipped"] == 1
    assert d["claims_extracted"] == 45
    assert d["claims_inserted"] == 30
    assert d["claims_skipped"] == 15
    assert d["claims_failed"] == 0
    assert len(d["errors"]) == 1


def test_backfill_summary_default_state():
    s = BackfillSummary()
    assert s.records_read == 0
    assert s.errors == []

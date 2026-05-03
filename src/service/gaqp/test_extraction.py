from __future__ import annotations

from src.service.decision_loop.engine import run_decision_loop
from src.service.decision_loop.models import DecisionReport, Scenario
from src.service.gaqp.extraction import (
    _run_admission_tests,
    admitted_claims,
    extract_claims,
    needs_review_claims,
)
from src.service.gaqp.models import CONFIDENCE_SCORE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _minimal_report() -> DecisionReport:
    scenario = Scenario(
        scenario_type="feasibility",
        governing_objective="reduce_cap",
        prompt="Should we trade the veteran for cap flexibility?",
        facts={"objective": "reduce_cap", "resources": "limited", "timeline": "Q3"},
        constraints={"cap_floor": "140M"},
    )
    return run_decision_loop(
        tenant_id="tenant_001",
        user_id="user_001",
        scenario=scenario,
    )


def _rich_report() -> DecisionReport:
    scenario = Scenario(
        scenario_type="draft_trade",
        governing_objective="maximize_upside",
        prompt="Evaluate this draft-day trade.",
        facts={"you_pick": "pick_5", "counterparty_pick": "pick_12", "counterparty": "Team B"},
        constraints={"salary_cap": "150M"},
        risk_surface="roster_volatility",
        decision_horizon="48_hours",
        stakeholder_scope="ownership, coaching staff",
        assumptions="Both picks project top-10 talent",
    )
    return run_decision_loop(
        tenant_id="tenant_001",
        user_id="user_001",
        scenario=scenario,
    )


# ---------------------------------------------------------------------------
# Admission tests
# ---------------------------------------------------------------------------

class TestAdmissionTests:
    def test_empty_content_rejected(self):
        result = _run_admission_tests("")
        assert result.admission_status == "rejected"
        assert "stand_alone" in result.failed_tests

    def test_too_short_rejected(self):
        result = _run_admission_tests("Short.")
        assert result.admission_status == "rejected"

    def test_boilerplate_rejected(self):
        result = _run_admission_tests("N/A — no constraints identified.")
        assert result.admission_status == "rejected"

    def test_question_rejected(self):
        result = _run_admission_tests(
            "Should we consider this option before the deadline?"
        )
        assert result.admission_status == "rejected"
        assert "disputability" in result.failed_tests

    def test_ephemeral_needs_review(self):
        result = _run_admission_tests(
            "Right now the market favors sellers with flexible terms and patience."
        )
        assert result.admission_status == "needs_review"
        assert "durability" in result.failed_tests

    def test_short_but_not_trivial_needs_review(self):
        result = _run_admission_tests("Speed trades off against certainty.")
        assert result.admission_status == "needs_review"
        assert "non_triviality" in result.failed_tests

    def test_substantive_claim_admitted(self):
        result = _run_admission_tests(
            "Under a payroll reduction mandate, prioritize cost-controlled flexibility "
            "and avoid moves that increase fixed commitments without surplus value."
        )
        assert result.admission_status == "admitted"
        assert result.admitted

    def test_admitted_has_no_failed_tests(self):
        result = _run_admission_tests(
            "A party with more balance-sheet flexibility typically commands better "
            "terms when the counterparty is operating under a hard cap constraint."
        )
        assert result.admitted
        assert result.failed_tests == []


# ---------------------------------------------------------------------------
# extract_claims — structure and volume
# ---------------------------------------------------------------------------

class TestExtractClaims:
    def test_returns_list(self):
        report = _minimal_report()
        claims = extract_claims(
            report=report,
            tenant_id="tenant_001",
            source_envelope_id="env_001",
            actor_id="user_001",
        )
        assert isinstance(claims, list)

    def test_produces_claims(self):
        report = _minimal_report()
        claims = extract_claims(
            report=report,
            tenant_id="tenant_001",
            source_envelope_id="env_001",
            actor_id="user_001",
        )
        assert len(claims) > 0

    def test_rich_report_produces_more_claims(self):
        minimal = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        rich = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e2", actor_id="u1",
        )
        assert len(rich) >= len(minimal)

    def test_all_claims_have_tenant_id(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="tenant_abc",
            source_envelope_id="env_001",
            actor_id="user_001",
        )
        assert all(c.tenant_id == "tenant_abc" for c in claims)

    def test_all_claims_have_source_envelope(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1",
            source_envelope_id="envelope_xyz",
            actor_id="u1",
        )
        assert all(c.source_envelope_id == "envelope_xyz" for c in claims)

    def test_all_claims_have_fingerprint(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        assert all(c.fingerprint for c in claims)

    def test_fingerprints_unique_within_extraction(self):
        claims = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        fps = [c.fingerprint for c in claims]
        assert len(fps) == len(set(fps)), "Duplicate fingerprints within one extraction"

    def test_all_claims_seed_confidence(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        assert all(c.confidence_level == "seed" for c in claims)
        assert all(c.confidence_score == CONFIDENCE_SCORE["seed"] for c in claims)

    def test_all_claims_tenant_corpus_scope(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        assert all(c.corpus_scope == "tenant" for c in claims)

    def test_all_claims_direct_field_extraction(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        assert all(c.extraction_method == "direct_field" for c in claims)

    def test_all_claims_have_activation_triggers(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        assert all(len(c.activation_triggers) > 0 for c in claims)

    def test_governing_objective_in_triggers_when_specific(self):
        report = _rich_report()
        claims = extract_claims(
            report=report,
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        objective_triggers = [
            t for c in claims
            for t in c.activation_triggers
            if t.startswith("objective:")
        ]
        assert len(objective_triggers) > 0

    def test_claim_types_from_expected_set(self):
        valid_types = {
            "tradeoff", "causal_claim", "strength", "weakness",
            "objective", "observation",
        }
        claims = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        for c in claims:
            assert c.claim_type in valid_types, f"Unexpected type: {c.claim_type}"

    def test_provenance_source_kind(self):
        claims = extract_claims(
            report=_minimal_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        assert all(c.provenance.source_kind == "decision_artifact" for c in claims)

    def test_idempotent_fingerprints_across_runs(self):
        report = _minimal_report()
        claims_a = extract_claims(
            report=report, tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        claims_b = extract_claims(
            report=report, tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        fps_a = sorted(c.fingerprint for c in claims_a)
        fps_b = sorted(c.fingerprint for c in claims_b)
        assert fps_a == fps_b


# ---------------------------------------------------------------------------
# Filter helpers
# ---------------------------------------------------------------------------

class TestFilterHelpers:
    def test_admitted_claims_filter(self):
        claims = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        admitted = admitted_claims(claims)
        assert all(c.admission_status == "admitted" for c in admitted)

    def test_needs_review_filter(self):
        claims = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        review = needs_review_claims(claims)
        assert all(c.admission_status == "needs_review" for c in review)

    def test_admitted_plus_rejected_plus_review_equals_total(self):
        claims = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        admitted = [c for c in claims if c.admission_status == "admitted"]
        rejected = [c for c in claims if c.admission_status == "rejected"]
        review = [c for c in claims if c.admission_status == "needs_review"]
        assert len(admitted) + len(rejected) + len(review) == len(claims)

    def test_admitted_claims_have_content(self):
        claims = extract_claims(
            report=_rich_report(),
            tenant_id="t1", source_envelope_id="e1", actor_id="u1",
        )
        for c in admitted_claims(claims):
            assert len(c.content) >= 20

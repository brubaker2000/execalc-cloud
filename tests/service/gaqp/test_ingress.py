"""Tests for Stage 9H type-specific ingress gates (26 claim types)."""
from __future__ import annotations
import pytest
from src.service.gaqp.ingress import (
    GATE_VERSION, TypeGateResult, _HARD_REJECT_TYPES,
    evaluate_type_gate, gate_enforcement,
)
def _passes(claim_type: str, content: str) -> bool:
    return evaluate_type_gate(content, claim_type).passed
def _result(claim_type: str, content: str) -> TypeGateResult:
    return evaluate_type_gate(content, claim_type)
class TestEnforcement:
    def test_hard_reject_types(self):
        for ct in ("observation", "strength", "weakness", "asset", "liability"):
            assert gate_enforcement(ct) == "rejected", ct
    def test_calibrating_types(self):
        for ct in ("tradeoff", "causal_claim", "objective"):
            assert gate_enforcement(ct) == "needs_review", ct
    def test_unknown_type_needs_review(self):
        assert gate_enforcement("unicorn_type") == "needs_review"
    def test_hard_reject_set_contents(self):
        assert "asset" in _HARD_REJECT_TYPES
        assert "liability" in _HARD_REJECT_TYPES
        assert "observation" in _HARD_REJECT_TYPES
class TestUngatedTypes:
    def test_unknown_passes(self):
        r = _result("unicorn_type", "Any content at all.")
        assert r.passed and r.failed_gates == [] and r.gate_version == GATE_VERSION
    def test_axiom(self): assert _passes("axiom", "x")
    def test_event(self): assert _passes("event", "A thing happened last quarter.")
    def test_tactic(self): assert _passes("tactic", "Deploy pricing pressure in enterprise segment.")
    def test_threat(self): assert _passes("threat", "A competitor is entering our core market.")
    def test_opportunity(self): assert _passes("opportunity", "Expansion into APAC represents significant revenue potential.")
class TestTradeoff:
    def test_pass(self):
        assert _passes("tradeoff", "Higher margins versus lower market share — clear tradeoff in pricing.")
    def test_fail_language(self):
        r = _result("tradeoff", "The company generates strong returns and has a large customer base.")
        assert not r.passed and "comparison_language" in r.failed_gates
    def test_fail_short(self):
        r = _result("tradeoff", "versus x")
        assert not r.passed and "min_length" in r.failed_gates
    def test_vs_no_period(self):
        assert _passes("tradeoff", "Speed vs certainty is the core tension in this time-compressed decision.")
    def test_relative_to(self):
        assert _passes("tradeoff", "Value depends on whether the move advances the objective relative to constraints.")
    def test_upside_downside(self):
        assert _passes("tradeoff", "Peak outcome vs variance — weighing upside against downside risk in portfolio.")
    def test_variants(self):
        for kw in ["at the cost of", "in exchange for", "on the other hand", "trade-off", "balance"]:
            content = f"Increasing speed {kw} quality is the fundamental tension here in this decision."
            assert _passes("tradeoff", content), kw
class TestCausalClaim:
    def test_pass(self):
        assert _passes("causal_claim", "High interest rates lead to reduced consumer borrowing and slower growth.")
    def test_fail(self):
        r = _result("causal_claim", "The market has a large addressable opportunity for expansion.")
        assert not r.passed and "causal_connector" in r.failed_gates
    def test_driven_by(self):
        assert _passes("causal_claim", "Supply is driven by scarcity of the desired outcome and counterparty leverage.")
    def test_depends_on(self):
        assert _passes("causal_claim", "The outcome depends on which party has more room to absorb constraint changes.")
    def test_shaped_by(self):
        assert _passes("causal_claim", "Leverage is shaped by the asymmetry of alternatives available to each side.")
    def test_variants(self):
        for kw in ["because", "results in", "due to", "as a result", "therefore", "consequently"]:
            content = f"The outcome {kw} significant pressure on operating margins over time."
            assert _passes("causal_claim", content), kw
class TestStrength:
    def test_pass(self):
        assert _passes("strength", "Our established distribution network is a proven competitive advantage.")
    def test_fail(self):
        r = _result("strength", "The team works together and serves many customers.")
        assert not r.passed and "capability_language" in r.failed_gates
    def test_hard_reject(self):
        assert gate_enforcement("strength") == "rejected"
    def test_variants(self):
        for kw in ["advantage", "capability", "superior", "differentiated", "reliable"]:
            content = f"Our platform delivers a clear {kw} position versus the nearest alternative."
            assert _passes("strength", content), kw
class TestWeakness:
    def test_pass(self):
        assert _passes("weakness", "Our supply chain is fragile and dependent on a single overseas manufacturer.")
    def test_fail(self):
        r = _result("weakness", "The team is growing and exploring new market opportunities.")
        assert not r.passed and "limitation_language" in r.failed_gates
    def test_hard_reject(self):
        assert gate_enforcement("weakness") == "rejected"
    def test_variants(self):
        for kw in ["liability", "limitation", "deficit", "insufficient", "vulnerable", "absent"]:
            content = f"The organization shows a clear {kw} in technical depth and platform resilience."
            assert _passes("weakness", content), kw
class TestAsset:
    """Asset is the extraction-facing rename of Strength (PR #64)."""
    def test_pass(self):
        assert _passes("asset", "Our established distribution network is a proven competitive advantage.")
    def test_fail(self):
        r = _result("asset", "The team works together and serves many customers.")
        assert not r.passed and "capability_language" in r.failed_gates
    def test_hard_reject(self):
        assert gate_enforcement("asset") == "rejected"
    def test_same_patterns_as_strength(self):
        content = "Our platform delivers a differentiated and trusted capability versus the nearest alternative."
        assert _passes("asset", content)
        assert _passes("strength", content)
class TestLiability:
    """Liability is the extraction-facing rename of Weakness (PR #64)."""
    def test_pass(self):
        assert _passes("liability", "Our supply chain is fragile and dependent on a single overseas manufacturer.")
    def test_fail(self):
        r = _result("liability", "The team is growing and exploring new market opportunities.")
        assert not r.passed and "limitation_language" in r.failed_gates
    def test_hard_reject(self):
        assert gate_enforcement("liability") == "rejected"
    def test_same_patterns_as_weakness(self):
        content = "The organization shows a clear gap and insufficient resilience in the technical infrastructure."
        assert _passes("liability", content)
        assert _passes("weakness", content)
class TestObjective:
    def test_pass(self):
        assert _passes("objective", "Our primary goal is to achieve category leadership within three fiscal years.")
    def test_fail(self):
        r = _result("objective", "The company operates in a competitive environment with many moving parts.")
        assert not r.passed and "goal_language" in r.failed_gates
    def test_preserve_language(self):
        assert _passes("objective", "Respect stated constraints while preserving optionality for future flexibility.")
    def test_maximize_language(self):
        assert _passes("objective", "Structure designed to maximize long-term enterprise value creation effectively.")
    def test_variants(self):
        for kw in ["target", "aim", "pursue", "commit", "aspire", "priority", "mission"]:
            content = f"We {kw} to expand our footprint into underserved enterprise segments."
            assert _passes("objective", content), kw
class TestObservation:
    def test_pass(self):
        assert _passes("observation", "Data shows that churn rates have increased by 12% over the prior three quarters.")
    def test_fail_short(self):
        r = _result("observation", "data")
        assert not r.passed and "min_length" in r.failed_gates
    def test_hard_reject(self):
        assert gate_enforcement("observation") == "rejected"
    def test_factual_statement(self):
        assert _passes("observation", "Revenue is growing at 18% annually across all product lines.")
    def test_variants(self):
        for kw in ["indicates", "suggests", "demonstrates", "reveals", "evidence", "trend"]:
            content = f"The pattern {kw} systemic underinvestment in customer success functions."
            assert _passes("observation", content), kw
class TestConstraint:
    def test_pass(self):
        assert _passes("constraint", "Capital expenditure must not exceed 15% of quarterly revenue under policy.")
    def test_fail(self):
        r = _result("constraint", "The team manages budget carefully across quarters.")
        assert not r.passed and "boundary_language" in r.failed_gates
    def test_variants(self):
        for kw in ["cannot", "limited to", "maximum", "no more than", "at most", "threshold"]:
            content = f"Leverage is {kw} four times EBITDA per the credit facility covenant terms."
            assert _passes("constraint", content), kw
class TestThresholdCondition:
    def test_pass(self):
        assert _passes("threshold_condition", "If churn exceeds 8% in any quarter, then escalate to the executive team immediately.")
    def test_fail_no_antecedent(self):
        r = _result("threshold_condition", "Then we escalate to the executive committee for immediate resolution and action.")
        assert not r.passed and "conditional_antecedent" in r.failed_gates
    def test_fail_no_consequent(self):
        r = _result("threshold_condition", "When churn rises above the threshold the team reviews the situation carefully.")
        assert not r.passed and "conditional_consequent" in r.failed_gates
    def test_both_required(self):
        r = _result("threshold_condition", "Nothing relevant in either clause whatsoever at all here.")
        assert not r.passed
        assert "conditional_antecedent" in r.failed_gates
        assert "conditional_consequent" in r.failed_gates
class TestDiagnosticSignal:
    def test_pass(self):
        assert _passes("diagnostic_signal", "Declining NPS scores are an early indicator of customer experience deterioration.")
    def test_fail(self):
        r = _result("diagnostic_signal", "The product team shipped three major features last quarter on schedule.")
        assert not r.passed and "signal_language" in r.failed_gates
    def test_variants(self):
        for kw in ["symptom", "flag", "warning", "red flag", "anomaly", "correlates", "points to"]:
            content = f"Elevated sales cycle length is a clear {kw} of pipeline quality erosion."
            assert _passes("diagnostic_signal", content), kw
class TestPrinciple:
    def test_pass(self):
        assert _passes("principle", "We should always prioritize long-term customer value over short-term revenue.")
    def test_fail(self):
        r = _result("principle", "The company has grown rapidly and expanded into adjacent markets over time.")
        assert not r.passed and "normative_language" in r.failed_gates
    def test_variants(self):
        for kw in ["ought", "must", "always", "never", "govern", "mandate", "ensure", "uphold"]:
            content = f"Leaders {kw} maintain transparency with the board on capital allocation decisions."
            assert _passes("principle", content), kw
class TestDoctrine:
    def test_pass(self):
        assert _passes("doctrine", "We will never compromise customer data security in exchange for product velocity.")
    def test_fail(self):
        r = _result("doctrine", "The company has a culture of innovation and customer focus across teams.")
        assert not r.passed and "organizational_commitment" in r.failed_gates
    def test_variants(self):
        for kw in ["we do not", "we always", "we never", "our approach", "non-negotiable", "we are committed"]:
            content = f"On capital allocation, {kw} prioritize organic growth over financial engineering always."
            assert _passes("doctrine", content), kw
class TestDeclarationOfValue:
    def test_pass(self):
        assert _passes("declaration_of_value", "We believe that long-term customer trust matters more than short-term profit.")
    def test_fail(self):
        r = _result("declaration_of_value", "The company operates across multiple verticals and serves enterprise clients.")
        assert not r.passed and "value_language" in r.failed_gates
    def test_variants(self):
        for kw in ["value", "commitment", "matters", "conviction", "care", "prioritize", "at our core"]:
            content = f"Our {kw} is that transparency drives better outcomes for all stakeholders here."
            assert _passes("declaration_of_value", content), kw
class TestToDict:
    def test_structure(self):
        d = _result("tradeoff", "Too short").to_dict()
        assert set(d.keys()) == {"claim_type", "passed", "failed_gates", "recommendations", "gate_version"}
        assert d["claim_type"] == "tradeoff"
        assert d["passed"] is False
        assert d["gate_version"] == GATE_VERSION
    def test_passed(self):
        d = _result("axiom", "any content").to_dict()
        assert d["passed"] is True and d["failed_gates"] == []

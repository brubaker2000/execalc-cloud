"""Tests for Stage 9G type-specific ingress gates."""
from __future__ import annotations
import pytest
from src.service.gaqp.ingress import GATE_VERSION, TypeGateResult, evaluate_type_gate

def _p(ct, c): return evaluate_type_gate(c, ct).passed
def _r(ct, c): return evaluate_type_gate(c, ct)

class TestUngatedTypes:
    def test_unknown_passes(self): assert _r("unicorn","Any content.").passed
    def test_axiom(self): assert _p("axiom","x")

class TestTradeoff:
    def test_pass(self): assert _p("tradeoff","Higher margins versus lower market share -- clear tradeoff in pricing.")
    def test_fail_language(self):
        r = _r("tradeoff","The company generates strong returns and has a large customer base.")
        assert not r.passed and "comparison_language" in r.failed_gates
    def test_fail_short(self):
        r = _r("tradeoff","versus x")
        assert not r.passed and "min_length" in r.failed_gates

class TestCausalClaim:
    def test_pass(self): assert _p("causal_claim","High interest rates lead to reduced consumer borrowing and slower growth.")
    def test_fail(self):
        r = _r("causal_claim","The market has a large addressable opportunity for expansion.")
        assert not r.passed and "causal_connector" in r.failed_gates

class TestThresholdCondition:
    def test_pass(self): assert _p("threshold_condition","If churn exceeds 8% in any quarter, then escalate to the executive team immediately.")
    def test_fail_both(self):
        r = _r("threshold_condition","Nothing relevant in either clause whatsoever at all here.")
        assert not r.passed
        assert "conditional_antecedent" in r.failed_gates
        assert "conditional_consequent" in r.failed_gates

class TestToDict:
    def test_structure(self):
        d = _r("tradeoff","Too short").to_dict()
        assert set(d.keys()) == {"claim_type","passed","failed_gates","recommendations","gate_version"}
        assert d["gate_version"] == GATE_VERSION

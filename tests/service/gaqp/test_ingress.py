from src.service.gaqp.ingress import GATE_VERSION,_HARD_REJECT_TYPES,evaluate_type_gate,gate_enforcement
def _p(ct,c): return evaluate_type_gate(c,ct).passed
def _r(ct,c): return evaluate_type_gate(c,ct)
class TestEnforcement:
    def test_hard(self):
        for ct in ("observation","strength","weakness"): assert gate_enforcement(ct)=="rejected"
    def test_soft(self):
        for ct in ("tradeoff","causal_claim","objective"): assert gate_enforcement(ct)=="needs_review"
class TestUngated:
    def test_unknown(self): assert _r("x","Any content.").passed
    def test_axiom(self): assert _p("axiom","x")
class TestTradeoff:
    def test_pass(self): assert _p("tradeoff","Higher margins versus lower market share -- clear tradeoff in pricing.")
    def test_fail(self):
        r=_r("tradeoff","The company generates strong returns.")
        assert not r.passed and "comparison_language" in r.failed_gates
    def test_vs(self): assert _p("tradeoff","Speed vs certainty is the core tension in this time-compressed decision.")
    def test_relative(self): assert _p("tradeoff","Value depends on move advancing the objective relative to stated constraints here.")
class TestCausal:
    def test_pass(self): assert _p("causal_claim","High rates lead to reduced borrowing and slower economic growth.")
    def test_fail(self):
        r=_r("causal_claim","The market has a large addressable opportunity for expansion.")
        assert not r.passed and "causal_connector" in r.failed_gates
    def test_driven_by(self): assert _p("causal_claim","Supply is driven by scarcity of the desired outcome and counterparty leverage.")
    def test_depends_on(self): assert _p("causal_claim","Outcome depends on which party has more room to absorb constraint changes here.")
class TestStrength:
    def test_pass(self): assert _p("strength","Our distribution network is a proven competitive advantage in this market.")
    def test_fail(self):
        r=_r("strength","The team works and serves customers.")
        assert not r.passed and "capability_language" in r.failed_gates
    def test_hard(self): assert gate_enforcement("strength")=="rejected"
class TestWeakness:
    def test_pass(self): assert _p("weakness","Supply chain is fragile and dependent on a single overseas manufacturer.")
    def test_hard(self): assert gate_enforcement("weakness")=="rejected"
class TestObjective:
    def test_pass(self): assert _p("objective","Our primary goal is to achieve category leadership within three fiscal years.")
    def test_preserve(self): assert _p("objective","Respect constraints while preserving optionality for future flexibility always.")
    def test_maximize(self): assert _p("objective","Structure designed to maximize long-term enterprise value creation effectively.")
class TestObservation:
    def test_pass(self): assert _p("observation","Data shows churn rates increased by 12 percent over prior three quarters.")
    def test_hard(self): assert gate_enforcement("observation")=="rejected"
class TestThreshold:
    def test_pass(self): assert _p("threshold_condition","If churn exceeds 8 percent in any quarter, then escalate to executive team immediately.")
    def test_fail_both(self):
        r=_r("threshold_condition","Nothing relevant in either clause whatsoever at all here.")
        assert not r.passed
        assert "conditional_antecedent" in r.failed_gates and "conditional_consequent" in r.failed_gates
class TestToDict:
    def test_keys(self):
        d=_r("tradeoff","Too short").to_dict()
        assert set(d.keys())=={"claim_type","passed","failed_gates","recommendations","gate_version"}
        assert d["gate_version"]==GATE_VERSION

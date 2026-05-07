from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
GATE_VERSION = "9g_v1"
@dataclass(frozen=True)
class TypeGateResult:
    claim_type: str
    passed: bool
    failed_gates: List[str]
    recommendations: List[str]
    gate_version: str = GATE_VERSION
    def to_dict(self) -> Dict:
        return {"claim_type": self.claim_type, "passed": self.passed, "failed_gates": self.failed_gates, "recommendations": self.recommendations, "gate_version": self.gate_version}
@dataclass(frozen=True)
class _GateSpec:
    pattern_groups: List[List[str]]
    min_length: int
    gate_labels: List[str]
    recommendations: List[str]
_GATE_SPECS = {
    "tradeoff": _GateSpec([["versus","vs.","at the cost of","trade-off","tradeoff","compared to","in exchange for","either","sacrifice","on the other hand","offset","balance"]], 40, ["comparison_language"], ["Tradeoff claims must contain explicit comparison language (versus / at the cost of / in exchange for)."]),
    "causal_claim": _GateSpec([["because","leads to","lead to","results in","result in","drives","causes","caused by","due to","as a result","therefore","consequently","which means","producing","generates","creates pressure","compresses","suppresses"]], 30, ["causal_connector"], ["Causal claims must contain an explicit causal connector (leads to / results in / because / due to)."]),
    "strength": _GateSpec([["advantage","strength","capability","asset","competitive","superior","effective","strong","robust","proven","differentiated","established","reliable","efficient","trusted","leading","best-in-class"]], 25, ["capability_language"], ["Strength claims must describe an explicit organizational capability, asset, or competitive advantage."]),
    "weakness": _GateSpec([["weakness","liability","limitation","constraint","gap","deficit","insufficient","lacking","risk","exposure","vulnerable","underdeveloped","dependent","costly","fragile","absent","missing","slow"]], 25, ["limitation_language"], ["Weakness claims must describe an explicit organizational limitation, liability, or gap."]),
    "objective": _GateSpec([["goal","objective","target","aim","achieve","seek","pursue","intend","commit","aspire","priority","ambition","mission","purpose","drive toward"]], 25, ["goal_language"], ["Objective claims must contain explicit goal or target language (goal / objective / target / aim to achieve)."]),
    "observation": _GateSpec([["indicates","suggests","shows","demonstrates","reveals","found","observed","noted","appears","evident","data","evidence","pattern","trend","signal","recorded","measured","reported","confirmed","is ","are ","was ","were ","has ","have "]], 30, ["epistemic_grounding"], ["Observation claims should contain epistemic grounding (indicates / suggests / data shows / we observed)."]),
    "constraint": _GateSpec([["must not","cannot","limited to","cap","ceiling","floor","maximum","minimum","not exceed","boundary","hard limit","no more than","at most","at least","threshold","restricted"]], 25, ["boundary_language"], ["Constraint claims must specify an explicit boundary or limit (must not / cannot exceed / limited to / ceiling of)."]),
    "threshold_condition": _GateSpec([["if ","when ","once ","should ","above ","below ","exceeds","falls below","rises above","triggers","crosses"],["then","result","leads","causes","activate","fire","escalate","flag","require","recommend","warrant"]], 35, ["conditional_antecedent","conditional_consequent"], ["Threshold conditions must specify the trigger condition (if / when / once / above / below).","Threshold conditions must specify the consequence (then / leads to / triggers / requires)."]),
    "diagnostic_signal": _GateSpec([["indicator","signal","symptom","flag","warning","early sign","red flag","pattern","anomaly","suggests","indicates","points to","correlates"]], 30, ["signal_language"], ["Diagnostic signal claims must identify an observable indicator (indicator of / signal / symptom / red flag)."]),
    "principle": _GateSpec([["should","ought","must","always","never","principle","govern","rule","standard","require","dictate","mandate","ensure","uphold"]], 30, ["normative_language"], ["Principle claims must contain normative language (should / must / always / never / governs)."]),
    "doctrine": _GateSpec([["doctrine","policy","we will","we do not","we always","we never","our approach","non-negotiable","standing rule","organizational commitment","we are committed"]], 35, ["organizational_commitment"], ["Doctrine claims must express an explicit organizational commitment (we will / we never / our policy / non-negotiable)."]),
    "declaration_of_value": _GateSpec([["we believe","value","commitment","matters","conviction","principle","care","prioritize","stand for","at our core","what we stand for"]], 30, ["value_language"], ["Declaration of value claims must express an explicit value or belief (we believe / value / commitment to / what matters)."]),
}
def evaluate_type_gate(content: str, claim_type: str) -> TypeGateResult:
    spec = _GATE_SPECS.get(claim_type)
    if spec is None:
        return TypeGateResult(claim_type=claim_type, passed=True, failed_gates=[], recommendations=[], gate_version=GATE_VERSION)
    lower = (content or "").lower()
    failed_gates: List[str] = []
    recommendations: List[str] = []
    if len((content or "").strip()) < spec.min_length:
        failed_gates.append("min_length")
        recommendations.append(f"Content is below the minimum length ({spec.min_length} chars) for a {claim_type} claim.")
    for group, label, rec in zip(spec.pattern_groups, spec.gate_labels, spec.recommendations):
        if not any(p in lower for p in group):
            failed_gates.append(label)
            recommendations.append(rec)
    passed = len(failed_gates) == 0
    return TypeGateResult(claim_type=claim_type, passed=passed, failed_gates=failed_gates, recommendations=recommendations, gate_version=GATE_VERSION)

from typing import Any, Dict, List


class GuardrailResult:
    def __init__(self, ok: bool, violations: List[str]):
        self.ok = ok
        self.violations = violations


def evaluate_decision_guardrails(action_proposal: Dict[str, Any]) -> GuardrailResult:
    violations = []
    if "tradeoffs" not in action_proposal:
        violations.append("missing_tradeoffs")
    if "alternatives" not in action_proposal:
        violations.append("missing_alternatives")
    if "risk_assessment" not in action_proposal:
        violations.append("missing_risk_assessment")
    ok = len(violations) == 0
    return GuardrailResult(ok=ok, violations=violations)

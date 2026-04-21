from typing import Any, Dict, List


class StabilityInvariantResult:
    def __init__(self, ok: bool, violations: List[str]):
        self.ok = ok
        self.violations = violations


def evaluate_stability_invariants(action_proposal: Dict[str, Any]) -> StabilityInvariantResult:
    violations = []
    if not action_proposal.get("proposal_id"):
        violations.append("missing_proposal_id")
    if not action_proposal.get("governing_objective"):
        violations.append("missing_governing_objective")
    if "assumptions" not in action_proposal:
        violations.append("missing_assumptions")
    if "constraints" not in action_proposal:
        violations.append("missing_constraints")
    if not action_proposal.get("scenario_type"):
        violations.append("missing_scenario_type")
    ok = len(violations) == 0
    return StabilityInvariantResult(ok=ok, violations=violations)

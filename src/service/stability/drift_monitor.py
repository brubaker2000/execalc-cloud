from typing import Any, Dict, List


class DriftSignal:
    def __init__(self, drift_detected: bool, reasons: List[str] | None = None):
        self.drift_detected = drift_detected
        self.reasons = reasons or []


def evaluate_runtime_drift(action_proposal: Dict[str, Any]) -> DriftSignal:
    reasons = []
    if not action_proposal.get("created_at"):
        reasons.append("missing_timestamp")
    if not action_proposal.get("environment_version"):
        reasons.append("missing_environment_version")
    drift_detected = len(reasons) > 0
    return DriftSignal(drift_detected=drift_detected, reasons=reasons)

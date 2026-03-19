from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple


CONFIDENCE_SCORE = {
    "unknown": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}


def _artifact_label(envelope_id: str, artifact: Dict[str, Any]) -> str:
    report = artifact.get("report") or {}
    objective = str(report.get("governing_objective") or "unspecified_objective")
    return f"{objective}:{envelope_id[:8]}"


def _sensitivity_count(artifact: Dict[str, Any]) -> int:
    report = artifact.get("report") or {}
    sensitivity = report.get("sensitivity") or []
    return len(sensitivity) if isinstance(sensitivity, list) else 0


def _confidence_value(artifact: Dict[str, Any]) -> int:
    report = artifact.get("report") or {}
    confidence = str(report.get("confidence") or "unknown").lower()
    return CONFIDENCE_SCORE.get(confidence, 0)


def _objective_alignment_score(
    artifact: Dict[str, Any],
    comparison_objective: str,
) -> int:
    report = artifact.get("report") or {}
    artifact_objective = str(report.get("governing_objective") or "").strip()
    if not comparison_objective:
        return 0
    return 1 if artifact_objective == comparison_objective else 0


def _tradeoff_counts(artifact: Dict[str, Any]) -> Dict[str, int]:
    report = artifact.get("report") or {}
    tradeoffs = report.get("tradeoffs") or {}
    if not isinstance(tradeoffs, dict):
        return {"upside": 0, "downside": 0, "key_tradeoffs": 0, "asymmetry": 0}
    return {
        "upside": len(tradeoffs.get("upside") or []),
        "downside": len(tradeoffs.get("downside") or []),
        "key_tradeoffs": len(tradeoffs.get("key_tradeoffs") or []),
        "asymmetry": len(tradeoffs.get("asymmetry") or []),
    }


def compare_decision_artifacts(
    *,
    tenant_id: str,
    artifacts: List[Dict[str, Any]],
    comparison_objective: str,
    requested_depth: str,
) -> Dict[str, Any]:
    """
    Deterministic Stage 7B comparison engine.

    Compares already-retrieved decision artifacts and returns a stable,
    structured comparison report.
    """
    if len(artifacts) < 2:
        raise ValueError("at least two decision artifacts are required")

    normalized: List[Dict[str, Any]] = []
    for item in artifacts:
        envelope_id = str(item.get("envelope_id") or "")
        result = item.get("result") or {}
        if not envelope_id or not isinstance(result, dict):
            raise ValueError("invalid decision artifact")
        normalized.append(
            {
                "envelope_id": envelope_id,
                "artifact": result,
                "label": _artifact_label(envelope_id, result),
                "confidence_score": _confidence_value(result),
                "sensitivity_count": _sensitivity_count(result),
                "objective_alignment": _objective_alignment_score(result, comparison_objective),
                "tradeoff_counts": _tradeoff_counts(result),
            }
        )

    normalized.sort(
        key=lambda x: (
            x["objective_alignment"],
            x["confidence_score"],
            -x["sensitivity_count"],
        ),
        reverse=True,
    )

    preferred = normalized[0]
    report0 = preferred["artifact"].get("report") or {}

    decision_set = [
        {
            "envelope_id": item["envelope_id"],
            "label": item["label"],
            "confidence": (item["artifact"].get("report") or {}).get("confidence"),
            "governing_objective": (item["artifact"].get("report") or {}).get("governing_objective"),
        }
        for item in normalized
    ]

    objectives = {
        str((item["artifact"].get("report") or {}).get("governing_objective") or "unspecified_objective")
        for item in normalized
    }
    scenario_types = {
        str((item["artifact"].get("audit") or {}).get("scenario_type") or "unknown")
        for item in normalized
    }

    what_changed: List[str] = []
    if len(objectives) > 1:
        what_changed.append("Compared decisions were produced under different governing objectives.")
    sensitivity_counts = {item["sensitivity_count"] for item in normalized}
    if len(sensitivity_counts) > 1:
        what_changed.append("The compared decisions carry different levels of sensitivity / missing-input burden.")
    confidence_scores = {item["confidence_score"] for item in normalized}
    if len(confidence_scores) > 1:
        what_changed.append("Confidence differs across the compared decisions.")
    if not what_changed:
        what_changed.append("The major differences are limited; the decision set is structurally similar.")

    what_stayed_constant: List[str] = []
    if len(scenario_types) == 1:
        what_stayed_constant.append(f"All compared decisions share the same scenario type: {next(iter(scenario_types))}.")
    if len(objectives) == 1:
        what_stayed_constant.append(f"All compared decisions share the same governing objective: {next(iter(objectives))}.")
    if not what_stayed_constant:
        what_stayed_constant.append("Each decision remains tenant-scoped and structurally comparable through the governed artifact schema.")

    tradeoff_shift_analysis: List[str] = []
    for item in normalized:
        counts = item["tradeoff_counts"]
        tradeoff_shift_analysis.append(
            f'{item["label"]} carries {counts["upside"]} upside items, '
            f'{counts["downside"]} downside items, '
            f'{counts["key_tradeoffs"]} key trade-off notes, and '
            f'{counts["asymmetry"]} asymmetry notes.'
        )

    objective_alignment: List[Dict[str, Any]] = []
    for item in normalized:
        report = item["artifact"].get("report") or {}
        objective_alignment.append(
            {
                "envelope_id": item["envelope_id"],
                "label": item["label"],
                "governing_objective": report.get("governing_objective"),
                "alignment": (
                    "direct"
                    if comparison_objective and item["objective_alignment"] == 1
                    else "indirect"
                ),
            }
        )

    fragility_lines = []
    for item in normalized:
        fragility_lines.append(
            {
                "envelope_id": item["envelope_id"],
                "label": item["label"],
                "sensitivity_count": item["sensitivity_count"],
                "fragility": (
                    "more_robust" if item["sensitivity_count"] == min(i["sensitivity_count"] for i in normalized)
                    else "more_fragile"
                ),
            }
        )

    preferred_label = preferred["label"]
    preferred_envelope = preferred["envelope_id"]
    comparison_summary = (
        f"Under the comparison objective '{comparison_objective or 'unspecified_objective'}', "
        f"{preferred_label} currently appears strongest because it combines the best objective fit, "
        f"the strongest available confidence posture, and the lowest visible fragility among the compared artifacts."
    )

    recommendation = {
        "preferred_envelope_id": preferred_envelope,
        "preferred_label": preferred_label,
        "rationale": (
            "Preferred option selected by deterministic comparison of objective alignment, "
            "confidence, and sensitivity burden."
        ),
        "conditions_that_change_recommendation": [
            "If a lower-ranked option gains stronger objective alignment under a revised comparison objective.",
            "If new facts materially reduce fragility or increase confidence for another option.",
            "If the operator prioritizes a different governing objective than the one used for this comparison.",
        ],
    }

    next_actions = [
        "Review the preferred artifact and validate that the comparison objective is still the correct lens.",
        "Pressure-test the sensitivity variables for the preferred and nearest competing option.",
        "Confirm whether any missing inputs could change the ranking materially.",
        "Advance the preferred option only if its governing objective still matches current operator intent.",
    ]

    return {
        "ok": True,
        "comparison_report": {
            "comparison_summary": comparison_summary,
            "decision_set": decision_set,
            "what_changed": what_changed,
            "what_stayed_constant": what_stayed_constant,
            "tradeoff_shift_analysis": tradeoff_shift_analysis,
            "governing_objective_alignment": objective_alignment,
            "sensitivity_and_fragility": fragility_lines,
            "recommendation": recommendation,
            "next_actions": next_actions,
        },
        "audit": {
            "tenant_id": tenant_id,
            "compared_envelope_ids": [item["envelope_id"] for item in normalized],
            "comparison_objective": comparison_objective or "unspecified_objective",
            "requested_depth": requested_depth or "standard",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "stage7b_v1",
        },
    }

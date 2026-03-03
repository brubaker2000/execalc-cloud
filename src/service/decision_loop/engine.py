from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from src.service.decision_loop.models import DecisionReport, Scenario, SensitivityVariable


CRITICAL_FIELDS_BY_SCENARIO: Dict[str, List[str]] = {
    # Draft-day example fields (future evaluators will use richer structures)
    "draft_trade": ["you_pick", "counterparty_pick"],
    # Generic feasibility
    "feasibility": ["objective", "resources", "timeline"],
}


def _missing_critical(s: Scenario) -> List[SensitivityVariable]:
    required = CRITICAL_FIELDS_BY_SCENARIO.get(s.scenario_type, [])
    missing = [k for k in required if k not in (s.facts or {})]
    out: List[SensitivityVariable] = []
    for k in missing:
        out.append(
            SensitivityVariable(
                name=k,
                impact=(
                    "Missing input could change the calculus and the confidence level; "
                    "provide this to tighten the recommendation."
                ),
            )
        )
    return out


def run_decision_loop(*, tenant_id: str, user_id: str, scenario: Scenario) -> DecisionReport:
    """
    Stage 4A: deterministic structured output.
    - No hallucinated facts
    - Explicit missing-data sensitivity
    - Governing objective drives framing language
    """

    sensitivity = _missing_critical(scenario)

    # Confidence rule (Stage 4A):
    # - unknown if missing critical fields
    # - medium otherwise (until real evaluators are wired)
    if sensitivity:
        confidence = "unknown"
        rationale = ["Critical inputs are missing; recommendation is constrained by data completeness."]
    else:
        confidence = "medium"
        rationale = ["Structured analysis produced from provided inputs; deeper evaluators will increase certainty."]

    # Executive summary: objective-aware phrasing without exposing mechanics
    obj = (scenario.governing_objective or "").strip() or "unspecified_objective"
    if obj in ("cut_payroll", "reduce_cap", "cap_cut"):
        summary = (
            "Under a payroll reduction mandate, prioritize cost-controlled flexibility and avoid moves that "
            "increase fixed commitments without compensating surplus value."
        )
        upside = [
            "Cap flexibility improves optionality.",
            "Cost-controlled contributors become more valuable than marginal veteran spend.",
        ]
        downside = [
            "Star probability may decrease if you trade down without surplus compensation.",
            "Variance rises; development strength matters.",
        ]
    else:
        summary = (
            "Given the stated objective, evaluate the trade-off between expected upside, downside exposure, "
            "and the sensitivity variables that could materially change the outcome."
        )
        upside = [
            "Higher expected upside if critical assumptions hold.",
            "Better alignment if constraints are satisfied.",
        ]
        downside = [
            "Downside increases if missing variables break against you.",
            "Confidence remains limited until key inputs are provided.",
        ]

    tradeoffs = {
        "upside": upside,
        "downside": downside,
        "key_tradeoffs": [
            "Speed vs certainty (time-compressed decision vs missing inputs).",
            "Peak outcome vs variance control (especially under constrained objectives).",
        ],
        "asymmetry": [
            "If you can shift risk to the counterparty while preserving upside, the deal becomes structurally favorable."
        ],
    }

    next_actions = [
        "Confirm governing objective and constraints (cap, payroll, timeline).",
        "Fill any missing critical inputs listed in sensitivity variables.",
        "Request 2–3 alternative deal structures and compare under the same objective.",
        "Run a downside-first scan: identify the failure mode that hurts most.",
        "Make a go/no-go decision and document the rationale for accountability.",
    ]

    audit = {
        "tenant_id": tenant_id,
        "user_id": user_id,
        "scenario_type": scenario.scenario_type,
        "governing_objective": scenario.governing_objective,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "version": "stage4a",
    }

    return DecisionReport(
        executive_summary=summary,
        confidence=confidence,  # type: ignore
        confidence_rationale=rationale,
        governing_objective=scenario.governing_objective,
        tradeoffs=tradeoffs,
        sensitivity=sensitivity,
        next_actions=next_actions,
        audit=audit,
    )

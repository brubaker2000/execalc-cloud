from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from src.service.decision_loop.models import DecisionReport, Scenario, SensitivityVariable
from src.service.decision_loop.support_stack import support_stack_trace


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


def _nonempty_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _listify(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def _build_prime_directive_assessments(
    scenario: Scenario,
    sensitivity: List[SensitivityVariable],
) -> Dict[str, str]:
    facts = scenario.facts or {}
    constraints = scenario.constraints or {}
    missing_names = [s.name for s in sensitivity]

    fact_keys = sorted(str(k) for k in facts.keys())
    constraint_keys = sorted(str(k) for k in constraints.keys())

    objective = _nonempty_str(scenario.governing_objective) or "unspecified_objective"
    horizon = _nonempty_str(scenario.decision_horizon)
    risk_surface = _nonempty_str(scenario.risk_surface)
    assumptions = _nonempty_str(scenario.assumptions)
    notes = _nonempty_str(scenario.decision_notes)

    if sensitivity:
        value_assessment = (
            "Value cannot be fully underwritten yet because critical inputs are missing: "
            + ", ".join(missing_names)
            + ". Preserve flexibility until the missing inputs are confirmed."
        )
    elif objective in ("cut_payroll", "reduce_cap", "cap_cut"):
        value_assessment = (
            "Value is created if the move improves flexibility and reduces fixed commitments "
            "without surrendering too much surplus upside."
        )
    else:
        value_assessment = (
            "Value depends on whether the move advances the governing objective while preserving "
            "enough upside relative to the stated constraints."
        )

    if risk_surface:
        risk_reward_assessment = (
            "Risk/reward should be evaluated against the stated risk surface: "
            f"{risk_surface}. "
            "If downside concentration is unacceptable, bias toward reversibility and option value."
        )
    elif sensitivity:
        risk_reward_assessment = (
            "Risk is currently harder to price than reward because missing inputs reduce confidence. "
            "Downside protection should dominate until the decision picture is complete."
        )
    else:
        risk_reward_assessment = (
            "Risk/reward is presently balanced at a medium-confidence level: the structure is analyzable, "
            "but additional evaluators or deeper facts would improve underwriting."
        )

    if objective in ("cut_payroll", "reduce_cap", "cap_cut"):
        supply_demand_assessment = (
            "Supply/demand should be viewed through the market for cost-controlled flexibility. "
            "If counterparties value immediate certainty more than you do, there may be room to extract surplus."
        )
    else:
        supply_demand_assessment = (
            "Supply/demand is driven by scarcity of the desired outcome, counterparty leverage, "
            "and the opportunity cost of waiting."
        )

    asset_parts: List[str] = []
    if fact_keys:
        asset_parts.append("available facts: " + ", ".join(fact_keys))
    if horizon:
        asset_parts.append(f"decision horizon: {horizon}")
    if notes:
        asset_parts.append("operator notes captured")
    if not asset_parts:
        asset_parts.append("the current prompt and structured context")

    asset_assessment = (
        "Primary assets in this decision are "
        + "; ".join(asset_parts)
        + ". These are the components currently strengthening the decision posture."
    )

    liability_parts: List[str] = []
    if missing_names:
        liability_parts.append("missing inputs: " + ", ".join(missing_names))
    if constraint_keys:
        liability_parts.append("stated constraints: " + ", ".join(constraint_keys))
    if assumptions:
        liability_parts.append("untested assumptions present")
    if not liability_parts:
        liability_parts.append("no major structural liabilities identified beyond normal execution risk")

    liability_assessment = (
        "Primary liabilities in this decision are "
        + "; ".join(liability_parts)
        + ". These are the factors most likely to impair execution or erode value."
    )

    return {
        "value_assessment": value_assessment,
        "risk_reward_assessment": risk_reward_assessment,
        "supply_demand_assessment": supply_demand_assessment,
        "asset_assessment": asset_assessment,
        "liability_assessment": liability_assessment,
    }


def _build_polymorphia_fields(
    scenario: Scenario,
    sensitivity: List[SensitivityVariable],
) -> Dict[str, List[str]]:
    facts = scenario.facts or {}
    constraints = scenario.constraints or {}

    actors: List[str] = []
    actors.extend(_listify(facts.get("actors")))
    actors.extend(_listify(facts.get("stakeholders")))
    if scenario.stakeholder_scope:
        actors.extend(_listify(scenario.stakeholder_scope))
    if scenario.operator_id:
        actors.append(f"operator:{scenario.operator_id}")

    deduped_actors: List[str] = []
    for actor in actors:
        if actor not in deduped_actors:
            deduped_actors.append(actor)
    if not deduped_actors:
        deduped_actors = ["operator", "counterparty", "affected stakeholders"]

    objective = _nonempty_str(scenario.governing_objective) or "unspecified_objective"

    incentives: List[str] = [f"Advance governing objective: {objective}"]
    if constraints:
        incentives.append("Respect stated constraints while preserving optionality")
    if scenario.risk_surface:
        incentives.append(f"Manage risk surface: {scenario.risk_surface}")
    if scenario.decision_horizon:
        incentives.append(f"Align with decision horizon: {scenario.decision_horizon}")
    if len(incentives) == 1:
        incentives.append("Improve decision quality without increasing hidden exposure")

    asymmetries: List[str] = []
    if sensitivity:
        asymmetries.append(
            "Information asymmetry is elevated because missing critical inputs reduce underwriting confidence."
        )
    if objective in ("cut_payroll", "reduce_cap", "cap_cut"):
        asymmetries.append(
            "A party with more balance-sheet flexibility may command better terms under a payroll-constrained objective."
        )
    if constraints:
        asymmetries.append(
            "The side with more room to absorb or reshape constraints usually has leverage."
        )
    if scenario.assumptions:
        asymmetries.append(
            "Unvalidated assumptions can create hidden asymmetry if the counterparty has better information."
        )
    if not asymmetries:
        asymmetries.append(
            "Leverage will likely flow to the side with better information, patience, and structural flexibility."
        )

    return {
        "actors": deduped_actors,
        "incentives": incentives,
        "asymmetries": asymmetries,
    }


def run_decision_loop(*, tenant_id: str, user_id: str, scenario: Scenario) -> DecisionReport:
    """
    Stage 4A: deterministic structured output.
    - No hallucinated facts
    - Explicit missing-data sensitivity
    - Governing objective drives framing language
    """

    sensitivity = _missing_critical(scenario)

    if sensitivity:
        confidence = "unknown"
        rationale = ["Critical inputs are missing; recommendation is constrained by data completeness."]
    else:
        confidence = "medium"
        rationale = ["Structured analysis produced from provided inputs; deeper evaluators will increase certainty."]

    if scenario.decision_horizon:
        rationale.append(f"Decision horizon provided: {scenario.decision_horizon}.")
    if scenario.risk_surface:
        rationale.append(f"Risk surface noted: {scenario.risk_surface}.")
    if scenario.assumptions:
        rationale.append("Explicit assumptions were provided and should be tested before commitment.")

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

    if scenario.decision_horizon:
        upside.append(f"Decision horizon is explicitly defined: {scenario.decision_horizon}.")
    if scenario.stakeholder_scope:
        downside.append(f"Stakeholder complexity is in scope: {scenario.stakeholder_scope}.")
    if scenario.risk_surface:
        downside.append(f"Risk surface requires active management: {scenario.risk_surface}.")

    tradeoffs = {
        "upside": upside,
        "downside": downside,
        "key_tradeoffs": [
            "Speed vs certainty (time-compressed decision vs missing inputs).",
            "Peak outcome vs variance control (especially under constrained objectives).",
            "Flexibility today vs commitment burden tomorrow.",
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
    if scenario.assumptions:
        next_actions.insert(2, "Pressure-test the stated assumptions before committing capital or credibility.")
    if scenario.stakeholder_scope:
        next_actions.append("Map stakeholder reactions and identify who benefits, resists, or loses leverage.")

    prime = _build_prime_directive_assessments(scenario, sensitivity)
    polymorphia = _build_polymorphia_fields(scenario, sensitivity)

    execution_trace = {
        "scenario_type": scenario.scenario_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actions_taken": [
            "validated critical fields",
            "assigned confidence from data completeness",
            "generated tradeoff analysis",
            "generated prime directive assessments",
            "generated polymorphia fields",
            "generated support stack trace",
        ],
        "context_used": {
            "decision_horizon": scenario.decision_horizon,
            "stakeholder_scope": scenario.stakeholder_scope,
            "risk_surface": scenario.risk_surface,
            "assumptions_present": bool(scenario.assumptions),
            "decision_notes_present": bool(scenario.decision_notes),
        },
        "support_stack": support_stack_trace(missing_critical_fields=[s.name for s in sensitivity]),
    }

    audit = {
        "tenant_id": tenant_id,
        "user_id": user_id,
        "scenario_type": scenario.scenario_type,
        "governing_objective": scenario.governing_objective,
        "workspace_id": scenario.workspace_id,
        "project_id": scenario.project_id,
        "chat_id": scenario.chat_id,
        "thread_id": scenario.thread_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "version": "stage4b",
    }

    return DecisionReport(
        executive_summary=summary,
        confidence=confidence,
        confidence_rationale=rationale,
        governing_objective=scenario.governing_objective,
        tradeoffs=tradeoffs,
        sensitivity=sensitivity,
        next_actions=next_actions,
        audit=audit,
        value_assessment=prime["value_assessment"],
        risk_reward_assessment=prime["risk_reward_assessment"],
        supply_demand_assessment=prime["supply_demand_assessment"],
        asset_assessment=prime["asset_assessment"],
        liability_assessment=prime["liability_assessment"],
        actors=polymorphia["actors"],
        incentives=polymorphia["incentives"],
        asymmetries=polymorphia["asymmetries"],
        execution_trace=execution_trace,
    )

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict, Optional

from src.service.orchestration.models import ScenarioEnvelope, TurnClass


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def classify_turn(user_text: str) -> TurnClass:
    text = (user_text or "").strip().lower()

    if any(phrase in text for phrase in ["send it", "approve this", "run the next step", "go ahead"]):
        return "execution_seeking"

    if any(phrase in text for phrase in ["draft the next move", "prepare the outreach", "generate the action"]):
        return "action_proposing"

    if any(phrase in text for phrase in ["what evidence", "pull the relevant docs", "what internal data"]):
        return "evidence_seeking"

    if any(phrase in text for phrase in ["which option is better", "evaluate this", "what should we do"]):
        return "decision_seeking"

    return "conversational"


def build_scenario_envelope(
    *,
    user_text: str,
    turn_class: TurnClass,
    scenario_type: str = "general",
    governing_objective: str = "unspecified",
    relevant_constraints: Optional[Dict[str, Any]] = None,
) -> ScenarioEnvelope:
    now = datetime.now(UTC)
    return ScenarioEnvelope(
        scenario_id=f"scenario_{int(now.timestamp())}",
        scenario_type=scenario_type,
        governing_objective=governing_objective,
        user_intent=turn_class,
        prompt=user_text,
        relevant_constraints=relevant_constraints or {},
        decision_state="pending" if turn_class in ("decision_seeking", "action_proposing", "execution_seeking") else "not_requested",
        action_state="pending" if turn_class in ("action_proposing", "execution_seeking") else "not_requested",
        created_at=now,
        updated_at=now,
    )


def route_turn(
    *,
    turn_class: TurnClass,
    scenario: ScenarioEnvelope,
) -> Dict[str, Any]:
    if turn_class == "decision_seeking":
        return {
            "decision_result": {"ok": True, "status": "stubbed"},
            "action_proposal": None,
            "execution_boundary_result": None,
            "assistant_message": "Decision path selected.",
            "rail_state": {"mode": "decision"},
        }

    if turn_class == "action_proposing":
        return {
            "decision_result": {"ok": True, "status": "stubbed"},
            "action_proposal": {
                "proposal_id": f"proposal_{scenario.scenario_id}",
                "scenario_id": scenario.scenario_id,
                "action_type": "proposed_action",
                "action_payload": {"source_prompt": scenario.prompt},
                "assumptions": [],
                "constraints": scenario.relevant_constraints,
                "approval_thresholds": {},
                "confidence": "unknown",
                "created_at": _now_iso(),
            },
            "execution_boundary_result": None,
            "assistant_message": "Action proposal path selected.",
            "rail_state": {"mode": "action_proposal"},
        }

    if turn_class == "execution_seeking":
        return {
            "decision_result": None,
            "action_proposal": {
                "proposal_id": f"proposal_{scenario.scenario_id}",
                "scenario_id": scenario.scenario_id,
                "action_type": "execution_requested",
                "action_payload": {"source_prompt": scenario.prompt},
                "assumptions": [],
                "constraints": scenario.relevant_constraints,
                "approval_thresholds": {},
                "confidence": "unknown",
                "created_at": _now_iso(),
            },
            "execution_boundary_result": {
                "status": "ESCALATE",
                "reason": "EBE v2 integration not wired yet",
            },
            "assistant_message": "Execution path selected; boundary review required.",
            "rail_state": {"mode": "execution_review"},
        }

    if turn_class == "evidence_seeking":
        return {
            "decision_result": None,
            "action_proposal": None,
            "execution_boundary_result": None,
            "assistant_message": "Evidence path selected.",
            "rail_state": {"mode": "evidence"},
        }

    return {
        "decision_result": None,
        "action_proposal": None,
        "execution_boundary_result": None,
        "assistant_message": "Conversational path selected.",
        "rail_state": {"mode": "conversation"},
    }


def run_orchestration(
    *,
    user_text: str,
    scenario_type: str = "general",
    governing_objective: str = "unspecified",
    relevant_constraints: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    turn_class = classify_turn(user_text)
    scenario = build_scenario_envelope(
        user_text=user_text,
        turn_class=turn_class,
        scenario_type=scenario_type,
        governing_objective=governing_objective,
        relevant_constraints=relevant_constraints,
    )
    routed = route_turn(turn_class=turn_class, scenario=scenario)

    return {
        "ok": True,
        "turn_class": turn_class,
        "scenario": scenario.to_dict(),
        "decision_result": routed["decision_result"],
        "action_proposal": routed["action_proposal"],
        "execution_boundary_result": routed["execution_boundary_result"],
        "assistant_message": routed["assistant_message"],
        "rail_state": routed["rail_state"],
    }

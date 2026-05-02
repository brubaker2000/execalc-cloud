from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict, Optional

from src.service.decision_loop.models import ActionProposal
from src.service.decision_loop.service import run_decision_service
from src.service.execution_record import ExecutionRecord
from src.service.orchestration.models import NavigationEnvelope, ScenarioEnvelope, TurnClass


def _now() -> datetime:
    return datetime.now(UTC)


def _serialize_action_proposal(proposal: ActionProposal) -> Dict[str, Any]:
    return {
        "proposal_id": proposal.proposal_id,
        "tenant_id": proposal.tenant_id,
        "user_id": proposal.user_id,
        "action_type": proposal.action_type,
        "target_ref": proposal.target_ref,
        "payload": proposal.payload,
        "decision_envelope_id": proposal.decision_envelope_id,
        "issued_at": proposal.issued_at.isoformat(),
        "expires_at": proposal.expires_at.isoformat() if proposal.expires_at else None,
        "authority_context": proposal.authority_context,
        "risk_level": proposal.risk_level,
        "requires_human_review": proposal.requires_human_review,
    }


def _noop_persist(record: ExecutionRecord) -> Dict[str, Any]:
    return {
        "persisted": False,
        "persist_table": None,
        "envelope_id": record.envelope_id,
        "mode": "orchestration_noop",
    }


_EBE_BRIDGE_PENDING_REASON = "execution_boundary_bridge_pending"

_EXECUTION_TRIGGERS = {
    "send it", "send this", "go ahead", "go for it",
    "run the next step", "approve this", "approve it",
    "execute this", "execute it", "run it", "do it now",
    "let's do it", "let's go", "pull the trigger",
    "confirm this", "confirm it", "submit this", "submit it",
    "launch this", "launch it", "finalize this", "finalize it",
    "proceed with this", "proceed with it", "proceed",
    "authorize this", "authorize it", "make it happen",
    "move forward on this", "move forward",
}

_ACTION_TRIGGERS = {
    "draft the next move", "draft a", "draft the",
    "prepare the outreach", "prepare a draft", "prepare the draft",
    "generate the action", "generate an action", "generate a draft",
    "write the outreach", "write a draft", "write the draft",
    "compose a", "compose the", "formulate a", "formulate the",
    "outline the steps", "outline the next steps",
    "build the plan", "build a plan",
    "create the action", "create an action",
    "structure the next move", "structure the action",
    "put together a plan",
}

_EVIDENCE_TRIGGERS = {
    "what evidence", "pull the relevant docs", "what internal data",
    "show me the data", "what data do we have",
    "find the relevant docs", "pull the data",
    "what does the research say", "show the research",
    "retrieve the docs", "fetch the data",
    "find evidence", "look up the", "search for evidence",
    "what information do we have", "what do the docs say",
}

_DECISION_TRIGGERS = {
    "which option is better", "which is better", "which should we",
    "evaluate this", "evaluate the", "what should we do",
    "what should i do", "should we", "should i",
    "recommend", "what do you recommend", "what do you think",
    "assess this", "assess the", "analyze this",
    "how should we approach", "how should i approach",
    "compare these", "compare the options", "make a call",
    "decide", "help me decide", "what's the best option",
    "what is the best", "weigh the options", "pros and cons",
    "trade-offs", "tradeoffs", "what's the right move",
    "what is the right move", "give me your judgment",
    "run an analysis",
}


def classify_turn(user_text: str) -> TurnClass:
    text = (user_text or "").strip().lower()
    if any(phrase in text for phrase in _EXECUTION_TRIGGERS):
        return "execution_seeking"
    if any(phrase in text for phrase in _ACTION_TRIGGERS):
        return "action_proposing"
    if any(phrase in text for phrase in _EVIDENCE_TRIGGERS):
        return "evidence_seeking"
    if any(phrase in text for phrase in _DECISION_TRIGGERS):
        return "decision_seeking"
    return "conversational"


def build_scenario_envelope(
    *,
    user_text: str,
    turn_class: TurnClass,
    scenario_type: str = "general",
    governing_objective: str = "unspecified",
    relevant_constraints: Optional[Dict[str, Any]] = None,
    navigation: Optional[Dict[str, Optional[str]]] = None,
) -> ScenarioEnvelope:
    now = _now()
    navigation_envelope = NavigationEnvelope(**(navigation or {}))
    return ScenarioEnvelope(
        scenario_id=f"scenario_{int(now.timestamp())}",
        scenario_type=scenario_type,
        governing_objective=governing_objective,
        user_intent=turn_class,
        prompt=user_text,
        relevant_constraints=relevant_constraints or {},
        decision_state="pending" if turn_class in ("decision_seeking", "action_proposing", "execution_seeking") else "not_requested",
        action_state="pending" if turn_class in ("action_proposing", "execution_seeking") else "not_requested",
        navigation=navigation_envelope,
        created_at=now,
        updated_at=now,
    )


def _build_action_proposal(
    *,
    scenario: ScenarioEnvelope,
    tenant_id: str,
    user_id: str,
    action_type: str,
    requires_human_review: bool = False,
    risk_level: str = "unknown",
) -> ActionProposal:
    return ActionProposal(
        proposal_id=f"proposal_{scenario.scenario_id}",
        tenant_id=tenant_id,
        user_id=user_id,
        action_type=action_type,
        payload={"source_prompt": scenario.prompt},
        decision_envelope_id=scenario.scenario_id,
        authority_context={"governing_objective": scenario.governing_objective},
        risk_level=risk_level,
        requires_human_review=requires_human_review,
    )


def route_turn(
    *,
    turn_class: TurnClass,
    scenario: ScenarioEnvelope,
    tenant_id: str,
    user_id: str,
) -> Dict[str, Any]:
    if turn_class == "decision_seeking":
        decision_out = run_decision_service(
            tenant_id=tenant_id,
            user_id=user_id,
            scenario_in={
                "scenario_type": scenario.scenario_type,
                "governing_objective": scenario.governing_objective,
                "prompt": scenario.prompt,
                "constraints": scenario.relevant_constraints,
            },
            persist_fn=_noop_persist,
        )
        return {
            "decision_result": decision_out,
            "action_proposal": None,
            "execution_boundary_result": decision_out.get("execution_boundary"),
            "assistant_message": "Decision path selected.",
            "rail_state": {"mode": "decision"},
        }

    if turn_class == "action_proposing":
        decision_out = run_decision_service(
            tenant_id=tenant_id,
            user_id=user_id,
            scenario_in={
                "scenario_type": scenario.scenario_type,
                "governing_objective": scenario.governing_objective,
                "prompt": scenario.prompt,
                "constraints": scenario.relevant_constraints,
            },
            persist_fn=_noop_persist,
        )
        proposal = _build_action_proposal(
            scenario=scenario,
            tenant_id=tenant_id,
            user_id=user_id,
            action_type="proposed_action",
        )
        return {
            "decision_result": decision_out,
            "action_proposal": _serialize_action_proposal(proposal),
            "execution_boundary_result": None,
            "assistant_message": "Action proposal path selected.",
            "rail_state": {"mode": "action_proposal"},
        }

    if turn_class == "execution_seeking":
        decision_out = run_decision_service(
            tenant_id=tenant_id,
            user_id=user_id,
            scenario_in={
                "scenario_type": scenario.scenario_type,
                "governing_objective": scenario.governing_objective,
                "prompt": scenario.prompt,
                "constraints": scenario.relevant_constraints,
            },
            persist_fn=_noop_persist,
        )
        proposal = _build_action_proposal(
            scenario=scenario,
            tenant_id=tenant_id,
            user_id=user_id,
            action_type="execution_requested",
            requires_human_review=True,
            risk_level="elevated",
        )
        # Adjust boundary decision for escalation
        execution_boundary_result = decision_out.get("execution_boundary", {})
        if not execution_boundary_result:
            execution_boundary_result = {
                "status": "ESCALATE",
                "reason": _EBE_BRIDGE_PENDING_REASON,
            }
        return {
            "decision_result": decision_out,
            "action_proposal": _serialize_action_proposal(proposal),
            "execution_boundary_result": execution_boundary_result,
            "assistant_message": "Execution path selected; boundary review required.",
            "rail_state": {"mode": "execution_review"},
        }

    if turn_class == "evidence_seeking":
        return {
            "decision_result": None,
            "action_proposal": None,
            "execution_boundary_result": None,
            "assistant_message": (
                "Evidence and corpus retrieval is not yet available. "
                "The GAQP knowledge corpus is a planned Stage 9 capability."
            ),
            "rail_state": {"mode": "evidence_unavailable"},
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
    navigation: Optional[Dict[str, Optional[str]]] = None,
    tenant_id: str = "tenant_test_001",
    user_id: str = "test_user",
) -> Dict[str, Any]:
    turn_class = classify_turn(user_text)
    scenario = build_scenario_envelope(
        user_text=user_text,
        turn_class=turn_class,
        scenario_type=scenario_type,
        governing_objective=governing_objective,
        relevant_constraints=relevant_constraints,
        navigation=navigation,
    )
    routed = route_turn(
        turn_class=turn_class,
        scenario=scenario,
        tenant_id=tenant_id,
        user_id=user_id,
    )

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

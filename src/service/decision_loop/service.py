from __future__ import annotations

from typing import Any, Callable, Dict
import secrets

from src.service.decision_loop.engine import run_decision_loop
from src.service.decision_loop.models import Scenario
from src.service.execution_record import ExecutionRecord


def run_decision_service(
    *,
    tenant_id: str,
    user_id: str,
    scenario_in: Dict[str, Any],
    persist_fn: Callable[[ExecutionRecord], Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Canonical orchestration layer for decision execution.

    Responsibilities:
    - validate and normalize scenario payload
    - construct Scenario runtime object
    - invoke decision engine
    - assemble canonical ExecutionRecord
    - call persistence abstraction
    - return final API-ready payload
    """
    if not isinstance(scenario_in, dict):
        raise ValueError("scenario must be an object")

    facts = scenario_in.get("facts") or {}
    constraints = scenario_in.get("constraints") or {}

    if not isinstance(facts, dict):
        raise ValueError("facts must be an object")
    if not isinstance(constraints, dict):
        raise ValueError("constraints must be an object")

    scenario = Scenario(
        scenario_type=str(scenario_in.get("scenario_type") or "feasibility"),
        governing_objective=str(scenario_in.get("governing_objective") or "unspecified_objective"),
        prompt=str(scenario_in.get("prompt") or ""),
        facts=facts,
        constraints=constraints,
        requested_depth=str(scenario_in.get("requested_depth") or "standard"),
        decision_horizon=str(scenario_in.get("decision_horizon")) if scenario_in.get("decision_horizon") is not None else None,
        stakeholder_scope=str(scenario_in.get("stakeholder_scope")) if scenario_in.get("stakeholder_scope") is not None else None,
        risk_surface=str(scenario_in.get("risk_surface")) if scenario_in.get("risk_surface") is not None else None,
        assumptions=str(scenario_in.get("assumptions")) if scenario_in.get("assumptions") is not None else None,
        decision_notes=str(scenario_in.get("decision_notes")) if scenario_in.get("decision_notes") is not None else None,
        tenant_id=tenant_id,
        operator_id=user_id,
    )

    report = run_decision_loop(tenant_id=tenant_id, user_id=user_id, scenario=scenario)

    envelope_id = secrets.token_hex(16)
    record = ExecutionRecord(
        tenant_id=tenant_id,
        envelope_id=envelope_id,
        result=report.to_dict(),
    )
    persisted = persist_fn(record)

    out = report.to_dict()
    out["audit"] = dict(out.get("audit") or {})
    out["audit"]["envelope_id"] = envelope_id
    out["audit"]["persist"] = persisted
    return out

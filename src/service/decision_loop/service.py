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

def get_decision_service(
    *,
    tenant_id: str,
    envelope_id: str,
    persist_enabled: bool,
    get_record_fn: Callable[..., Any] | None,
) -> tuple[Dict[str, Any], int]:
    """
    Canonical orchestration layer for decision retrieval by envelope_id.
    Returns an API-ready payload and status code.
    """
    eid = (envelope_id or "").strip().lower()
    if not eid or any(c not in "0123456789abcdef" for c in eid) or len(eid) < 16:
        return {"ok": False, "error": "invalid envelope_id"}, 400

    if not persist_enabled:
        return {"ok": False, "error": "not_found"}, 404

    if get_record_fn is None:
        return {"ok": False, "error": "db_unavailable"}, 503

    try:
        rec = get_record_fn(tenant_id=tenant_id, envelope_id=eid)
    except Exception as e:
        return {"ok": False, "error": "db_unavailable", "detail": str(e)}, 503

    if not rec:
        return {"ok": False, "error": "not_found"}, 404

    return {
        "ok": True,
        "envelope_id": rec.get("envelope_id"),
        "created_at": rec.get("created_at"),
        "result": rec.get("result"),
    }, 200


def list_recent_decisions_service(
    *,
    tenant_id: str,
    raw_limit: str,
    persist_enabled: bool,
    list_records_fn: Callable[..., Any] | None,
) -> tuple[Dict[str, Any], int]:
    """
    Canonical orchestration layer for recent decision listing.
    Returns an API-ready payload and status code.
    """
    raw = (raw_limit or "").strip()
    try:
        limit = int(raw) if raw else 25
    except ValueError:
        return {"ok": False, "error": "limit must be an integer"}, 400

    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100

    if not persist_enabled:
        return {"ok": True, "records": [], "persist_enabled": False}, 200

    if list_records_fn is None:
        return {"ok": False, "error": "db_unavailable"}, 503

    try:
        rows = list_records_fn(tenant_id=tenant_id, limit=limit)
    except Exception as e:
        return {"ok": False, "error": "db_unavailable", "detail": str(e)}, 503

    return {"ok": True, "records": rows, "persist_enabled": True}, 200

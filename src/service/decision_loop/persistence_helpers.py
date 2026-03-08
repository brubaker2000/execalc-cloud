from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.service.db.postgres import (
    insert_execution_record,
    get_execution_record,
    list_execution_records,
)


def save_decision_entry(tenant_id: str, user_id: str, decision_data: Any) -> str:
    """
    Compatibility wrapper over canonical execution_records persistence.

    Persists the supplied decision payload as an execution record and returns
    the generated envelope_id, which acts as the durable retrieval key.
    """
    payload: Dict[str, Any]
    if isinstance(decision_data, dict):
        payload = dict(decision_data)
    else:
        payload = {"value": decision_data}

    envelope_id = str(payload.get("envelope_id") or f"decision-{tenant_id}-{user_id}")
    insert_execution_record(
        tenant_id=tenant_id,
        envelope_id=envelope_id,
        result=payload,
    )
    return envelope_id


def get_decision_entry(entry_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """
    Compatibility wrapper that fetches a canonical execution record by
    (tenant_id, envelope_id).
    """
    return get_execution_record(tenant_id=tenant_id, envelope_id=entry_id)


def get_all_decisions_for_tenant(tenant_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Compatibility wrapper that lists recent execution records for a tenant.
    """
    return list_execution_records(tenant_id=tenant_id, limit=limit)

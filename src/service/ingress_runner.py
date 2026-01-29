"""
Ingress Runner

Canonical end-to-end pattern for executing tenant-scoped service calls:

raw_input (dict) -> IngressEnvelope -> seal -> run_as_request -> ExecutionRecord

This prevents ad-hoc context setup in future API/Zapier/webhook handlers.
"""

from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, Optional, Tuple

from src.service.envelope import IngressEnvelope
from src.service.envelope_seal import seal_envelope
from src.service.execution_record import ExecutionRecord
from src.service.tenant.entrypoint import run_as_request
from src.service.tenant.errors import InvalidTenantPayload
from src.service.tenant.identity import TenantIdentity


def execute_ingress(
    raw_input: Dict[str, Any],
    *,
    user_id: str,
    role: str,
    fn: Callable[..., Any],
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    tenant_name: Optional[str] = None,
    envelope_id: Optional[str] = None,
) -> ExecutionRecord:
    """
    Execute a tenant-scoped callable from external input in a canonical way.

    - Validates tenant_id presence at ingress.
    - Builds and seals an IngressEnvelope (structure contract).
    - Runs the service inside request-scoped tenant+actor context.
    - Returns an ExecutionRecord with either success output or error payload.
    """
    if not isinstance(raw_input, dict):
        raise InvalidTenantPayload("raw_input must be a dict.")
    tenant_id = raw_input.get("tenant_id")
    if not tenant_id:
        raise InvalidTenantPayload("Missing tenant_id at ingress.")

    args = args or ()
    kwargs = kwargs or {}

    env_id = envelope_id or raw_input.get("envelope_id") or uuid.uuid4().hex

    env = IngressEnvelope(
        input=raw_input,
        tenant_context=TenantIdentity(
            tenant_id=tenant_id,
            tenant_name=tenant_name or raw_input.get("tenant_name"),
        ),
        meta={"envelope_id": env_id},
    )
    seal_envelope(env)

    try:
        result = run_as_request(
            raw_input,
            user_id=user_id,
            role=role,
            metadata={"envelope_id": env_id},
            fn=fn,
            args=args,
            kwargs=kwargs,
        )
        payload = {"ok": True, "data": result}
    except Exception as e:
        payload = {
            "ok": False,
            "error_type": e.__class__.__name__,
            "error": str(e),
        }

    return ExecutionRecord(
        tenant_id=tenant_id,
        envelope_id=env_id,
        result=payload,
    )

"""
Tenant Context Injector

Creates an immutable TenantContext from
validated tenant data and attaches it to
the runtime envelope.
"""

from typing import Dict, Any
from src.service.tenant.context import TenantContext


def inject_tenant_context(
    envelope: Dict[str, Any],
    tenant_record: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Attach TenantContext to the envelope.

    Assumes:
    - tenant_record is trusted and validated
    - envelope is mutable at ingress only
    """

    envelope["tenant_context"] = TenantContext(
        tenant_id=tenant_record["tenant_id"],
        tenant_name=tenant_record["tenant_name"],
    )

    return envelope

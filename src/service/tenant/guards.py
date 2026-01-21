"""
Tenant Context Guards

Utilities to enforce immutability of tenant context
after ingress.
"""

from typing import Dict, Any
from dataclasses import is_dataclass
from src.service.tenant.context import TenantContext


def assert_tenant_context_immutable(envelope: Dict[str, Any]) -> None:
    """
    Raise if tenant_context is missing or not immutable.

    Intended to be called at boundary points
    after ingress (e.g., before routing, execution).
    """

    if "tenant_context" not in envelope:
        raise RuntimeError("Tenant context missing from envelope")

    tenant_context = envelope["tenant_context"]

    if not isinstance(tenant_context, TenantContext):
        raise RuntimeError("Invalid tenant context type")

    if not is_dataclass(tenant_context) or not getattr(tenant_context, "__dataclass_params__", None).frozen:
        raise RuntimeError("Tenant context must be frozen and immutable")

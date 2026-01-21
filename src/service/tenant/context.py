"""
Tenant Context

Immutable tenant identity injected at ingress
and propagated through the runtime envelope.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    tenant_name: str

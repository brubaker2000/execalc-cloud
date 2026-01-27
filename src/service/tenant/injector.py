"""
Tenant Context Injector

Ingress helper that sets (or validates) the execution tenant context
from an envelope-like dict.
"""

from src.service.tenant.context import peek_tenant_context, set_tenant_context
from src.service.tenant.errors import InvalidTenantPayload


def inject_tenant_context(envelope: dict) -> dict:
    if not isinstance(envelope, dict):
        raise InvalidTenantPayload("Envelope must be a dict.")

    tenant_id = envelope.get("tenant_id")
    if not tenant_id:
        raise InvalidTenantPayload("Envelope missing tenant_id.")

    current = peek_tenant_context()

    # If already set, it must match (no mid-flight tenant switching).
    if current and current != tenant_id:
        raise InvalidTenantPayload(
            f"Envelope tenant_id '{tenant_id}' does not match execution tenant context '{current}'."
        )

    # Context not set yet — set it now (ingress).
    if not current:
        set_tenant_context(tenant_id)

    return envelope

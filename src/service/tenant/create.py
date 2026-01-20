"""
Execalc Cloud v1 — Tenant Creation Contract

This module defines the contract for creating a tenant.
It validates intent and structure only.
No persistence, side effects, or execution beyond validation are permitted.
"""

class TenantCreationError(Exception):
    """Base exception for tenant creation violations."""
    pass


class InvalidTenantPayload(TenantCreationError):
    """Raised when the tenant payload is invalid or incomplete."""
    pass


def create_tenant(payload):
    """
    Validate a tenant creation request.

    Required fields:
    - tenant_id: unique identifier for the tenant
    - name: human-readable tenant name

    This function does NOT:
    - Persist data
    - Allocate resources
    - Modify system state

    It exists solely to define and enforce the tenant creation contract.
    """

    if not isinstance(payload, dict):
        raise InvalidTenantPayload("Tenant payload must be a dictionary.")

    tenant_id = payload.get("tenant_id")
    name = payload.get("name")

    if not tenant_id or not isinstance(tenant_id, str):
        raise InvalidTenantPayload("tenant_id is required and must be a string.")

    if not name or not isinstance(name, str):
        raise InvalidTenantPayload("name is required and must be a string.")

    return {
        "tenant_id": tenant_id,
        "name": name,
        "status": "validated",
        "message": "Tenant payload is valid. No persistence performed."
    }

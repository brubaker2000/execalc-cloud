from src.service.tenant.envelope import ingest_envelope
from src.service.tenant.model import Tenant
from src.service.tenant.persistence import create_tenant

def create_tenant_service(payload: dict) -> dict:
    # Enforce tenant context + envelope validation first.
    ingest_envelope(payload)

    tenant_id = payload["tenant_id"]
    name = payload["name"]
    status = "active"  # Default status for now
    created_at = "2026-01-01T00:00:00Z"  # Placeholder created_at timestamp

    tenant = Tenant(tenant_id, name, status, created_at)
    create_tenant(tenant.tenant_id, tenant.name, tenant.status, tenant.created_at)

    return {
        "tenant_id": tenant.tenant_id,
        "name": tenant.name,
        "status": tenant.status,
        "created_at": tenant.created_at,
    }

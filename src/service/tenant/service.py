from src.service.tenant.envelope import ingest_envelope
from src.service.tenant.errors import TenantNotFound
from src.service.tenant.model import Tenant
from src.service.tenant.persistence import create_tenant, get_tenant
from src.service.tenant.authz import assert_actor_role_in

def create_tenant_service(payload: dict) -> dict:
    ingest_envelope(payload)

    # Creating tenants is a privileged system operation.
    assert_actor_role_in(["admin", "system"])

    tenant_id = payload["tenant_id"]
    name = payload["name"]
    status = "active"
    created_at = "2026-01-01T00:00:00Z"

    tenant = Tenant(tenant_id, name, status, created_at)
    create_tenant(tenant.tenant_id, tenant.name, tenant.status, tenant.created_at)

    return {
        "tenant_id": tenant.tenant_id,
        "name": tenant.name,
        "status": tenant.status,
        "created_at": tenant.created_at,
    }

def get_tenant_service(tenant_id: str) -> dict:
    # Envelope expects a dict payload; use a minimal one for enforcement.
    ingest_envelope({"tenant_id": tenant_id, "name": "__read__"})

    # Reading tenant metadata requires at least read access.
    assert_actor_role_in(["admin", "operator", "viewer", "system"])

    row = get_tenant(tenant_id)
    if not row:
        raise TenantNotFound(f"Tenant '{tenant_id}' not found.")

    return {
        "tenant_id": row[0],
        "name": row[1],
        "status": row[2],
        "created_at": row[3],
    }

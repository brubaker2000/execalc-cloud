from src.service.tenant.context import get_tenant_context
from src.service.tenant.errors import InvalidTenantPayload

def ingest_envelope(payload: dict) -> None:
    # Enforce that an execution tenant context is set.
    ctx_tenant_id = get_tenant_context()
    if not ctx_tenant_id:
        raise InvalidTenantPayload("Missing tenant execution context.")

    # Basic payload validation (target tenant).
    if not isinstance(payload, dict):
        raise InvalidTenantPayload("Payload must be a dict.")
    if not payload.get("tenant_id"):
        raise InvalidTenantPayload("Missing tenant_id in the payload.")
    if not payload.get("name"):
        raise InvalidTenantPayload("Missing name in the payload.")

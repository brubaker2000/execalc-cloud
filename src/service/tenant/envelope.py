from src.service.tenant.actor_context import get_actor_context
from src.service.tenant.context import get_tenant_context
from src.service.tenant.errors import InvalidTenantPayload

def ingest_envelope(payload: dict) -> None:
    # Enforce that an execution tenant context is set.
    _ = get_tenant_context()

    # Enforce that an actor context is set (who is calling).
    _ = get_actor_context()

    # Basic payload validation (target tenant).
    if not isinstance(payload, dict):
        raise InvalidTenantPayload("Payload must be a dict.")
    if not payload.get("tenant_id"):
        raise InvalidTenantPayload("Missing tenant_id in the payload.")
    if not payload.get("name"):
        raise InvalidTenantPayload("Missing name in the payload.")

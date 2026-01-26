from contextvars import ContextVar
from typing import Optional

from src.service.tenant.errors import InvalidTenantPayload


_tenant_id_ctx: ContextVar[Optional[str]] = ContextVar("tenant_id", default=None)


def set_tenant_context(tenant_id: str) -> None:
    if not isinstance(tenant_id, str) or not tenant_id.strip():
        raise InvalidTenantPayload("tenant_id must be a non-empty string.")
    _tenant_id_ctx.set(tenant_id)


def get_tenant_context() -> str:
    tenant_id = _tenant_id_ctx.get()
    if not tenant_id:
        raise InvalidTenantPayload("Tenant context is not set.")
    return tenant_id


def clear_tenant_context() -> None:
    _tenant_id_ctx.set(None)

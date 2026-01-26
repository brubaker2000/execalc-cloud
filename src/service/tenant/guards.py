"""
Tenant Guards

Small guard utilities to enforce tenant safety invariants.
"""

from src.service.tenant.context import get_tenant_context
from src.service.tenant.errors import InvalidTenantPayload


def assert_execution_tenant_context_set() -> str:
    """
    Returns the current execution tenant_id (raises if missing).
    """
    return get_tenant_context()


def assert_target_tenant_matches_execution(target_tenant_id: str) -> None:
    """
    Default invariant: the tenant you are acting on must match
    the execution tenant context, unless a higher-privilege pathway
    explicitly overrides this later.
    """
    exec_tenant_id = get_tenant_context()
    if target_tenant_id != exec_tenant_id:
        raise InvalidTenantPayload(
            f"Target tenant_id '{target_tenant_id}' does not match execution tenant context '{exec_tenant_id}'."
        )

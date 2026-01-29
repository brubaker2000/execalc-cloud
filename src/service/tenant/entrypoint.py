"""
Tenant Entrypoint Runner

This is the canonical pattern for invoking tenant-scoped services:
- Establish request_context (tenant + actor) exactly once
- Execute the service function
- Guarantee cleanup
"""

from typing import Any, Callable, Dict, Optional

from src.service.tenant.request_context import request_context


def run_as_request(
    envelope: Dict[str, Any],
    *,
    user_id: str,
    role: str,
    metadata: Optional[Dict[str, Any]] = None,
    fn: Callable[..., Any],
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> Any:
    """
    Runs a callable inside a tenant+actor request context.

    Parameters:
        envelope: Must include tenant_id.
        user_id/role/metadata: Derived from auth; not trusted from payload by default.
        fn: Service callable to invoke.
        args/kwargs: Arguments for the callable.

    Returns:
        Whatever the callable returns.
    """
    args = args or ()
    kwargs = kwargs or {}

    with request_context(envelope, user_id=user_id, role=role, metadata=metadata):
        return fn(*args, **kwargs)

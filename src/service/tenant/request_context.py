"""
Request Context

Single, authoritative wrapper for setting and clearing execution context
for a single request. This prevents tenant/actor context bleed.
"""

from contextlib import contextmanager
from typing import Dict, Any, Optional

from src.service.tenant.injector import inject_tenant_context
from src.service.tenant.actor_context import set_actor_context, clear_actor_context
from src.service.tenant.context import clear_tenant_context


@contextmanager
def request_context(
    envelope: Dict[str, Any],
    *,
    user_id: str,
    role: str,
    metadata: Optional[Dict[str, Any]] = None,
):
    """
    Establishes tenant + actor execution contexts for one request and guarantees cleanup.
    - Tenant context is derived from the envelope (ingress).
    - Actor context is derived from the auth layer (not trusted from payload by default).
    """
    try:
        inject_tenant_context(envelope)
        set_actor_context(user_id=user_id, role=role, metadata=metadata)
        yield
    finally:
        # Cleanup must always happen, even on exceptions.
        clear_actor_context()
        clear_tenant_context()

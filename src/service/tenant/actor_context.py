from contextvars import ContextVar
from typing import Optional, Dict, Any

from src.service.tenant.errors import InvalidTenantPayload

_actor_ctx: ContextVar[Optional[Dict[str, Any]]] = ContextVar("actor_ctx", default=None)

def set_actor_context(user_id: str, role: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    if not isinstance(user_id, str) or not user_id.strip():
        raise InvalidTenantPayload("user_id must be a non-empty string.")
    if not isinstance(role, str) or not role.strip():
        raise InvalidTenantPayload("role must be a non-empty string.")
    _actor_ctx.set({"user_id": user_id, "role": role, "metadata": metadata or {}})

def get_actor_context() -> Dict[str, Any]:
    ctx = _actor_ctx.get()
    if not ctx:
        raise InvalidTenantPayload("Actor context is not set.")
    return ctx

def clear_actor_context() -> None:
    _actor_ctx.set(None)

"""
Authorization (RBAC)

Small, explicit role→permission mapping for the tenant kernel.
This is intentionally simple and testable.
"""

from typing import Dict, Iterable, Set

from src.service.tenant.actor_context import get_actor_context
from src.service.tenant.errors import Unauthorized


ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    # Full control within a tenant boundary.
    "admin": {"tenant:read", "tenant:write", "system:configure"},
    # Typical operator inside a tenant.
    "operator": {"tenant:read", "tenant:write"},
    # Read-only access.
    "viewer": {"tenant:read"},
    # Internal/service actor (used by system automations).
    "system": {"tenant:read", "tenant:write", "system:configure"},
}


def assert_actor_role_in(allowed_roles: Iterable[str]) -> None:
    ctx = get_actor_context()
    role = ctx.get("role")
    if role not in set(allowed_roles):
        raise Unauthorized(f"Role '{role}' is not permitted for this action.")


def assert_actor_has_permission(permission: str) -> None:
    ctx = get_actor_context()
    role = ctx.get("role")

    perms = ROLE_PERMISSIONS.get(role)
    if perms is None:
        raise Unauthorized(f"Unknown role '{role}'.")

    if permission not in perms:
        raise Unauthorized(f"Role '{role}' lacks permission '{permission}'.")

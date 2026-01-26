from typing import Dict
from src.service.tenant.errors import InvalidTenantPayload


class ActorContext:
    def __init__(self, user_id: str, role: str, metadata: Dict = None):
        self.user_id = user_id
        self.role = role
        self.metadata = metadata or {}

    def add_metadata(self, key: str, value: str):
        self.metadata[key] = value

    def get_metadata(self):
        return self.metadata


# Define roles and permissions
ROLE_PERMISSIONS = {
    "admin": {"create_tenant", "get_tenant", "update_tenant", "delete_tenant"},
    "viewer": {"get_tenant"},
    "editor": {"get_tenant", "update_tenant"},
}

def set_actor_context(user_id: str, role: str, metadata: Dict = None) -> ActorContext:
    if not user_id or not role:
        raise InvalidTenantPayload("user_id and role must be non-empty strings.")
    if role not in ROLE_PERMISSIONS:
        raise InvalidTenantPayload(f"Invalid role '{role}'.")
    
    actor_context = ActorContext(user_id, role, metadata)
    return actor_context

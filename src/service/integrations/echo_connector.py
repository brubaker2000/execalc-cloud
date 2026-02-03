from __future__ import annotations

from typing import Any, Dict

from .connector import ConnectorContext


class EchoConnector:
    """
    Simple test connector that echoes inputs back.

    Used to validate:
    - registry wiring
    - tenant/role enforcement
    - required scopes enforcement
    - request body shape handling
    """
    name = "echo"

    def healthcheck(self, ctx: ConnectorContext) -> Dict[str, Any]:
        return {"ok": True, "connector": self.name, "tenant_id": ctx.tenant_id}

    def fetch(self, ctx: ConnectorContext, query: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ok": True,
            "connector": self.name,
            "tenant_id": ctx.tenant_id,
            "query": query,
        }

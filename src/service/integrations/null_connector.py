from __future__ import annotations

from typing import Any, Dict

from .connector import ConnectorContext


class NullConnector:
    """
    Test/dummy connector.

    Used to prove registry wiring and connector invocation paths
    without touching real external systems.
    """
    name = "null"

    def healthcheck(self, ctx: ConnectorContext) -> Dict[str, Any]:
        return {"ok": True, "connector": self.name, "tenant_id": ctx.tenant_id}

    def fetch(self, ctx: ConnectorContext, query: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "connector": self.name, "tenant_id": ctx.tenant_id, "query": query}

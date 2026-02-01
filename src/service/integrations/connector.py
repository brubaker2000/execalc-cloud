from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol


@dataclass(frozen=True)
class ConnectorContext:
    """
    Minimal runtime context passed into connectors.
    Expand deliberately as we add auth, RBAC, per-tenant scoping, etc.
    """
    tenant_id: str
    actor_id: Optional[str] = None
    scopes: Optional[list[str]] = None


class Connector(Protocol):
    """
    Connector contract.

    Connectors are intentionally *thin* wrappers around external systems.
    They do not own governance. They return structured data; Execalc governs usage.
    """
    name: str

    def healthcheck(self, ctx: ConnectorContext) -> Dict[str, Any]:
        ...

    def fetch(self, ctx: ConnectorContext, query: Dict[str, Any]) -> Dict[str, Any]:
        ...

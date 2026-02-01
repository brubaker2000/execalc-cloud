from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Type

from .connector import Connector


class ConnectorRegistryError(Exception):
    pass


@dataclass
class ConnectorRegistry:
    """
    Simple in-process registry.

    Later upgrades (without breaking API):
    - per-tenant enablement flags
    - RBAC gating and scope enforcement
    - lazy initialization + credential injection
    - connector discovery via entrypoints/plugins
    """
    _connectors: Dict[str, Connector]

    @classmethod
    def empty(cls) -> "ConnectorRegistry":
        return cls(_connectors={})

    def register(self, connector: Connector) -> None:
        name = getattr(connector, "name", None)
        if not name or not isinstance(name, str):
            raise ConnectorRegistryError("Connector must define a non-empty string 'name'.")
        if name in self._connectors:
            raise ConnectorRegistryError(f"Connector already registered: {name}")
        self._connectors[name] = connector

    def get(self, name: str) -> Connector:
        if name not in self._connectors:
            raise ConnectorRegistryError(f"Unknown connector: {name}")
        return self._connectors[name]

    def list(self) -> Iterable[str]:
        return sorted(self._connectors.keys())

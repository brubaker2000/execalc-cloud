from __future__ import annotations

from .null_connector import NullConnector
from .registry import ConnectorRegistry


def default_registry() -> ConnectorRegistry:
    """
    Default in-process registry.

    This is the stable assembly point we can expand later with:
    - per-tenant enablement
    - RBAC/scope gating
    - credential injection
    - plugin discovery
    """
    registry = ConnectorRegistry.empty()
    registry.register(NullConnector())
    return registry

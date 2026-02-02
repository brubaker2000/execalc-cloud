from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set

from .connector import ConnectorContext


class ConnectorPolicyError(Exception):
    pass


def _load_json_env(var_name: str) -> Optional[Any]:
    raw = os.getenv(var_name)
    if raw is None or raw.strip() == "":
        return None
    try:
        return json.loads(raw)
    except Exception as e:
        raise ConnectorPolicyError(f"Invalid JSON in {var_name}: {e}") from e


def _as_str_list(value: Any, *, var_name: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ConnectorPolicyError(f"{var_name} entries must be lists of strings.")
    return value


@dataclass(frozen=True)
class ConnectorPolicy:
    """
    Runtime connector access policy.

    Env vars (JSON):
      - EXECALC_CONNECTOR_ALLOWLIST:
          {
            "*": ["null"],
            "tenant_demo_999": ["null"]
          }
        If set, tenants may only use explicitly allowed connectors.

      - EXECALC_CONNECTOR_REQUIRED_SCOPES:
          {
            "gmail": ["gmail.readonly"],
            "drive": ["drive.readonly"]
          }
        If set, connector calls require the listed scopes in ctx.scopes.
    """
    allowlist_by_tenant: Optional[Dict[str, Any]]
    required_scopes_by_connector: Optional[Dict[str, Any]]

    @classmethod
    def from_env(cls) -> "ConnectorPolicy":
        allowlist = _load_json_env("EXECALC_CONNECTOR_ALLOWLIST")
        scopes = _load_json_env("EXECALC_CONNECTOR_REQUIRED_SCOPES")

        if allowlist is not None and not isinstance(allowlist, dict):
            raise ConnectorPolicyError("EXECALC_CONNECTOR_ALLOWLIST must be a JSON object (mapping).")

        if scopes is not None and not isinstance(scopes, dict):
            raise ConnectorPolicyError("EXECALC_CONNECTOR_REQUIRED_SCOPES must be a JSON object (mapping).")

        return cls(allowlist_by_tenant=allowlist, required_scopes_by_connector=scopes)

    def allowed_connectors(self, tenant_id: str, available: Iterable[str]) -> List[str]:
        """
        If allowlist is unset -> allow all available connectors.
        If allowlist is set -> allow only tenant-specific list, falling back to '*' (wildcard).
        If tenant has no entry and no '*' -> deny all.
        """
        available_set: Set[str] = set(available)

        if self.allowlist_by_tenant is None:
            return sorted(available_set)

        raw = None
        if tenant_id in self.allowlist_by_tenant:
            raw = self.allowlist_by_tenant[tenant_id]
        elif "*" in self.allowlist_by_tenant:
            raw = self.allowlist_by_tenant["*"]

        allowed = set(_as_str_list(raw, var_name="EXECALC_CONNECTOR_ALLOWLIST"))
        return sorted(available_set.intersection(allowed))

    def _required_scopes(self, connector_name: str) -> List[str]:
        if self.required_scopes_by_connector is None:
            return []
        raw = self.required_scopes_by_connector.get(connector_name)
        return _as_str_list(raw, var_name="EXECALC_CONNECTOR_REQUIRED_SCOPES")

    def authorize_or_raise(self, connector_name: str, ctx: ConnectorContext, available: Iterable[str]) -> None:
        """
        Raises ConnectorPolicyError for misconfiguration.
        Raises PermissionError for authorization failures.
        """
        allowed = self.allowed_connectors(ctx.tenant_id, available)
        if connector_name not in allowed:
            raise PermissionError(f"Connector '{connector_name}' is not enabled for tenant '{ctx.tenant_id}'.")

        required = self._required_scopes(connector_name)
        if required:
            scopes = ctx.scopes or []
            missing = [s for s in required if s not in scopes]
            if missing:
                raise PermissionError(f"Missing required scopes for '{connector_name}': {missing}")

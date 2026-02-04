from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class CredentialStoreError(Exception):
    pass


@dataclass(frozen=True)
class CredentialStatus:
    """
    Represents whether a connector has credentials configured for a given tenant.
    secret_ref is an opaque reference (e.g., Secret Manager version URI), not secret material.
    """
    configured: bool
    secret_ref: Optional[str] = None


def _load_json_env(var_name: str) -> Optional[Any]:
    raw = os.getenv(var_name)
    if raw is None or raw.strip() == "":
        return None
    try:
        return json.loads(raw)
    except Exception as e:
        raise CredentialStoreError(f"Invalid JSON in {var_name}: {e}") from e


def _as_str_map(value: Any, *, var_name: str) -> Dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
        raise CredentialStoreError(f"{var_name} must be a JSON object mapping strings to strings.")
    return value


def _as_str_list(value: Any, *, var_name: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise CredentialStoreError(f"{var_name} entries must be lists of strings.")
    return value


def _as_str_list_map(value: Any, *, var_name: str) -> Dict[str, List[str]]:
    """
    Validates a mapping like: {"*":["gmail"],"tenant_a":["gdrive"]}.
    """
    if value is None:
        return {}
    if not isinstance(value, dict) or not all(isinstance(k, str) for k in value.keys()):
        raise CredentialStoreError(f"{var_name} must be a JSON object mapping strings to lists of strings.")
    out: Dict[str, List[str]] = {}
    for k, v in value.items():
        out[k] = _as_str_list(v, var_name=var_name)
    return out


class EnvCredentialStore:
    """
    Reads per-tenant connector secret references from env.

    Env var:
      EXECALC_CONNECTOR_SECRET_REFS
        JSON object:
          {
            "*": {"echo": "secret://ref"},
            "tenant_a": {"gmail": "projects/.../secrets/.../versions/latest"}
          }
    """

    def __init__(self, secret_refs_by_tenant: Optional[Dict[str, Any]]):
        self.secret_refs_by_tenant = secret_refs_by_tenant

    @classmethod
    def from_env(cls) -> "EnvCredentialStore":
        refs = _load_json_env("EXECALC_CONNECTOR_SECRET_REFS")
        if refs is not None and not isinstance(refs, dict):
            raise CredentialStoreError("EXECALC_CONNECTOR_SECRET_REFS must be a JSON object (mapping).")
        return cls(secret_refs_by_tenant=refs)

    def status(self, tenant_id: str, connector_name: str) -> CredentialStatus:
        if self.secret_refs_by_tenant is None:
            return CredentialStatus(configured=False)

        raw = self.secret_refs_by_tenant.get(tenant_id)
        if raw is None:
            raw = self.secret_refs_by_tenant.get("*")

        mapping = _as_str_map(raw, var_name="EXECALC_CONNECTOR_SECRET_REFS")
        ref = mapping.get(connector_name)
        if not ref:
            return CredentialStatus(configured=False)
        return CredentialStatus(configured=True, secret_ref=ref)


@dataclass(frozen=True)
class CredentialRequirementPolicy:
    """
    Determines which connectors require credentials to be considered usable.

    Env var:
      EXECALC_CONNECTOR_CREDENTIAL_REQUIRED
        JSON object:
          {"*":["gmail","gdrive"],"tenant_a":["gcal"]}
    """
    required_by_tenant: Optional[Dict[str, List[str]]] = None

    @classmethod
    def from_env(cls) -> "CredentialRequirementPolicy":
        raw = _load_json_env("EXECALC_CONNECTOR_CREDENTIAL_REQUIRED")
        if raw is None:
            return cls(required_by_tenant=None)
        required = _as_str_list_map(raw, var_name="EXECALC_CONNECTOR_CREDENTIAL_REQUIRED")
        return cls(required_by_tenant=required)

    def requires_credentials(self, tenant_id: str, connector_name: str) -> bool:
        if self.required_by_tenant is None:
            return False
        lst = self.required_by_tenant.get(tenant_id)
        if lst is None:
            lst = self.required_by_tenant.get("*", [])
        return connector_name in lst

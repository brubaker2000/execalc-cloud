from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


class CredentialStoreError(Exception):
    pass


@dataclass(frozen=True)
class CredentialStatus:
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


class EnvCredentialStore:
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

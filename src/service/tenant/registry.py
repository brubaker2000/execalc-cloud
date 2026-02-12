"""
Tenant Registry (Canonical Runtime)

Purpose:
- Provide a single, canonical tenant existence check against the runtime registry (Postgres).
- Enforce "tenant must exist" at request boundary when enabled.

Notes:
- Enforcement is gated by env var EXECALC_ENFORCE_TENANT_REGISTRY.
- This module must not break unit tests or local runs when DB is unavailable.
"""

from __future__ import annotations

import os

from src.service.tenant.errors import TenantNotFound

try:
    # Runtime canonical store (Cloud SQL / Postgres)
    from src.service.db.postgres import get_conn  # type: ignore
except Exception:
    get_conn = None  # type: ignore


def _truthy_env(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def enforcement_enabled() -> bool:
    """
    When enabled, all requests must target a provisioned tenant in the canonical registry.
    """
    return _truthy_env("EXECALC_ENFORCE_TENANT_REGISTRY", "0")


def tenant_exists(tenant_id: str) -> bool:
    """
    Returns True if tenant_id exists in Postgres tenants table.
    Raises RuntimeError if enforcement is on but DB access is unavailable.
    """
    if get_conn is None:
        raise RuntimeError("tenant registry DB module not available")

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT 1 FROM tenants WHERE tenant_id = %s LIMIT 1", (tenant_id,))
            return cur.fetchone() is not None
    finally:
        conn.close()


def ensure_tenant_registered(tenant_id: str) -> None:
    """
    Enforces that tenant_id exists in the canonical registry, if enforcement is enabled.
    """
    if not enforcement_enabled():
        return

    if not tenant_exists(tenant_id):
        raise TenantNotFound(f"Tenant '{tenant_id}' not found in canonical registry.")

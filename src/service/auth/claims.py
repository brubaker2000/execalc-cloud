from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from flask import Request


class AuthError(Exception):
    """Raised when verified claims are missing or cannot be trusted."""


@dataclass(frozen=True)
class VerifiedClaims:
    user_id: str
    role: str
    tenant_id: Optional[str] = None
    scopes: Optional[List[str]] = None


def _dev_harness_enabled() -> bool:
    return os.getenv("EXECALC_DEV_HARNESS", "0").strip().lower() in ("1", "true", "yes", "on")


def _smoke_harness_enabled() -> bool:
    return os.getenv("EXECALC_SMOKE_HARNESS", "0").strip().lower() in ("1", "true", "yes", "on")


def _smoke_key_ok(req: Request) -> bool:
    expected = (os.getenv("EXECALC_SMOKE_KEY") or "").strip()
    if not expected:
        return False
    provided = (req.headers.get("X-Smoke-Key") or "").strip()
    return bool(provided) and provided == expected

def claims_from_request(req: Request) -> VerifiedClaims:
    """
    Verified-claims entrypoint.

    Dev harness:
      - Claims are supplied via headers for local/test use only.

    Production:
      - This will be replaced by real verified identity claims (JWT/IAP/etc.).
    """
    # Smoke harness: allows CI to exercise protected endpoints without enabling dev harness globally.
    # Enabled only when EXECALC_SMOKE_HARNESS=1 and X-Smoke-Key matches EXECALC_SMOKE_KEY.
    if _smoke_harness_enabled() and _smoke_key_ok(req):
        pass
    elif not _dev_harness_enabled():
        raise AuthError("verified claims provider not configured")

    user_id = (req.headers.get("X-User-Id") or "").strip()
    role = (req.headers.get("X-Role") or "").strip().lower()

    if not user_id:
        raise AuthError("X-User-Id header is required in dev harness")
    if not role:
        raise AuthError("X-Role header is required in dev harness")

    tenant_id = (req.headers.get("X-Tenant-Id") or "").strip() or None

    # If smoke harness is enabled, optionally lock requests to a single configured tenant.
    if _smoke_harness_enabled() and _smoke_key_ok(req):
        locked = (os.getenv("EXECALC_SMOKE_TENANT_ID") or "").strip() or None
        if locked and tenant_id != locked:
            raise AuthError("smoke harness tenant mismatch")

    scopes_hdr = (req.headers.get("X-Scopes") or "").strip()
    scopes = None
    if scopes_hdr:
        scopes = [s.strip() for s in scopes_hdr.split(",") if s.strip()]

    return VerifiedClaims(user_id=user_id, role=role, tenant_id=tenant_id, scopes=scopes)

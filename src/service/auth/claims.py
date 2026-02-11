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


def claims_from_request(req: Request) -> VerifiedClaims:
    """
    Verified-claims entrypoint.

    Dev harness:
      - Claims are supplied via headers for local/test use only.

    Production:
      - This will be replaced by real verified identity claims (JWT/IAP/etc.).
    """
    if not _dev_harness_enabled():
        raise AuthError("verified claims provider not configured")

    user_id = (req.headers.get("X-User-Id") or "").strip()
    role = (req.headers.get("X-Role") or "").strip().lower()

    if not user_id:
        raise AuthError("X-User-Id header is required in dev harness")
    if not role:
        raise AuthError("X-Role header is required in dev harness")

    tenant_id = (req.headers.get("X-Tenant-Id") or "").strip() or None

    scopes_hdr = (req.headers.get("X-Scopes") or "").strip()
    scopes = None
    if scopes_hdr:
        scopes = [s.strip() for s in scopes_hdr.split(",") if s.strip()]

    return VerifiedClaims(user_id=user_id, role=role, tenant_id=tenant_id, scopes=scopes)

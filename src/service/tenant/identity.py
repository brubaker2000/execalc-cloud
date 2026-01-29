"""
Tenant Identity

Immutable tenant identity metadata used by structure-only contracts
(e.g., IngressEnvelope, ArtifactAttribution).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TenantIdentity:
    tenant_id: str
    tenant_name: Optional[str] = None

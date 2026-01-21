"""
Ingress Envelope Contract

Defines the canonical structure of an execution envelope
at system ingress. This file contains structure only.
No validation, routing, or execution logic is permitted here.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from src.service.tenant.context import TenantContext


@dataclass
class IngressEnvelope:
    """
    Mutable at ingress only.

    Once tenant context is injected and the envelope is sealed,
    downstream execution must treat this as read-only.
    """

    # Raw external input (request, event, payload)
    input: Dict[str, Any]

    # Immutable tenant identity (injected at ingress)
    tenant_context: Optional[TenantContext] = None

    # System metadata (timestamps, ids, trace info)
    meta: Dict[str, Any] = field(default_factory=dict)

    # Indicates whether mutation is still allowed
    mutable: bool = True
